from typing import Optional, List

from .base import BaseInterface
from .models import Cocktail, Ingredient
from .serializers import CocktailSchema, IngredientSchema


class CocktailInterface(BaseInterface):
    def create(self, name:str, ingredients:List[int]):
        new_item = Cocktail(name=name)

        for ingredient_id in ingredients:
            ingredient_object = IngredientInterface.read_one(ingredient_id)
            Cocktail.ingredients.append(ingredient_object)

        self.session.add(new_item)
        self.session.commit()
        return new_item


    def read_one(self, id:int):
        query = self.session.query(Cocktail).filter(Cocktail.id==id)
        found = query.one()
        return found

    def read_all(self):
        query = self.session.query(Cocktail)
        found = query.all()
        return found


class IngredientInterface(BaseInterface):
    def create(self, name: str):
        new_item = Ingredient(name=name)
        self.session.add(new_item)
        self.session.commit()
        return new_item

    def read_one(self, id: int):
        query = self.session.query(Ingredient).filter(Ingredient.id == id)
        found = query.one()
        return found

    def read_all(self):
        query = self.session.query(Ingredient)
        found = query.all()
        return found
