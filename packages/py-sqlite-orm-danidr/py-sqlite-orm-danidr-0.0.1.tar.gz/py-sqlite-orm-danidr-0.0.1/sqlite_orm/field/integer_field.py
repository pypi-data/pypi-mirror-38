from .base_field import BaseField


class IntegerField(BaseField):
    __type_name__ = 'INTEGER'

    def __init__(self, auto_increment=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auto_increment = auto_increment
