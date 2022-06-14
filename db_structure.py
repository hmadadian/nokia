from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, TEXT, Boolean
import env

Base = declarative_base()


# Database Structure as class
class DbStructure:
    def __init__(self):
        self.base = Base

    class FoodList(Base):
        __tablename__ = env.TABLE_NAME
        pid = Column(Integer, primary_key=True)
        name = Column(TEXT, nullable=False)
        price = Column(Integer, nullable=False)
        ingredients = Column(TEXT, nullable=False)
        spicy = Column(Boolean, nullable=False)
        vegan = Column(Boolean, nullable=False)
        gluten_free = Column(Boolean, nullable=False)
        description = Column(TEXT, nullable=False)
        kcal = Column(Integer, nullable=False)
        pic_uri = Column(TEXT)

    def return_base(self):
        return self.base
