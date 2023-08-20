from rest.rest_client import RestClient


class NotesRest(RestClient):
    """
    Notes API service
    """
    BASE_URL = "https://practice.expandtesting.com/notes/api/"
    _token: str | None = None

    @property
    def _headers(self):
        return {"x-auth-token": self._token}

    def get_health_check(self):
        """
        Send a GET request to /health-check
        :return: response in JSON format
        """
        self._log.info("Checking health")
        response = self._get("health-check")
        return response

    def post_users_register(self, name=None, email=None, password=None, expected_status_code=201):
        """
        Send a POST request to register a new user
        :param name: user's name
        :param email: user's email
        :param password: user's password
        :param expected_status_code: expected status code
        :return: response in JSON format
        """
        self._log.info(f"Registering new user with email: {email}")
        response = self._post("users/register",
                              data={"name": name, "email": email, "password": password},
                              expected_status_code=expected_status_code)
        return response

    def post_users_login(self, email=None, password=None, expected_status_code=200):
        """
        Send a POST request to /users/login
        :param email: email
        :param password: password
        :param expected_status_code: expected status code
        :return: response in JSON format
        """
        self._log.info(f"Logging in as {email}")
        response = self._post("users/login",
                              json={"email": email, "password": password},
                              expected_status_code=expected_status_code)
        if response["status"] == 200:
            self._token = response["data"]["token"]
        return response

    def delete_users_logout(self, expected_status_code=200):
        """
        Send a DELETE request to /users/logout
        :param expected_status_code: expected status code
        :return: response in JSON format
        """
        self._log.info("Logging out")
        response = self._delete("users/logout", expected_status_code=expected_status_code)
        if response["status"] == 200:
            self._token = None
        return response

    def get_users_profile(self, expected_status_code=200):
        """
        Send a GET request to /users/profile
        :param expected_status_code: expected status code
        :return: response in JSON format
        """
        self._log.info("Getting user profile")
        response = self._get("users/profile", expected_status_code=expected_status_code)
        return response

    def post_notes(self, title=None, description=None, category=None, expected_status_code=200):
        """
        Send a POST request to /notes
        :param title: title of the note
        :param description: description of the note
        :param category: category of the note (Home, Work, Personal)
        :param expected_status_code: expected status code
        :return: response in JSON format
        """
        self._log.info(f"Creating note with title: {title}")
        response = self._post("notes",
                              data={"title": title, "description": description, "category": category},
                              expected_status_code=expected_status_code)
        return response

    def delete_note_by_id(self, note_id=None, expected_status_code=200):
        """
        Send a DELETE request to /notes/{note_id}
        :param note_id: id of the note
        :param expected_status_code: expected status code
        :return: response in JSON format
        """
        self._log.info(f"Deleting note with id: {note_id}")
        response = self._delete(f"notes/{note_id}", expected_status_code=expected_status_code)
        return response

    def update_users_profile(self, name=None, phone=None, company=None, expected_status_code=200):
        """
        Send a PATCH request to /users/profile to update user profile
        :param name: new name of the user
        :param phone: new phone number of the user
        :param company: new company name of the user
        :param expected_status_code: expected status code
        :return: response in JSON format
        """
        self._log.info("Updating user profile")
        data = {
            "name": name,
            "phone": phone,
            "company": company
        }
        headers = {
            "x-auth-token": self._token,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = self._patch("users/profile", data=data, headers=headers, expected_status_code=expected_status_code)
        return response

    def users_forgot_password(self, email, expected_status_code=200):
        """
        Send a POST request to /users/forgot-password
        :param email: user's email for password reset
        :param expected_status_code: expected status code
        :return: response in JSON format
        """
        self._log.info(f"Sending password reset request to {email}")
        response = self._post("users/forgot-password", data={"email": email}, expected_status_code=expected_status_code)
        return response

    def change_users_password(self, current_password, new_password, expected_status_code=200):
        """
        Change a user's password by providing the user's current password and the new password.
        :param current_password: user's current password
        :param new_password: user's new password
        :param expected_status_code: expected status code
        :return: response in JSON format
        """
        self._log.info("Changing user's password")
        data = {
            "currentPassword": current_password,
            "newPassword": new_password
        }
        response = self._post("users/change-password", data=data, expected_status_code=expected_status_code)
        return response

    def update_token(self, token):
        self._token = token

    def delete_users_account(self, expected_status_code=200):
        """
        Delete the authenticated user account
        :param expected_status_code: expected status code
        :return: response in JSON format
        """
        self._log.info("Deleting user account")
        headers = {
            "x-auth-token": self._token
        }
        response = self._delete("users/delete-account", headers=headers, expected_status_code=expected_status_code)
        if response["status"] == 200:
            self._token = None
        return response

    def get_notes(self, expected_status_code=200):
        """
        Retrieve a list of notes for the authenticated user
        :param expected_status_code: expected status code
        :return: response in JSON format
        """
        self._log.info("Getting user notes")
        response = self._get("notes", expected_status_code=expected_status_code)
        return response

    def get_note_by_id(self, note_id, expected_status_code=200):
        """
        Retrieve a note by its ID
        :param note_id: ID of the note to retrieve
        :param expected_status_code: expected status code
        :return: response in JSON format
        """
        self._log.info(f"Getting note by ID: {note_id}")
        response = self._get(f"notes/{note_id}", expected_status_code=expected_status_code)
        return response

    def post_users_reset_password(self, token, new_password):
        """
        Reset password by token
        :param token: token send by email.
        :param new_password: changing the password.
        :return: response in JSON format
        """
        path = "users/reset-password"
        data = {
            "token": token,
            "newPassword": new_password
        }
        response = self._post(path, data=data, expected_status_code=401)
        return response

    def post_users_verify_reset_password_token(self, token):
        """
        Verify the provided password reset token.
        :param token: The password reset token received via email
        :return: Response in JSON format
        """
        path = "users/verify-reset-password-token"
        data = {
            "token": token
        }
        response = self._post(path, data=data, expected_status_code=401)
        return response
