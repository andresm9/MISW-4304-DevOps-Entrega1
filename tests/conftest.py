import os
import pytest
from dotenv import load_dotenv

load_dotenv()
print(os.getenv('JWT_SECRET_KEY'))

from application import create_app
from models import db


@pytest.fixture()
def app():

    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    }

    app = create_app(test_config)

    with app.app_context():
        db.create_all()

        # Execute SQL statements from `data.sql` (if present)
        sql_path = os.path.join(os.path.dirname(__file__), 'data.sql')
        if os.path.exists(sql_path):
            with open(sql_path, 'r') as f:
                sql = f.read()
            conn = db.engine.raw_connection()
            try:
                cursor = conn.cursor()
                cursor.executescript(sql)
                conn.commit()
            finally:
                conn.close()

        yield app


        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def token(client):
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDAyMDgzMiwianRpIjoiNTE2ZTc5MGEtOWVkOS00NDUwLWJiNTctMTkxMTYxNjhkYTRkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IkRlZmF1bHRVc2VyIiwibmJmIjoxNzYwMDIwODMyLCJjc3JmIjoiOWNhNThmMTMtOTBiZi00Y2NjLWI3MmUtZWI1ZmQwMzY4OGU5IiwiZXhwIjoxNzY1MjA0ODMyfQ.NgwyLsqFhzRXV5cpuN5yVdINlTZNocwuo-CD47HU_W8"
