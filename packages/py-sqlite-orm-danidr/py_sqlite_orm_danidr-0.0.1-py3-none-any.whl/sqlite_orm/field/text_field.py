from .base_field import BaseField


class TextField(BaseField):
    __type_name__ = 'TEXT'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def value(val):
        if val is not None:
            val = str(val)
        return val

    @classmethod
    def quoted_value(cls, val):
        return 'NULL' if val is None else repr(cls.value(val))
