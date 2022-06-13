from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import pytest
from db_structure import DbStructure
import env
from main import app

client = TestClient(app)
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


def get_token():
    response = client.post("/user/login", params={"username": "nokia", "password": "nokiaisbest"})
    headers = {"Authorization": "Bearer {}".format(response.json()["token"])}
    return headers


# Test CRUD + User authentication With normal Query

def test_login_query():
    response = client.post("/user/login", params={"username": "nokia", "password": "nokiaisbest"})
    assert response.status_code == 200
    assert response.json()["is_ok"] is True
    assert response.json()["token"] is not None


def test_signup_query():
    headers = get_token()
    response1 = client.post("/user/signup", headers=headers, params={"username": "hamed", "password": "hamed"})
    assert response1.status_code == 200
    assert response1.json()["is_ok"] is True
    response2 = client.post("/user/signup", headers=headers, params={"username": "hamed", "password": "hamed"})
    assert response2.status_code == 200
    assert response2.json()["is_ok"] is False


def test_create_query(db_session):
    headers = get_token()
    params = {"name": "PÁCOLT NYERS HÚS", "price": 1850, "ingredients": "chicken, herbs", "spicy": True,
              "vegan": False, "gluten_free": True, "description": "Marinated chicken breast slices with herbs",
              "kcal": 5000}
    response = client.post("/create", headers=headers, params=params)
    test = db_session.query(structure.FoodList).filter(
        *[getattr(structure.FoodList, k) == v for k, v in params.items()]).first()
    test = test.__dict__.copy()
    del test["_sa_instance_state"]
    del test["pid"]
    del test["pic_uri"]
    assert response.status_code == 200
    assert test == params


def test_read_query(db_session):
    headers = get_token()
    params = {"name": "PÁCOLT NYERS HÚS"}
    response = client.post("/read", headers=headers, params=params)
    result = [{'pid': 1, "name": "PÁCOLT NYERS HÚS", "price": 1850, "ingredients": "chicken, herbs", "spicy": True,
               "vegan": False, "gluten_free": True, "description": "Marinated chicken breast slices with herbs",
               "kcal": 5000, "pic_uri": None}]
    assert response.status_code == 200
    assert response.json()["result"] == result


def test_update_query(db_session):
    headers = get_token()
    result = {"name": "PÁCOLT NYERS HÚS", "price": 1850, "ingredients": "ingredients changed", "spicy": True,
              "vegan": False, "gluten_free": True, "description": "description changed",
              "kcal": 5000, "pic_uri": None}
    response = client.post("/update/filter[name]=PÁCOLT NYERS HÚS&update_params[description]=description changed&" +
                           "update_params[ingredients]=ingredients changed", headers=headers)
    test = db_session.query(structure.FoodList).filter(structure.FoodList.name == "PÁCOLT NYERS HÚS").first()
    test = test.__dict__.copy()
    del test["_sa_instance_state"]
    del test["pid"]
    assert response.status_code == 200
    assert test == result


def test_delete_query(db_session):
    headers = get_token()
    params1 = {"name": "PÁCOLT NYERS HÚS", "price": 576}
    response1 = client.post("/delete", headers=headers, params=params1)
    result = {"name": "PÁCOLT NYERS HÚS", "price": 1850, "ingredients": "ingredients changed", "spicy": True,
              "vegan": False, "gluten_free": True, "description": "description changed",
              "kcal": 5000, "pic_uri": None}
    test1 = db_session.query(structure.FoodList).filter(structure.FoodList.name == "PÁCOLT NYERS HÚS").first()
    test1 = test1.__dict__.copy()
    del test1["_sa_instance_state"]
    del test1["pid"]
    assert response1.status_code == 200
    assert test1 == result

    params2 = {"name": "PÁCOLT NYERS HÚS"}
    response2 = client.post("/delete", headers=headers, params=params2)
    test2 = db_session.query(structure.FoodList).filter(structure.FoodList.name == "PÁCOLT NYERS HÚS").first()
    assert response2.status_code == 200
    assert test2 is None


# Test CRUD + User authentication With json

def test_login_json():
    response = client.post("/user/login/json/", json={"username": "nokia", "password": "nokiaisbest"})
    assert response.status_code == 200
    assert response.json()["is_ok"] is True
    assert response.json()["token"] is not None


def test_signup_json():
    headers = get_token()
    response1 = client.post("/user/signup/json/", headers=headers, json={"username": "Bence", "password": "Bence"})
    assert response1.status_code == 200
    assert response1.json()["is_ok"] is True
    response2 = client.post("/user/signup/json/", headers=headers, json={"username": "Bence", "password": "Bence"})
    assert response2.status_code == 200
    assert response2.json()["is_ok"] is False


def test_create_json(db_session):
    headers = get_token()
    json = {"name": "LEVESEK", "price": 575, "ingredients": "Potato, sour cream", "spicy": False,
            "vegan": True, "gluten_free": False, "description": "Potato soup with sour cream and parsley",
            "kcal": 400}
    response = client.post("/create/json/", headers=headers, json=json)
    test = db_session.query(structure.FoodList).filter(
        *[getattr(structure.FoodList, k) == v for k, v in json.items()]).first()
    test = test.__dict__.copy()
    del test["_sa_instance_state"]
    del test["pid"]
    del test["pic_uri"]
    assert response.status_code == 200
    assert test == json


def test_read_json(db_session):
    headers = get_token()
    json = {"name": "LEVESEK"}
    response = client.post("/read/json/", headers=headers, json=json)
    result = [{'pid': 2, "name": "LEVESEK", "price": 575, "ingredients": "Potato, sour cream", "spicy": False,
               "vegan": True, "gluten_free": False, "description": "Potato soup with sour cream and parsley",
               "kcal": 400, "pic_uri": None}]
    assert response.status_code == 200
    assert response.json()["result"] == result


def test_update_json(db_session):
    headers = get_token()
    json = {"filter": {"name": "LEVESEK"}, "update_params": {"price": 1000, "spicy": True}}
    result = {"name": "LEVESEK", "price": 1000, "ingredients": "Potato, sour cream", "spicy": True,
              "vegan": True, "gluten_free": False, "description": "Potato soup with sour cream and parsley",
              "kcal": 400, "pic_uri": None}
    response = client.post("/update/json/", headers=headers, json=json)
    test = db_session.query(structure.FoodList).filter(structure.FoodList.name == "LEVESEK").first()
    test = test.__dict__.copy()
    del test["_sa_instance_state"]
    del test["pid"]
    assert response.status_code == 200
    assert test == result


def test_delete_json(db_session):
    headers = get_token()
    json1 = {"name": "LEVESEK", "price": 576}
    response1 = client.post("/delete/json/", headers=headers, json=json1)
    result = {"name": "LEVESEK", "price": 1000, "ingredients": "Potato, sour cream", "spicy": True,
              "vegan": True, "gluten_free": False, "description": "Potato soup with sour cream and parsley",
              "kcal": 400, "pic_uri": None}
    test1 = db_session.query(structure.FoodList).filter(structure.FoodList.name == "LEVESEK").first()
    test1 = test1.__dict__.copy()
    del test1["_sa_instance_state"]
    del test1["pid"]
    assert response1.status_code == 200
    assert test1 == result

    json2 = {"name": "LEVESEK"}
    response2 = client.post("/delete/json/", headers=headers, json=json2)
    test2 = db_session.query(structure.FoodList).filter(structure.FoodList.name == "LEVESEK").first()
    assert response2.status_code == 200
    assert test2 is None
