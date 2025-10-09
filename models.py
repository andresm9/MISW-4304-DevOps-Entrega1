from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
ma = Marshmallow()

class Blacklist(Base):
    __tablename__ = 'blacklist'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    email = mapped_column(String, unique=True, nullable=False)
    app_uuid = mapped_column(String, nullable=False)
    blocked_reason = mapped_column(String, nullable=True)

class BlacklistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Blacklist
        load_instance = True
        include_fk = True