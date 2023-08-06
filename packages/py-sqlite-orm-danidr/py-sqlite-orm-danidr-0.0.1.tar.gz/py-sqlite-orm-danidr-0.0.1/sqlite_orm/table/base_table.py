from ..field import BaseField


class SetTableClassMeta(type):

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)

        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, BaseField):
                attr_value.set_table_class(cls)


class BaseTable(metaclass=SetTableClassMeta):
    __table_name__ = None

    def __init__(self, **kwargs):
        super().__init__()
        for field_name, field_instance in self.__class__.get_fields():
            self.__setattr__(field_name, kwargs.get(field_name, field_instance.default_value))

    @property
    def column_value_map(self):
        return {
            field_name: field_instance.__class__.quoted_value(getattr(self, field_name))
            for field_name, field_instance in self.__class__.get_fields()
        }

    @staticmethod
    def value(val):
        return val

    @classmethod
    def get_field_name(cls, field_instance):
        """
        :param field_instance: инстанс поля таблицы
        :return: название поля
        """
        field_name = None
        for attr in cls.__dict__:
            if getattr(cls, attr) is field_instance:
                field_name = attr
                break

        return field_name

    @classmethod
    def get_fields(cls):
        """
        возвращает набор полей таблицы
        :return: список пар [(название колонки, инстанс колонки),..]
        """
        return [(attr, getattr(cls, attr)) for attr in cls.__dict__ if isinstance(getattr(cls, attr), BaseField)]

    @classmethod
    def get_field_by_name(cls, field_name):
        return getattr(cls, field_name)

    @classmethod
    def get_foreign_field_by_table(cls, table):
        field_foreign_key = None
        for _, field in cls.get_fields():
            if field.foreign_key:
                if field.foreign_key.table_class is table:
                    field_foreign_key = field
                    break

        return field_foreign_key
