from marshmallow import Schema, fields


class IngredientSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class CocktailSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    ingredients = fields.Nested(IngredientSchema, many=True)
