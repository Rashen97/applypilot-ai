from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.database import Base, get_db
from backend.app.main import app

import pytest

TEST_DATABASE_URL = "sqlite://"

#This function provides testing setup/behaviour for each test function. It will run before and after each test function.
@pytest.fixture(autouse=True)  
def reset_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield

test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestSessionLocal = sessionmaker(bind=test_engine, autoflush=False, expire_on_commit=False)

Base.metadata.create_all(bind=test_engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db