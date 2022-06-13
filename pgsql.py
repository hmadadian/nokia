from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect
from db_structure import DbStructure
import copy
import env


class SqlInteraction:
    def __init__(self, db_url, table_name, test=False):
        DATABASE_URL = db_url
        self.__engine = create_engine(DATABASE_URL, poolclass=NullPool)
        self.__structure = DbStructure()
        base = self.__structure.return_base()
        insp = inspect(self.__engine)
        if not insp.has_table(table_name):
            base.metadata.create_all(self.__engine)
        self.__session = Session(self.__engine)
        self.test = test

    def set_in_db(self, **kwargs):
        fl = self.__structure.FoodList(**kwargs)
        self.__session.add(fl)
        self.__session.commit()
        return {"pod_name": env.HOSTNAME, "status": "# of inserted rows = {}".format(1)}

    def get_from_db(self, **kwargs):
        fl = self.__session.query(self.__structure.FoodList).filter(
                *[getattr(self.__structure.FoodList, k) == v for k, v in kwargs.items()]
        ).all()
        new_fl = copy.deepcopy(fl)
        self.__session.commit()
        return new_fl if self.test else self.__db_to_dict(new_fl)

    def update_row(self, information_dict):
        fl = self.__session.query(self.__structure.FoodList).filter(
            *[getattr(self.__structure.FoodList, k) == v for k, v in information_dict["filter"].items()]
        ).update(information_dict["update_params"])
        self.__session.commit()
        return {"pod_name": env.HOSTNAME, "status": "# of updated rows = {}".format(fl)}

    def delete_row(self, **kwargs):
        fl = self.__session.query(self.__structure.FoodList).filter(
            *[getattr(self.__structure.FoodList, k) == v for k, v in kwargs.items()]
        ).delete()
        self.__session.commit()
        return {"pod_name": env.HOSTNAME, "status": "# of deleted rows = {}".format(fl)}

    def __get_col(self):
        return self.__structure.FoodList.__table__.columns.keys()

    def __db_to_dict(self, obj):
        result = list()
        cols = self.__get_col()
        for food in obj:
            food_list = dict()
            for col in cols:
                food_list[col] = getattr(food, col)
            result.append(food_list)
        return result
