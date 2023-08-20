import os

from logging import getLogger

import pytest

from rest.notes_rest import NotesRest

logger = getLogger(__name__)


@pytest.fixture(scope="session")
def email():
    return os.getenv("EMAIL")


@pytest.fixture(scope="session")
def password():
    return os.getenv("PASSWORD")


@pytest.fixture
def registration_data():
    return {
        "name": "Something New",
        "email": "ddozoaaaa@any.pink",
        "password": "123456789"
    }


@pytest.fixture
def registered_user(registration_data, notes_service):
    response = notes_service.post_users_register(**registration_data)
    return response["data"]


@pytest.fixture
def notes_service():
    return NotesRest()


@pytest.fixture
def authenticated_notes_service(notes_service, email, password):
    authenticated_notes_service = notes_service
    login_response = authenticated_notes_service.post_users_login(email, password)
    authenticated_notes_service.update_token(login_response["data"]["token"])
    return authenticated_notes_service


@pytest.fixture
def prepared_note(authenticated_notes_service) -> dict:
    logger.info("Preparing note for tests")
    response = authenticated_notes_service.post_notes(
        title="Test note",
        description="Test Description",
        category="Home",
        expected_status_code=200
    )
    logger.info(f"Note prepared: {response['data']}")
    return response["data"]


@pytest.fixture
def created_note_response(request):
    return request.getfixturevalue("prepared_note")
