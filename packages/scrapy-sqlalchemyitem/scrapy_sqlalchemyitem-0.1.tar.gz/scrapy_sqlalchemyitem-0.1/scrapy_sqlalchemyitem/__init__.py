#!/usr/bin/env python
# -*- coding: utf-8 -*-

from six import with_metaclass
from scrapy.item import Field, Item, ItemMeta
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.sql.schema import Table

class SqlalchemyItemMeta(ItemMeta):

    def __new__(mcs, class_name, bases, attrs):
        cls = super(SqlalchemyItemMeta, mcs).__new__(mcs, class_name, bases, attrs)
        if cls.sqlalchemy_model is not None:
            cls._model_fields = []
            if isinstance(cls.sqlalchemy_model,DeclarativeMeta):
                columns = cls.sqlalchemy_model.__table__.columns
            elif isinstance(cls.sqlalchemy_model,Table):
                columns = cls.sqlalchemy_model.columns
            else:
                raise TypeError('类型错误，仅支持 “DeclarativeMeta”，“Table” 类型')
            for model_field in columns:
                    if model_field.name not in cls.fields:
                        cls.fields[model_field.name] = Field()
        return cls
# with_metaclass 用meta创建base
class SqlalchemyItem(with_metaclass(SqlalchemyItemMeta, Item)):
    sqlalchemy_model = None