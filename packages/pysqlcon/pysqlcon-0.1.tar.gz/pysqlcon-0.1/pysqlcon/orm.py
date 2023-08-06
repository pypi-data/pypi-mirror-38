"""
@author: Kudzai Tsapo (kudzai@charteredsys.com)

Description: 
--------------
This file contains the model classes for the Object Relational Mapper (Custom made)
"""
from datetime import datetime

class Meta(type):
    def __new__(cls, name, bases, attrs):
        new_type = type(name, bases, attrs)
        for field_name, field in attrs.items():
            field._name = field_name

        attrs['_data'] = dict.fromkeys(attrs.keys())
        return new_type

class Relation(Field):
    def __init__(self, rel_model_class, reverse_name=None):
        self._model_class = rel_model_class
        self._reverse_name = reverse_name

    def __set__(self, obj, value):
        if not isinstance(value, self._model_class):
            raise TypeError(obj, self._name, self._model_class, value)
        
        super().__init__(obj, value)

class InverseRelation:
    def __init__(self, origin_model, field_name):
        self._origin_model, self._field_name = origin_model, field_name

    def __get__(self, obj, type=None):
        return self._origin_model.S.filter(self._field_name=obj)

class RelationMeta(type):
    def __new__(cls, name, bases, attrs):
        new_type = type(name, bases, attrs)
        for field_name, field in attrs.items():
            if isinstance(field, Relation):
                setattr(field._model_class , self._reverse_name, \
                    InverseRelation (new_type, field_name))

        return new_type

class Field:
    def __set__(self, obj, value):
        obj._data[self._name] = value

    def __get__(self, obj, type=None):
        return obj._data[self._name]

class FieldTypeValidator(Field):
    def __set__(self, obj, value, class_type):
        if not isinstance(value, class_type):
            raise TypeError(obj, self._name, class_type, value)
        super().__set__(obj, value)

class IntField(FieldTypeValidator):
    def __set__(self, obj, value):
        super().__set__(obj, value, int)

class FloatField(FieldTypeValidator):
    def __set__(self, obj, value):
        super().__set__(obj, value, float)

class StringField(FieldTypeValidator):
    def __set__(self, obj, value):
        super().__set__(obj, value, str)

class BooleanField(FieldTypeValidator):
    def __set__(self, obj, value):
        super().__set__(obj, value, bool)

class DatetimeField(FieldTypeValidator):
    def __set__(self, obj, value):
        super().__set__(obj, value, datetime)

class Model(metaclass=Meta):
    pass


