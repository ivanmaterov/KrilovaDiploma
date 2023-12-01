import pathlib

import pytest
from django.conf import settings
from rest_framework.test import APIClient

from apps.users.models import User


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def api_client() -> APIClient:
    """Create api client."""
    return APIClient()


@pytest.fixture(scope='function')
def user_authenticated(api_client: APIClient, user: User):
    """Fixture authenticates current user to API."""
    api_client.force_authenticate(user=user)


@pytest.fixture(scope='function')
def set_up_temporary_media_directory(tmp_path: pathlib.Path):
    """Override default media path for tests."""
    settings.MEDIA_ROOT = tmp_path
    return settings.MEDIA_ROOT
