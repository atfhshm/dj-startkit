import pytest
from django.test import Client
from django.contrib.auth.models import User
from myapp.models import (
    MyModel,
)  # Replace 'myapp' and 'MyModel' with actual app and model names


@pytest.fixture
def api_client():
    """
    Fixture returns a Django test client instance.
    """
    return Client()


@pytest.fixture
def create_user(db):
    """
    Fixture to create a Django user instance.
    """

    def _create_user(
        username="testuser",
        password="testpassword",
        email="testuser@example.com",
        **kwargs,
    ):
        user = User.objects.create_user(
            username=username, password=password, email=email, **kwargs
        )
        return user

    return _create_user


@pytest.fixture
def authenticated_client(api_client, create_user):
    """
    Fixture to provide a Django test client logged in as a created user.
    """
    user = create_user()
    api_client.login(username=user.username, password="testpassword")
    return api_client


@pytest.fixture
def sample_model_instance(db):
    """
    Fixture to create a sample model instance.
    """

    def _create_instance(**kwargs):
        instance = MyModel.objects.create(**kwargs)
        return instance

    return _create_instance


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Automatically enable database access for all tests.
    """
    pass


@pytest.fixture(scope="session")
def django_db_setup():
    """
    Custom Django database setup fixture.
    Modify settings if needed.
    """
    from django.conf import settings

    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "test_db",
        "USER": "test_user",
        "PASSWORD": "test_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
