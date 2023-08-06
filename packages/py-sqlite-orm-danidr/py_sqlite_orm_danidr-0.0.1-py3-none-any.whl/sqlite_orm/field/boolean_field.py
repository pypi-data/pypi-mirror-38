from .base_field import BaseField


class BooleanField(BaseField):
    __type_name__ = 'BOOLEAN'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def value(val):
        if val is not None:
            val = 1 if val else 0
        return val
