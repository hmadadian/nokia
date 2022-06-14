from pydantic import BaseModel


# validator class for fastapi data validation
class Params(BaseModel):
    name: str | None = None
    price: int | None = None
    ingredients: str | None = None
    spicy: bool | None = None
    vegan: bool | None = None
    gluten_free: bool | None = None
    description: str | None = None
    kcal: int | None = None


class JsonBody(BaseModel):
    filter: Params
    update_params: Params


class ParamsRequired(BaseModel):
    name: str
    price: int
    ingredients: str
    spicy: bool
    vegan: bool
    gluten_free: bool
    description: str
    kcal: int


class UserSchema(BaseModel):
    username: str
    password: str
