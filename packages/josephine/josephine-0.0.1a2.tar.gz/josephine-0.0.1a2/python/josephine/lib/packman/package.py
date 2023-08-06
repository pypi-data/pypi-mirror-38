from __future__ import print_function

import os
import getpass
import time
import json
import traceback
import shutil

from .exceptions import LockedError, NotLockedError

class Package(object):

    _PACKMAN_BASENAME = '.packman'
    _CONFIG_BASENAME = '.config'
    _LOCK_BASENAME = '.packlock'

    _VERSION_INFO_BASENAME = '.packinfo'
    _VERSION_OFFICIAL_BASENAME = '.official'

    @classmethod
    def create_package(cls, path, name, extension, file_content=None):
        '''
        Creates a package with the given name in the given path.
        The managed file will have the given name and the given extension.
        If the extension is None, the package will manage a folder.

        The initial version will be created and published as official.
        If it's not a folder it will contain the given file_content or a default one.

        The given name must not exists in the given path.

        Returns a Package managing the created package.
        '''
        package_path = os.path.join(path, name)
        if os.path.exists(package_path):
            raise ValueError('Path already exists: %r' % (package_path,))

        os.makedirs(os.path.join(package_path, cls._PACKMAN_BASENAME))
        config_file = os.path.join(
            package_path, cls._PACKMAN_BASENAME, cls._CONFIG_BASENAME
        )
        if extension:
            extension = extension.lstrip('.')
        config = dict(
            created_by=getpass.getuser(),
            created_on=time.time(),
            created_at=package_path,
            extension=extension,
            is_folder=not bool(extension),
        )
        with open(config_file, 'w') as fh:
            json.dump(config, fh)

        pack = cls(package_path)
        path = pack.edit(empty=True)
        if not pack.is_folder():
            file_content = file_content or '# Initial version.\n'
            with open(path, 'w') as fh:
                fh.write(file_content)
        pack.publish('Initial version.', official=True)

        return pack

    def __init__(self, package_path):
        super(Package, self).__init__()
        if not os.path.isdir(
            os.path.join(package_path, self._PACKMAN_BASENAME)
        ):
            raise ValueError(
                'This is not a packman package: {}'.format(package_path)
            )

        self._package_path = package_path
        path, name = os.path.split(package_path)
        self._path = path
        self._name = name

        self._user = getpass.getuser()

        self._lock_file = os.path.join(
            self._package_path, self._PACKMAN_BASENAME, self._LOCK_BASENAME
        )
        self._config_file = os.path.join(
            self._package_path, self._PACKMAN_BASENAME, self._CONFIG_BASENAME
        )
        self._config = {}
        self._read_config()

    def _read_config(self):
        try:
            with open(self._config_file, 'r') as fh:
                self._config = json.load(fh)
        except:
            print('>>>> TRACE:')
            traceback.print_exc()
            print('<<<< TRACE.')
            raise Exception('Cannot read package config {}'.format(self._config_file))

    def extension(self):
        return self._config.get('extension', '')

    def is_folder(self):
        try:
            return self._config['is_folder']
        except KeyError:
            return bool(self.extension())

    def _is_public_version_name(self, name):
        return name.isdigit()

    def get_version_names(self):
        version_names = []
        filenames = os.listdir(self._package_path)
        for filename in filenames:
            if not os.path.isdir(os.path.join(self._package_path, filename)):
                continue
            if not self._is_public_version_name(filename):
                continue
            version_names.append(int(filename))
        return [ str(n) for n in sorted(version_names) ]

    def has_version(self, version_name):
        return os.path.isdir(
            os.path.join(
                self._package_path, version_name
            )
        )

    def _is_working_copy_name(self, name):
        return name.startswith('w') and name[1:].isdigit()

    def get_working_copy_names(self):
        wc_names = []
        filenames = sorted(os.listdir(self._package_path))
        for filename in filenames:
            if not os.path.isdir(os.path.join(self._package_path, filename)):
                continue
            if not self._is_working_copy_name(filename):
                continue
            wc_names.append((int(filename[1:]),filename))
        wc_names.sort() 
        return [ n for i, n in wc_names ]

    def is_official_version(self, version_name):
        if not self._is_public_version_name(version_name):
            return False
        return os.path.exists(
            os.path.join(
                self._package_path, version_name, self._VERSION_OFFICIAL_BASENAME
            )
        )

    def resolve_version(self, version):
        '''
        Return the physical name of the given version:
            - None or '' points to the official version
            - a positive integer is a published version number
            - a negative interger is an offset from last published version:
                -1 = last version
                -2 = previous version
                etc...
            - a string like 'w<int>' is a working copy
            - 'w': the current working copy

        If version is not one of those, a TypeError is raised.

        If the version does not resolve to an existing one, 
        a ValueError is raised.
        '''
        if not version:
            versions = self.get_version_names()
            for version in versions:
                if self.is_official_version(version):
                    return version

        if version == 'w':
            return self.get_current_working_copy_name()

        try:
            version = int(version)
        except (ValueError, TypeError):
            if not self._is_working_copy_name(version):
                raise TypeError(
                    'Cannot resolve version {} '
                    '(must be an int, None or "w<int>")'.format(version)
                )
            wc_names = self.get_working_copy_names()
            if version not in wc_names:
                raise ValueError(
                    'Could not find working copy {}'.format(version)
                )

        if version > 0:
            version = str(version)
            if not self.has_version(str(version)):
                raise ValueError(
                    'Could not find version {}'.format(version)
                )
            return version

        else:
            versions = self.get_version_names()
            try:
                version = versions[version]
            except IndexError:
                raise IndexError(
                    'Could not fine version {}'.format(version)
                )
            return version

    def get_current_working_copy_name(self):
        wc_names = self.get_working_copy_names()
        if not wc_names:
            return None
        return wc_names[-1]

    def get_next_working_copy_name(self):
        wc_names = self.get_working_copy_names()
        if not wc_names:
            return 'w0'
        last_number = int(wc_names[-1][1:])
        return 'w{}'.format(last_number+1)

    def get_next_version_name(self):
        try:
            max_version = int(self.resolve_version(-1))
        except IndexError:
            versions = self.get_version_names()
            if not versions:
                max_version = -1
            else:
                raise
        return str(max_version+1)

    def _create_new_version(self, name, **more_info):
        p = os.path.join(self._package_path, name)
        try:
            os.makedirs(p)
        except FileExistsError:
            print('>>>> TRACE:')
            traceback.print_exc()
            print('<<<< TRACE.')
            raise ValueError(
                'Cannot create version {}: it already exists'.format(name)
            )
        info_file = os.path.join(p, self._VERSION_INFO_BASENAME)
        info = dict(
            created_on=time.time(),
            created_by=getpass.getuser(),
            owner=self._user,
        )
        info.update(more_info)
        with open(info_file, 'w') as fh:
            json.dump(info, fh)

    def get_version_info(self, version=None):
        version_name = self.resolve_version(version)
        info_file = os.path.join(
            self._package_path, version_name, self._VERSION_INFO_BASENAME
        )
        with open(info_file, 'r') as fh:
            d = json.load(fh)
        return d

    def set_official(self, version):
        version = self.resolve_version(version)
        if not self._is_public_version_name(version):
            raise ValueError('Can only set published version as official')
        for filename in os.listdir(self._package_path):
            p = os.path.join(self._package_path, filename)
            if not os.path.isdir(p):
                continue
            official_file = os.path.join(p, self._VERSION_OFFICIAL_BASENAME)
            if filename == version:
                with open(official_file, 'w') as fh:
                    json.dump(
                        dict(
                            set_by=self._user,
                            set_on=time.time(),
                        ), fh
                    )
            else:
                try:
                    os.remove(official_file)
                except OSError:
                    pass


    def basename(self):
        extension = self.extension()
        if not extension:
            return self._name
        return '{}.{}'.format(self._name, extension)
        
    def path(self, version=None):
        '''
        Returns the path of the packaged file at the official version
        or at the specified version.
        '''
        version = self.resolve_version(version)
        return os.path.join(
            self._package_path, version, self.basename()
        )

    def _acquire_lock(self):
        if os.path.exists(self._lock_file):
            raise LockedError(self)
        with open(self._lock_file, 'w') as fh:
            fh.write(self._user)

    def locker(self):
        try:
            with open(self._lock_file, 'r') as fh:
                locker = fh.read()
        except IOError:
            return None
        return locker

    def has_lock(self):
        return self.locker() == self._user

    def _release_lock(self):
        if not self.has_lock():
            raise NotLockedError(self)
        os.remove(self._lock_file)

    def edit(self, empty=False):
        self._acquire_lock()

        init_from_version=None
        if not empty:
            init_from_version = self.resolve_version(None)

        new_working_copy_name = self.get_next_working_copy_name()
        self._create_new_version(
            new_working_copy_name, 
            created_empty=empty,
            from_version=init_from_version,
        )

        dst = self.path(version=new_working_copy_name)
        if not empty:
            src = self.path(version=init_from_version)
            if self.is_folder():
                shutil.copytree(src, dst)
            else:
                shutil.copy(src, dst)
            os.chmod(dst, 0o644)
    
        return dst

    def publish(self, message, official=True):
        if not self.has_lock():
            raise NotLockedError(self)

        wc_name = self.get_current_working_copy_name()
        if wc_name is None:
            raise Exception('No working copy found to publish.')

        wc_owner = self.get_version_info(wc_name)['owner']
        if not wc_owner == self._user:
            raise Exception(
                'You ({}) own the lock but the current working copy ({}) belongs to {}. '
                'Cannot publish.'.format(self._user, wc_name, wc_owner)
            )

        new_version = self.get_next_version_name()
        self._create_new_version(
            new_version,
            from_version=wc_name,
            publish_message=message,
            official_requested=True
        )
        src = self.path(version=wc_name)
        dst = self.path(version=new_version)
        if self.is_folder():
            shutil.copytree(src, dst)
        else:
            shutil.copy(src, dst)

        os.chmod(dst, 0o444)
        if official:
            self.set_official(new_version)

        self._release_lock()

    def history(self, with_working_copies=False):
        '''
        Returns a 2d list of (version_name, version_info)
        The list is ordered from newer to older version.
        '''
        names = self.get_version_names()
        need_sorting = False
        if with_working_copies:
            wc_names = self.get_working_copy_names()
            names.extend(wc_names)
            # we need to sort by date since wc number
            # does not follow version numbers:
            need_sorting = True

        entries = []
        for name in names:
            info = self.get_version_info(name)
            info['official'] = self.is_official_version(name)
            entries.append((name, info))

        timed = []
        for name, info in entries:
            t = info['created_on']
            timed.append((t, (name, info)))
        entries = [ e for t, e in sorted(timed) ]

        return reversed(entries)

