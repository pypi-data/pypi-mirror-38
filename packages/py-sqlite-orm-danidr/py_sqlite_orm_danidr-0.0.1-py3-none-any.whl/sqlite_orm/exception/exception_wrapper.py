import logging


def reraise(tp, value, tb=None):
    if value.__traceback__ is not tb:
        logging.exception("Exception: ".format(value.with_traceback(tb)))
        raise value.with_traceback(tb)
    logging.exception("Exception: ".format(value))
    raise value


class SQLiteORMException(Exception):
    pass


class ImproperlyConfigured(SQLiteORMException):
    pass


class DatabaseError(SQLiteORMException):
    pass


class IntegrityError(DatabaseError):
    pass


class OperationalError(DatabaseError):
    pass


class ExceptionWrapper(object):
    __slots__ = ('exceptions',)

    def __init__(self, exceptions):
        self.exceptions = exceptions

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None and exc_type.__name__ in self.exceptions:
            new_type = self.exceptions[exc_type.__name__]
            exc_args = exc_value.args
            reraise(new_type, new_type(*exc_args), traceback)
