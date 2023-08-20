import pytest


@pytest.mark.parametrize("category", ["Home", "Work", "Personal"])
def test_create_note(authenticated_notes_service, category):
    title = "Test note"
    description = "Test Description"
    response = authenticated_notes_service.post_notes(title, description, category)
    assert response["message"] == "Note successfully created"
    assert response["data"]["title"] == title
    assert response["data"]["description"] == description
    assert response["data"]["category"] == category
    assert response["data"]["id"] is not None
    return response


def test_create_note_negative_check(authenticated_notes_service):
    title = "1"
    description = "1"
    category = "Home"
    response = authenticated_notes_service.post_notes(title=title, description=description, category=category,
                                                      expected_status_code=400)
    assert response["success"] is False
    assert response["status"] == 400
    assert response["message"] == "Title must be between 4 and 100 characters"


def test_create_note_invalid_category(authenticated_notes_service):
    title = "Test note"
    description = "Test Description"
    category = "Invalid"
    response = authenticated_notes_service.post_notes(title, description, category, expected_status_code=400)
    assert response["message"] == "Category must be one of the categories: Home, Work, Personal"


def test_get_notes(authenticated_notes_service):
    response = authenticated_notes_service.get_notes()
    assert response["success"] is True
    assert response["status"] == 200
    assert response["message"] == "Notes successfully retrieved"


def test_get_note_by_id(authenticated_notes_service, created_note_response):
    note_id = created_note_response["id"]
    get_response = authenticated_notes_service.get_note_by_id(note_id)
    assert get_response["success"] is True
    assert get_response["status"] == 200
    assert get_response["message"] == "Note successfully retrieved"
    assert "data" in get_response
    note_data = get_response["data"]
    assert note_data["id"] == note_id
    assert note_data["title"] == "Test note"


def test_get_note_invalid_id(authenticated_notes_service):
    invalid_note_id = "64"
    response = authenticated_notes_service.get_note_by_id(invalid_note_id, expected_status_code=400)
    assert response["success"] is False
    assert response["status"] == 400
    assert response["message"] == "Note ID must be a valid ID"


def test_delete_note_by_id(authenticated_notes_service, prepared_note):
    response = authenticated_notes_service.delete_note_by_id(prepared_note["id"])
    assert response["message"] == "Note successfully deleted"
