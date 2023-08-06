'''
    
    Quick and Dirty Testing.
    Run w/ something like:
        python -m josephine.lib.packman.test
    (you will need to create the folder D:\DATA_STORE\TESTS)

'''
from __future__ import print_function

import sys
import os
import time

def import_packman():
    try:
        import josephine.lib.packman

    except ImportError:
        path = os.path.normpath(
            os.path.join(
                __file__,
                '..', '..'
            )
        )
        if path not in sys.path:
            sys.path.append(path)
        import packman
        return packman

    else:
        return josephine.lib.packman


def test():
    root_path = r'D:\DATA_STORE\TESTS'
    if not os.path.exists(root_path):
        raise Exception('root path doesnt exists {}'.format(root_path))

    tests_path = root_path+'/PACKMAN'
    if os.path.exists(tests_path):
        os.rename(tests_path, tests_path+'.{}'.format(time.time()))

    pm = import_packman()  

    print('Creating Package Tests/TestPack')
    new_pack = pm.Package.create_package(tests_path+'/Tests', 'TestPack', 'txt')

    print('Assert official version is 0')
    p = new_pack.path()
    assert(os.path.basename(os.path.dirname(p)) == '0')

    print('Loading Package')
    pack = pm.Package(tests_path+'/Tests/TestPack')

    print('Assert official path is the same')
    print(new_pack.path())
    print(pack.path())
    assert(os.path.normpath(pack.path()) == os.path.normpath(new_pack.path()))

    print('Assert official version not writable')
    try:
        with open(pack.path(), 'w') as fh:
            fh.write('FUUUUCK IIIIIIT !!!')
    except IOError:
        pass
    else:
        raise Exception('Did not prevent writing on official version !')

    print('Editing the package (empty)')
    edit_path = pack.edit(empty=True)

    print('Assert file does not exists')
    assert(not os.path.exists(edit_path))

    print('Assert has lock')
    assert(pack.has_lock())

    print('Assert not editable by another user')
    pack2 = pm.Package(tests_path+'/Tests/TestPack')
    pack2._user = 'SomeoneElse'
    assert(pack2.path() == pack.path())

    try:
        pack2.edit()
    except pm.LockedError:
        pass
    else:
        raise AssertionError('Did not raise LockedError')

    print('Editing file content')
    edit_content = 'This file has been edited.'
    with open(edit_path, 'w') as fh:
        fh.write(edit_content)

    print('Assert SomeoneElse cannot publish')
    try:
        pack2.publish('just testing')
    except pm.NotLockedError:
        pass
    else:
        raise AssertionError('Did not raise NotLockedError')

    print('Publishing')
    pub_message = 'Publishing...'
    pack.publish(pub_message, official=True)

    print('Assert official version has our content')
    path = pack.path()
    with open(path, 'r') as fh:
        content = fh.read()
    assert(content == edit_content)

    print('Assert publish message is ours')
    version_info = pack.get_version_info()
    assert(version_info['publish_message'] == pub_message)

    print('Assert publish owner is us')
    assert(version_info['owner'] == pack._user)

    print('Edit again, but with initial content')
    path = pack.edit(empty=False)

    print('Assert editable content is initializes with last published content')
    with open(path, 'r') as fh:
        content = fh.read()
    assert(content == edit_content)

    print('Publish new content without making it official')
    another_content = 'This is another content.'
    with open(path, 'w') as fh:
        fh.write(another_content)
    pack.publish('testing publish w/o making it official', official=False)

    print('Assert official version is not the last one')
    assert(pack.resolve_version(None) != pack.resolve_version('-1'))

    print('Assert official content is still the same')
    with open(pack.path(), 'r') as fh:
        content = fh.read()
    assert(content == edit_content)

    print('Make last publish official')
    pack.set_official(-1)
    print('Assert official content is updated')
    with open(pack.path(), 'r') as fh:
        content = fh.read()
    assert(content == another_content)

    print('Inspecting History')
    history = pack.history(True)
    for version, info in history:
        is_official = info.get('official', False)
        owner = info['owner']
        from_version = info['from_version']
        msg = info.get('publish_message', '')
        print('   {}{} [{}] (from {}) {}'.format(
                is_official and '*' or ' ', version, owner, from_version, msg
            )
        )

if __name__ == '__main__':
    test()


