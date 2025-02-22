from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_restful import Api
from sqlalchemy import MetaData
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_convention)
db = SQLAlchemy(metadata=metadata)
# api = Api(app)

def init_db(app):
    db.init_app(app)

    print("here")
    Migrate(app, db)
