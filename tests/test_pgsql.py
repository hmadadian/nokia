from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pgsql import SqlInteraction
from db_structure import DbStructure
import pytest
import env

sql = SqlInteraction(env.DATABASE_URL, env.TABLE_NAME, True)
structure = DbStructure()
Base = structure.return_base()


@pytest.fixture(scope="session")
def engine():
    return create_engine(env.DATABASE_URL)


@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


def set_in_db_testing(dbs, test_data):
    sql.set_in_db(**test_data)
    test = dbs.query(structure.FoodList).filter(*[getattr(structure.FoodList, k) == v for k, v in test_data.items()])\
        .first()
    test = test.__dict__.copy()
    del test["_sa_instance_state"]
    del test["pid"]
    return test


def get_from_db_testing(test_data):
    test = sql.get_from_db(**test_data)
    test = test[0].__dict__.copy()
    del test["_sa_instance_state"]
    del test["pid"]
    return test


def update_row_db_testing(dbs, test_data, filter_data: dict = None):
    sql.update_row(test_data)
    if filter_data:
        fd = [getattr(structure.FoodList, k) == v for k, v in filter_data.items()]
    else:
        fd = [getattr(structure.FoodList, k) == v for k, v in test_data["update_params"].items()]
    test = dbs.query(structure.FoodList).filter(*fd).first()
    test = test.__dict__.copy()
    del test["_sa_instance_state"]
    del test["pid"]
    return test


def delete_row_db_testing(dbs, test_data, filter_data: dict = None):
    sql.delete_row(**test_data)
    if filter_data:
        fd = [getattr(structure.FoodList, k) == v for k, v in filter_data.items()]
    else:
        fd = [getattr(structure.FoodList, k) == v for k, v in test_data.items()]
    test = dbs.query(structure.FoodList).filter(*fd).first()
    if test:
        test = test.__dict__.copy()
        del test["_sa_instance_state"]
        del test["pid"]
    return test


def test_set_in_db(db_session):
    test_data1 = {"name": "PÁCOLT NYERS HÚS", "price": 1850, "ingredients": "chicken, herbs", "spicy": True,
                  "vegan": False, "gluten_free": True, "description": "Marinated chicken breast slices with herbs",
                  "kcal": 5000,
                  "pic_uri": "https://www.teletal.hu/etel_kepek/gr_zoldfuszeres_fokhagymas_csirkemell_960x.jpg"}

    test_data2 = {"name": "LEVESEK", "price": 575, "ingredients": "Potato, sour cream", "spicy": False,
                  "vegan": True, "gluten_free": False, "description": "Potato soup with sour cream and parsley",
                  "kcal": 400,
                  "pic_uri": "https://www.teletal.hu/etel_kepek/tejfolos_petrezselymes_burgonyaleves_960x.jpg"}

    test_results1 = set_in_db_testing(db_session, test_data1)
    test_results2 = set_in_db_testing(db_session, test_data2)

    assert test_results1 == test_data1
    assert test_results2 == test_data2


def test_get_from_db(db_session):
    test_data1 = {"name": "PÁCOLT NYERS HÚS"}
    result_data1 = {"name": "PÁCOLT NYERS HÚS", "price": 1850, "ingredients": "chicken, herbs", "spicy": True,
                    "vegan": False, "gluten_free": True, "description": "Marinated chicken breast slices with herbs",
                    "kcal": 5000,
                    "pic_uri": "https://www.teletal.hu/etel_kepek/gr_zoldfuszeres_fokhagymas_csirkemell_960x.jpg"}

    test_data2 = {"name": "LEVESEK"}
    result_data2 = {"name": "LEVESEK", "price": 575, "ingredients": "Potato, sour cream", "spicy": False,
                    "vegan": True, "gluten_free": False, "description": "Potato soup with sour cream and parsley",
                    "kcal": 400,
                    "pic_uri": "https://www.teletal.hu/etel_kepek/tejfolos_petrezselymes_burgonyaleves_960x.jpg"}

    test_results1 = get_from_db_testing(test_data1)
    test_results2 = get_from_db_testing(test_data2)

    assert test_results1 == result_data1
    assert test_results2 == result_data2


def test_update_row(db_session):
    test_data_filter1 = {"name": "PÁCOLT NYERS HÚS"}
    test_data_params1 = {"name": "Húsos levesek"}
    test_information1 = {"filter": test_data_filter1, "update_params": test_data_params1}
    result_data1 = {"name": "Húsos levesek", "price": 1850, "ingredients": "chicken, herbs", "spicy": True,
                    "vegan": False, "gluten_free": True, "description": "Marinated chicken breast slices with herbs",
                    "kcal": 5000,
                    "pic_uri": "https://www.teletal.hu/etel_kepek/gr_zoldfuszeres_fokhagymas_csirkemell_960x.jpg"}

    test_data_filter2 = {"name": "LEVESEK", "price": 575}
    test_data_params2 = {"ingredients": "changed ingredients", "description": "changed description"}
    test_information2 = {"filter": test_data_filter2, "update_params": test_data_params2}
    result_data2 = {"name": "LEVESEK", "price": 575, "ingredients": "changed ingredients", "spicy": False,
                    "vegan": True, "gluten_free": False, "description": "changed description",
                    "kcal": 400,
                    "pic_uri": "https://www.teletal.hu/etel_kepek/tejfolos_petrezselymes_burgonyaleves_960x.jpg"}

    test_results1 = update_row_db_testing(db_session, test_information1)
    test_results2 = update_row_db_testing(db_session, test_information2, test_data_filter2)

    assert test_results1 == result_data1
    assert test_results2 == result_data2


def test_delete_row(db_session):
    test_data_filter1 = {"name": "Húsos levesek"}
    test_data_filter2 = {"name": "LEVESEK", "price": 576}
    result_data2 = {"name": "LEVESEK", "price": 575, "ingredients": "changed ingredients", "spicy": False,
                    "vegan": True, "gluten_free": False, "description": "changed description",
                    "kcal": 400,
                    "pic_uri": "https://www.teletal.hu/etel_kepek/tejfolos_petrezselymes_burgonyaleves_960x.jpg"}

    test_results1 = delete_row_db_testing(db_session, test_data_filter1)
    test_results2 = delete_row_db_testing(db_session, test_data_filter2, {"name": "LEVESEK", "price": 575})

    assert test_results1 is None
    assert test_results2 == result_data2

