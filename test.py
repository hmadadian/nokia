from pydantic import BaseModel
from http_2_json import Http2Json
from pydantic import ValidationError

# import requests
#
# params = {
#     'name': 'Geymeh',
#     'price': '500000',
#     'ingredients': 'split peas, meat',
#     'spicy': 'true',
#     'vegan': 'false',
#     'gluten_free': 'true',
#     'description': 'iranian food',
#     'kcal': '8000',
# }
#
# file = {
#     'file': open('C:\\Users\\Hamed\\Desktop\\Immigration\\hm2-2.jpg', 'rb'),
# }
#
# response = requests.post('http://127.0.0.1:8000/create/', params=params, files=file)
#
# print(response.text)




from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import pytest
import os
from pgsql import SqlInteraction

POSTGRESQL_ADDRESS = os.getenv('POSTGRESQL_ADDRESS')
POSTGRESQL_USERNAME = os.getenv('POSTGRESQL_USERNAME')
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
POSTGRESQL_DATABASE_NAME = os.getenv('POSTGRESQL_DATABASE_NAME')
TABLE_NAME = os.getenv('POSTGRESQL_TABLE_NAME')


@pytest.fixture(scope='session')
def db_engine():
    """yields a SQLAlchemy engine which is suppressed after the test session"""
    db_url = 'postgresql://' + POSTGRESQL_USERNAME + ':' + POSTGRESQL_PASSWORD + '@' + POSTGRESQL_ADDRESS + \
             '/' + POSTGRESQL_DATABASE_NAME
    engine_ = create_engine(db_url, echo=True)
    yield engine_
    engine_.dispose()


@pytest.fixture(scope='session')
def db_session_factory(db_engine):
    """returns a SQLAlchemy scoped session factory"""
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope='function')
def db_session(db_session_factory):
    """yields a SQLAlchemy connection which is rollbacked after the test"""
    session_ = db_session_factory()

    yield session_

    session_.rollback()
    session_.close()


def __db_to_dict(obj, cols):
    result = list()
    for food in obj:
        food_list = dict()
        for col in cols:
            food_list[col] = getattr(food, col)
        result.append(food_list)
    return result


def test_something(db_session):
    DATABASE_URL = 'postgresql://' + POSTGRESQL_USERNAME + ':' + POSTGRESQL_PASSWORD + '@' + POSTGRESQL_ADDRESS + \
                   '/' + POSTGRESQL_DATABASE_NAME
    sql = SqlInteraction(DATABASE_URL)

    test_data = {"name": "PÁCOLT NYERS HÚS", "price": 1850, "ingredients": "chicken, herbs", "spicy": True,
                 "vegan": False, "gluten_free": True, "description": "Marinated chicken breast slices with herbs",
                 "kcal": 5000,
                 "pic_uri": "https://www.teletal.hu/etel_kepek/gr_zoldfuszeres_fokhagymas_csirkemell_960x.jpg"}

    sql.set_in_db(**test_data)
    cols = sql.FoodList.__table__.columns.keys()
    # test1 = db_session.query(sql.FoodList).filter_by(sql.FoodList.name == "PÁCOLT NYERS HÚS").all()
    test1 = db_session.query(sql.FoodList).with_entities(*[i for i in cols if i != "pid"]).filter(sql.FoodList.name == "PÁCOLT NYERS HÚS").first()
    test_data_class = sql.FoodList(**test_data)
    print(".........................")
    # print(__db_to_dict(test1, cols))
    print(".........................")
    # print(__db_to_dict(test_data_class, cols))
    print(".........................")
    print(test1.__dict__)
    print(".........................")
    print(test_data_class.__dict__)
    print(".........................")
    assert test1 == test_data_class
