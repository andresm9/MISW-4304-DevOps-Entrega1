import os
import pytest
from dotenv import load_dotenv
from testcontainers.postgres import PostgresContainer

load_dotenv()
print(os.getenv('JWT_SECRET_KEY'))

from application import create_app
from models import db

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:latest", port=5434) as pg:
        yield pg

@pytest.fixture
def app(postgres_container):
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": postgres_container.get_connection_url()
    }
    app = create_app(test_config)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def token(client):
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MTIyNTI5NiwianRpIjoiYTU5NmI0MTctZWNmYy00MzBkLWFhZjItNjczZjJmNGQ0MWJkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IkRlZmF1bHRVc2VyIiwibmJmIjoxNzYxMjI1Mjk2LCJjc3JmIjoiMjdlZjNhODctN2JkYi00NGMyLWJmNWMtYjc3OTE3YTgwM2ZjIiwiZXhwIjoxNzY2NDA5Mjk2fQ.HWJbk6009Rg1wpGHsMh71VGKiihHJ3Isv-wxNZENFIg"
