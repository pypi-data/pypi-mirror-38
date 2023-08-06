

class LockedError(Exception):

    def __init__(self, package):
        self.package = package
        self.by = package.locker()
        super(LockedError, self).__init__(
            'Package already locked by {}'.format(self.by)
        )

class NotLockedError(Exception):

    def __init__(self, package):
        self.package = package
        self.by = package.locker()
        if self.by is None:
            msg = 'Package is not locked'
        else:
            msg = 'Package is locked by {}, not by you'.format(self.by)
        super(NotLockedError, self).__init__(msg)
