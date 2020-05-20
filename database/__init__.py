# !/usr/bin/python
# -*- encoding: utf-8 -*-

"""
@author: fengli
@contact: fenglilee@icloud.com
@file: __init__.py
@time: 2019/11/8 5:55 下午
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class AttrModel(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True, comment='主键')


class MethodModel(db.Model):

    __abstract__ = True

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
                db.session.refresh(self)
                return self
            except Exception as e:
                db.session.rollback()
                raise e

    @classmethod
    def create(cls, commit=True, **kwargs):
        instance = cls(**kwargs)
        return instance.save(commit=commit)

    @classmethod
    def create_if_not_exist(cls, commit=True, **kwargs):
        ins = cls.find_one(**kwargs)
        if ins is not None:
            return ins
        return cls.create(commit=commit, **kwargs)

    @classmethod
    def find_one(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def find_all(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save(commit=commit)

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()

    @classmethod
    def delete_by(cls, **kwargs):
        cls.query.filter_by(**kwargs).delete()
        return db.session.commit()

    def to_dict(self):
        """ not support column name starts with '_'
        """
        return dict([(k, getattr(self, k)) for k in self.__dict__.keys() if not k.startswith("_")])


if __name__ == '__main__':
    pass
