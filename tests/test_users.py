import pytest


def test_user_registration(notes_service, registration_data):
    response = notes_service.post_users_register(**registration_data)
    assert response["success"] is True
    assert response["status"] == 201
    assert response["message"] == "User account created successfully"
    registered_user_data = response["data"]
    assert "id" in registered_user_data
    assert "name" in registered_user_data
    assert "email" in registered_user_data
    assert registered_user_data["name"] == registration_data["name"]
    assert registered_user_data["email"] == registration_data["email"]


def test_user_registration_duplicate_email_negative(notes_service):
    registration_data = {
        "name": "Something New",
        "email": "ddozoa@any.pink",
        "password": "password123"
    }
    response = notes_service.post_users_register(**registration_data, expected_status_code=409)
    assert response["success"] is False
    assert response["status"] == 409
    assert "email" in response["message"].lower()
    assert "data" not in response


def test_login(notes_service, email, password):
    response = notes_service.post_users_login(email, password)
    assert response["data"]["token"] is not None


def test_login_invalid_email(notes_service, password):
    response = notes_service.post_users_login("invalid@email.com", password, expected_status_code=401)
    assert response["message"] == "Incorrect email address or password"


def test_profile_unauthenticated(notes_service):
    response = notes_service.get_users_profile(expected_status_code=401)
    assert response["message"] == "No authentication token specified in x-auth-token header"


def test_profile(authenticated_notes_service, email):
    response = authenticated_notes_service.get_users_profile()
    assert response["message"] == "Profile successful"
    assert response["data"]["email"] == email, "Email address is not correct"


def test_update_profile_positive(authenticated_notes_service):
    new_name = "Something New"
    new_phone = "1234567890"
    new_company = "Test"
    response = authenticated_notes_service.update_users_profile(
        name=new_name, phone=new_phone, company=new_company)
    assert response["success"] is True
    assert response["status"] == 200
    assert response["message"] == "Profile updated successful"
    assert "data" in response
    assert "id" in response["data"]
    assert "name" in response["data"]
    assert "email" in response["data"]
    assert "phone" in response["data"]
    assert "company" in response["data"]
    assert response["data"]["name"] == new_name
    assert response["data"]["phone"] == new_phone
    assert response["data"]["company"] == new_company


def test_update_profile_negative_check(authenticated_notes_service):
    new_name = "A"
    new_phone = "1234567890"
    new_company = "Test"
    response = authenticated_notes_service.update_users_profile(
        name=new_name, phone=new_phone, company=new_company, expected_status_code=400)
    assert response["success"] is False
    assert response["status"] == 400
    assert response["message"] == "User name must be between 4 and 30 characters"


def test_forgot_password(authenticated_notes_service, email):
    response = authenticated_notes_service.users_forgot_password(email=email)
    assert response["success"] is True
    assert response["status"] == 200
    assert response["message"] == f"Password reset link successfully sent to {email}. " \
                                  f"Please verify by clicking on the given link"


def test_forgot_password_negative_check(authenticated_notes_service):
    non_existing_email = "ew@any.pink"
    response = authenticated_notes_service.users_forgot_password(email=non_existing_email, expected_status_code=401)
    assert response["success"] is False
    assert response["status"] == 401
    assert response["message"] == "No account found with the given email address"


@pytest.mark.parametrize("token, expected_status", [
    ("52ff781c1ed64ca1b89b704b9713767d5dc34cda3722432ca3be0330fbfd78e4", 401),
])
def test_verify_reset_password_token_negative(notes_service, token, expected_status):
    response = notes_service.post_users_verify_reset_password_token(token=token)
    assert response["success"] is False
    assert response["status"] == expected_status
    assert response["message"] == "The provided password reset token is invalid or has expired"


@pytest.mark.parametrize("token, new_password", [
    ("52ff781c1ed64ca1b89b704b9713767d5dc34cda3722432ca3be0330fbfd78e4", "123456"),
])
def test_reset_password_with_invalid_token(notes_service, token, new_password):
    response = notes_service.post_users_reset_password(token=token, new_password=new_password)
    assert response["success"] is False
    assert response["status"] == 401
    assert response["message"] == "The password reset token is invalid or has expired"


def test_change_password(authenticated_notes_service, email, password):
    new_password = "1234test123456"
    response = authenticated_notes_service.change_users_password(current_password=password, new_password=new_password)
    assert response["success"] is True
    assert response["status"] == 200
    assert response["message"] == "The password was successfully updated"
    login_response = authenticated_notes_service.post_users_login(email=email, password=new_password)
    assert login_response["data"]["token"] is not None


def test_logout(notes_service, email):
    new_password = "1234test123456"
    response = notes_service.post_users_login(email, new_password)
    assert response["data"]["token"] is not None
    response = notes_service.delete_users_logout()
    assert response["success"] is True
    assert response["status"] == 200
    assert response["message"] == "User has been successfully logged out"


def test_delete_account(notes_service, email):
    new_password = "1234test123456"
    response = notes_service.post_users_login(email, new_password)
    assert response["data"]["token"] is not None
    response = notes_service.delete_users_account()
    assert response["success"] is True
    assert response["status"] == 200
    assert response["message"] == "Account successfully deleted"
