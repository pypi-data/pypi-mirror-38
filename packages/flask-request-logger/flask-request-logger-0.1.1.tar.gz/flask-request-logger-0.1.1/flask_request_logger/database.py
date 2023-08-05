import datetime

from sqlalchemy.ext.declarative import as_declarative

from flask_sqlalchemy import DefaultMeta as ModelDefaultMeta


@as_declarative(name='Model', metaclass=ModelDefaultMeta)
class Model(object):
    """
        Use this class has the base for your models, it will define your table names automatically
        MyModel will be called my_model on the database.
        ::
            from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, Date
            from flask_appbuilder import Model
            class MyModel(Model):
                id = Column(Integer, primary_key=True)
                name = Column(String(50), unique = True, nullable=False)
    """

    __table_args__ = {'extend_existing': True}

    def to_json(self):
        result = dict()
        for key in self.__mapper__.c.keys():
            col = getattr(self, key)
            if isinstance(col, datetime.datetime) or isinstance(col, datetime.date):
                col = col.isoformat()
            result[key] = col
        return result


Base = Model
