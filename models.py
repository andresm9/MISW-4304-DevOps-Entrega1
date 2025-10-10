from flask_marshmallow import Marshmallow, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from marshmallow.validate import Length

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
ma = Marshmallow()

class Blacklist(db.Model):
    __tablename__ = 'blacklist'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    email = mapped_column(String, unique=True, nullable=False)
    app_uuid = mapped_column(String, nullable=False)
    blocked_reason = mapped_column(String, nullable=True)
    ip_address = mapped_column(String, nullable=True)

#Esquema para los datos de entrada
class BlackListRequestSchema(ma.Schema):
    email = fields.fields.Email(required=True)
    app_uuid = fields.fields.UUID(required=True)
    blocked_reason = fields.fields.String(validate=Length(max=255, error="Blocked reason must be less than 255 characters"))


class BlacklistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Blacklist
        load_instance = True,
        include_fk = True

    email = fields.fields.Email(required=True)
    app_uuid = fields.fields.UUID()
    blocked_reason = fields.fields.String()
    ip_address = fields.fields.IP()
