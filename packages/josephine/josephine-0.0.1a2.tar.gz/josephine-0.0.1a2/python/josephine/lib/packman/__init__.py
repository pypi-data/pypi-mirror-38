'''

josephine.lib.packman: s simple package versioning system.

A package is a folder containing a file and all previous versions of it.

A user can edit the file only if the package is not locked.
Editing the file locks the package.
The editing is done in a working copy version.

Once edit is done the working copy can be published.
Publishing a working copy unlocks the package.


Synopsys:
    # Create a new package:
    package = packman.Package.create(dirname, package_name, extension)

    # Create a Package instance to manage an existing package:
    package = vers.Package(package_path)

    # Get paths from the package
    filename = package.path() # get the official version path
    prev_version = package.path(version=-2) # get specific version path

    # Edit a file to get write permissions:
    filename = package.edit()

    # Now the package is locked:
    locked = package.is_locked()

    # If the package is locked, you can't edit it:
    try:
        filename = package.edit()
    except vers.LockedError, err:
        print('Already locked by '+err.by)

    # Publish your edits to release the lock and update the official version:
    filename = package.publish()

'''
from .package import Package
from .exceptions import *