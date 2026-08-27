import pytest
from datetime import date
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db
from models import User, Transaction
from security import get_current_user








SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)
















#--------------------------------------------------------------------------------------------------------------------
# Create Database Session for Testing 
#--------------------------------------------------------------------------------------------------------------------
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)






#--------------------------------------------------------------------------------------------------------------------
# Create Fake User
#--------------------------------------------------------------------------------------------------------------------
@pytest.fixture(scope="function")
def test_user(db_session: Session):
    user = User(
        username="testuser",
        email="testuser@example.com",
        hashed_password="fakehashedpassword",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user







#--------------------------------------------------------------------------------------------------------------------
# Override get_db & get_current_user functions
#--------------------------------------------------------------------------------------------------------------------

@pytest.fixture(scope="function")
def client(db_session: Session, test_user: User):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    def override_get_current_user():
        return test_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()







#--------------------------------------------------------------------------------------------------------------------
# Sample test case for testing 
#--------------------------------------------------------------------------------------------------------------------

@pytest.fixture(scope="function")
def sample_transaction(db_session: Session, test_user: User):
    transaction = Transaction(
        title="Groceries",
        amount=250.0,
        type="expense",
        category="Food",
        date=date(2026, 1, 15),
        owner_id=test_user.id,
    )
    db_session.add(transaction)
    db_session.commit()
    db_session.refresh(transaction)
    return transaction