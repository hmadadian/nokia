from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends
from pydantic import ValidationError
from typing import Optional
import uvicorn
import json

from http_2_json import Http2Json
from pgsql import SqlInteraction
from authentication import *
from validator import *
import env

# from fastapi import UploadFile
# from pathlib import Path
# import string
# import random
# import shutil
# import os

# Connect to sql class with Database URL and table name
sql = SqlInteraction(env.DATABASE_URL, env.TABLE_NAME)
# Authentication
auth = UserManager()

# execute fastapi as app and run it as middleware.
app = FastAPI()
origins = ["*"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

# CRUD + User authentication With normal Query


# function for checking duplicated rows
def check_duplication(data):
    checking_data = data.copy()
    if len(sql.get_from_db(**checking_data)) != 0:
        return True
    return False


# route for sending post request for create new user with normal http query *Login is Required*
@app.post("/user/signup", dependencies=[Depends(JWTBearer())], tags=["User, Query Method"])
def create_user(username: str, password: str):
    return auth.add_user(UserSchema(**{"username": username, "password": password}))


# route for sending login request and get tokens with normal http query
@app.post("/user/login", tags=["User, Query Method"])
def user_login(username: str, password: str):
    return auth.check_user(UserSchema(**{"username": username, "password": password}))


# route for sending post request for create a new row with normal http query *Login is Required*
@app.post("/create", dependencies=[Depends(JWTBearer())], tags=["CRUD, Query Method"])
async def data_entry(name: str, price: int, ingredients: str, spicy: bool, vegan: bool, gluten_free: bool,
                     description: str, kcal: int):
    # file_url = None
    # if file:
    #     random_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
    #     file_name = random_name + Path(file.filename).suffix
    #     directory = env.WEBSERVER_DIR + os.sep + file_name
    #     file_url = env.WEBSERVER_URL + "/" + file_name
    #     with open(directory, "wb") as buffer:
    #         shutil.copyfileobj(file.file, buffer)

    data = {"name": name, "price": price, "ingredients": ingredients, "spicy": spicy, "vegan": vegan,
            "gluten_free": gluten_free, "description": description, "kcal": kcal}

    if check_duplication(data):
        return {"pod_name": env.HOSTNAME, "status": "# of inserted rows = {}".format(0)}
    return sql.set_in_db(**data)


# route for sending post request for read row/rows with normal http query *Login is Required*
@app.post("/read", dependencies=[Depends(JWTBearer())], tags=["CRUD, Query Method"])
def data_load(name: str | None = None, price: int | None = None, ingredients: str | None = None,
              spicy: bool | None = None, vegan: bool | None = None, gluten_free: bool | None = None,
              description: str | None = None, kcal: int | None = None):
    data = {}
    if name:
        data.update({"name": name})
    if price:
        data.update({"price": price})
    if ingredients:
        data.update({"ingredients": ingredients})
    if spicy:
        data.update({"spicy": spicy})
    if vegan:
        data.update({"vegan": vegan})
    if gluten_free:
        data.update({"gluten_free": gluten_free})
    if description:
        data.update({"description": description})
    if kcal:
        data.update({"kcal": kcal})

    return {"pod_name": env.HOSTNAME, "result": sql.get_from_db(**data)}


# route for sending post request for update row/rows with normal http query *Login is Required*
@app.post("/update/{items}", dependencies=[Depends(JWTBearer())], tags=["CRUD, Query Method"])
def data_update(items: Optional[str] = None):
    query = Http2Json()
    item_dict = query.convert(items)
    try:
        validated_items = JsonBody(**item_dict).dict(exclude_none=True)
        if len(validated_items["filter"]) == 0:
            return {"pod_name": env.HOSTNAME, "is_ok": False, "details": "at least one filter should be used"}
        if len(validated_items["update_params"]) == 0:
            return {"pod_name": env.HOSTNAME, "is_ok": False, "details": "at least one update_params should be used"}
        return sql.update_row(validated_items)
    except ValidationError as e:
        return JSONResponse(json.loads(e.json()))


# route for sending post request for delete row/rows with normal http query *Login is Required*
@app.post("/delete", dependencies=[Depends(JWTBearer())], tags=["CRUD, Query Method"])
def delete_item(name: str | None = None, price: int | None = None, ingredients: str | None = None,
                spicy: bool | None = None, vegan: bool | None = None, gluten_free: bool | None = None,
                description: str | None = None, kcal: int | None = None):
    data = {}
    if name:
        data.update({"name": name})
    if price:
        data.update({"price": price})
    if ingredients:
        data.update({"ingredients": ingredients})
    if spicy:
        data.update({"spicy": spicy})
    if vegan:
        data.update({"vegan": vegan})
    if gluten_free:
        data.update({"gluten_free": gluten_free})
    if description:
        data.update({"description": description})
    if kcal:
        data.update({"kcal": kcal})
    if len(data) == 0:
        return {"pod_name": env.HOSTNAME, "is_ok": False, "details": "There should be param to remove"}
    return sql.delete_row(**data)


# CRUD + UserAuthorization With JSON Requests

# route for sending post request for create a new user with json *Login is Required*
@app.post("/user/signup/json/", dependencies=[Depends(JWTBearer())], tags=["User, JSON Method"])
def create_user_json(user: UserSchema):
    return auth.add_user(user)


# route for sending post request for login user with json
@app.post("/user/login/json/", tags=["User, JSON Method"])
def user_login_json(user: UserSchema):
    return auth.check_user(user)


# route for sending post request for create a new row with json *Login is Required*
@app.post("/create/json/", dependencies=[Depends(JWTBearer())], tags=["CRUD, JSON Method"])
async def data_entry_json(item: ParamsRequired):
    results = item.dict(exclude_none=True)
    results.update({"pic_uri": None})
    if check_duplication(results):
        return {"pod_name": env.HOSTNAME, "status": "# of inserted rows = {}".format(0)}
    return sql.set_in_db(**results)


# route for sending post request for read row/rows with json *Login is Required*
@app.post("/read/json/", dependencies=[Depends(JWTBearer())], tags=["CRUD, JSON Method"])
def data_load_json(item: Params):
    results = item.dict(exclude_none=True)
    return {"pod_name": env.HOSTNAME, "result": sql.get_from_db(**results)}


# route for sending post request for update row/rows with json *Login is Required*
@app.post("/update/json/", dependencies=[Depends(JWTBearer())], tags=["CRUD, JSON Method"])
async def update_item_json(item: JsonBody):
    results = item.dict(exclude_none=True)
    if len(results["filter"]) == 0:
        return {"pod_name": env.HOSTNAME, "is_ok": False, "details": "at least one filter should be used"}
    if len(results["update_params"]) == 0:
        return {"pod_name": env.HOSTNAME, "is_ok": False, "details": "at least one update_params should be used"}
    return sql.update_row(results)


# route for sending post request for delete row/rows with json *Login is Required*
@app.post("/delete/json/", dependencies=[Depends(JWTBearer())], tags=["CRUD, JSON Method"])
async def delete_item_json(item: Params):
    results = item.dict(exclude_none=True)
    if len(results) == 0:
        return {"is_ok": False, "details": "There should be param to remove"}
    return sql.delete_row(**results)

if __name__ == "__main__":
    uvicorn.run("main:app", host=env.RESTAPI_URL, port=env.RESTAPI_PORT, log_level="info")
