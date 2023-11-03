import enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

## Enumeration of possible size
class SizeOption(enum.Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

## Oferta model
class Oferta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.Integer)
    userId = db.Column(db.Integer)
    description = db.Column(db.String(140))
    size = db.Column(db.Enum(SizeOption))
    fragile = db.Column(db.Boolean)
    offer = db.Column(db.Float)
    createdAt = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

## Serializer
class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return f'{value.value}'

## Oferta schema for get
class OfertaSchemaGet(SQLAlchemyAutoSchema):
    size = EnumADiccionario(attribute=("size"))
    class Meta:
        model = Oferta
        load_instance = True


class OfertaSchema(Schema):
    id = fields.Int(dump_only=True)
    postId = fields.Int(required=True, validate=[validate.Range(min=0)])
    userId = fields.Int(required=True,validate=[validate.Range(min=0)] )
    description = fields.Str(required=True, validate=[validate.Length(min=1, max=140)], load_only=True)
    size = EnumADiccionario(attribute=("size"), required=True, validate=[validate.OneOf([item.value for item in SizeOption])] , load_only=True)	
    fragile = fields.Bool(required=True, load_only=True)
    offer = fields.Float(required=True, validate=[validate.Range(min=0)], load_only=True)
    createdAt = fields.DateTime(dump_only=True)

    class Meta:
        model = Oferta