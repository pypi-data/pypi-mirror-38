import pytest

from cocktail_model_lib import base
from cocktail_model_lib import models
from cocktail_model_lib import functions

from .helpers import contains_dict_with_field




def test_database_contains_correct_tables(engine):
    from sqlalchemy.engine import reflection

    inspection = reflection.Inspector.from_engine(engine)
    table_names = inspection.get_table_names()
    assert 'ingredient' in table_names
    assert 'cocktail' in table_names
    assert 'ingredient_cocktail_association' in table_names

def test_database_ingredient_table_is_correct(engine):
    from sqlalchemy.engine import reflection

    inspection = reflection.Inspector.from_engine(engine)
    ingredient_columns = inspection.get_columns('ingredient')
    assert contains_dict_with_field(ingredient_columns, 'name', 'id')
    assert contains_dict_with_field(ingredient_columns, 'name', 'name')

def test_database_cocktail_table_is_correct(engine):
    from sqlalchemy.engine import reflection

    inspection = reflection.Inspector.from_engine(engine)
    cocktail_columns = inspection.get_columns('cocktail')
    assert contains_dict_with_field(cocktail_columns, 'name', 'id')
    assert contains_dict_with_field(cocktail_columns, 'name', 'name')
