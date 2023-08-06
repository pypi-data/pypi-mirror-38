from .base import MODEL_BASE
from .base import Column, Table, String, Integer, ForeignKey
from .base import relationship


ingredient_cocktail_association = Table(
    'ingredient_cocktail_association',
    MODEL_BASE.metadata,
    Column('ingredient_id', Integer, ForeignKey('ingredient.id'), primary_key=True),
    Column('cocktail_id', Integer, ForeignKey('cocktail.id'), primary_key=True),
)


class Ingredient(MODEL_BASE):
    __tablename__ = 'ingredient'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)


class Cocktail(MODEL_BASE):
    __tablename__ = 'cocktail'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    ingredients = relationship(
        'Ingredient',
        secondary='ingredient_cocktail_association',
    )