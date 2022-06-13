from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import FastAPI, UploadFile, Depends
from pydantic import ValidationError
from typing import Optional
from pathlib import Path
import string
import random
import shutil
import json
import os
from pgsql import SqlInteraction
from http_2_json import Http2Json
from validator import *
from authentication import *
import env
import uvicorn

sql = SqlInteraction(env.DATABASE_URL, env.TABLE_NAME)
auth = UserManager()

app = FastAPI()
origins = ["*"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])


# CRUD + User authentication With normal Query

@app.post("/user/signup", dependencies=[Depends(JWTBearer())], tags=["User, Query Method"])
def create_user(username: str, password: str):
    return auth.add_user(UserSchema(**{"username": username, "password": password}))


@app.post("/user/login", tags=["User, Query Method"])
def user_login(username: str, password: str):
    return auth.check_user(UserSchema(**{"username": username, "password": password}))


@app.post("/create", dependencies=[Depends(JWTBearer())], tags=["CRUD, Query Method"])
async def data_entry(name: str, price: int, ingredients: str, spicy: bool, vegan: bool, gluten_free: bool,
                     description: str, kcal: int, file: UploadFile | None = None):
    file_url = None
    if file:
        random_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
        file_name = random_name + Path(file.filename).suffix
        directory = env.WEBSERVER_DIR + os.sep + file_name
        file_url = env.WEBSERVER_URL + "/" + file_name
        with open(directory, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    data = {"name": name, "price": price, "ingredients": ingredients, "spicy": spicy, "vegan": vegan,
            "gluten_free": gluten_free, "description": description, "kcal": kcal, "pic_uri": file_url}

    return sql.set_in_db(**data)


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

    # imporove description with searching inside description cell
    if description:
        data.update({"description": description})
    if kcal:
        data.update({"kcal": kcal})

    return JSONResponse(sql.get_from_db(**data))


@app.post("/update/{items}", dependencies=[Depends(JWTBearer())], tags=["CRUD, Query Method"])
def data_update(items: Optional[str] = None):
    query = Http2Json()
    item_dict = query.convert(items)
    try:
        validated_items = JsonBody(**item_dict).dict(exclude_none=True)
        if len(validated_items["filter"]) == 0:
            return {"is_ok": False, "details": "at least one filter should be used"}
        if len(validated_items["update_params"]) == 0:
            return {"is_ok": False, "details": "at least one update_params should be used"}
        return sql.update_row(validated_items)
    except ValidationError as e:
        return JSONResponse(json.loads(e.json()))


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

    # imporove description with searching inside description cell
    if description:
        data.update({"description": description})
    if kcal:
        data.update({"kcal": kcal})
    if len(data) == 0:
        return {"is_ok": False, "details": "There should be param to remove"}
    return sql.delete_row(**data)


# CRUD + UserAuthorization With JSON Requests

@app.post("/user/signup/json/", dependencies=[Depends(JWTBearer())], tags=["User, JSON Method"])
def create_user_json(user: UserSchema):
    return auth.add_user(user)


@app.post("/user/login/json/", tags=["User, JSON Method"])
def user_login_json(user: UserSchema):
    return auth.check_user(user)


@app.post("/create/json/", dependencies=[Depends(JWTBearer())], tags=["CRUD, JSON Method"])
async def data_entry_json(item: ParamsRequired):
    results = item.dict(exclude_none=True)
    results.update({"pic_uri": None})
    return sql.set_in_db(**results)


@app.post("/read/json/", dependencies=[Depends(JWTBearer())], tags=["CRUD, JSON Method"])
def data_load_json(item: Params):
    results = item.dict(exclude_none=True)
    return JSONResponse(sql.get_from_db(**results))


@app.post("/update/json/", dependencies=[Depends(JWTBearer())], tags=["CRUD, JSON Method"])
async def update_item_json(item: JsonBody):
    results = item.dict(exclude_none=True)
    if len(results["filter"]) == 0:
        return {"is_ok": False, "details": "at least one filter should be used"}
    if len(results["update_params"]) == 0:
        return {"is_ok": False, "details": "at least one update_params should be used"}
    return sql.update_row(results)


@app.post("/delete/json/", dependencies=[Depends(JWTBearer())], tags=["CRUD, JSON Method"])
async def delete_item_json(item: Params):
    results = item.dict(exclude_none=True)
    if len(results) == 0:
        return {"is_ok": False, "details": "There should be param to remove"}
    return sql.delete_row(**results)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
