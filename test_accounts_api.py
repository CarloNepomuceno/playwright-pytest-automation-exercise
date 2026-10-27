
import pytest

from utils.apiBase import APIUtils


# pytest -m api

@pytest.mark.smoke
@pytest.mark.api
def test_verify_login_valid(playwright, newUser):
    api_utils = APIUtils()
    response = api_utils.verifyLogin(playwright, newUser["email"], newUser["password"])
    assert response["responseCode"] == 200
    assert response["message"] == "User exists!"


@pytest.mark.api
def test_verify_login_wrong_password(playwright, newUser):
    api_utils = APIUtils()
    response = api_utils.verifyLogin(playwright, newUser["email"], "wrong-password")
    assert response["responseCode"] == 404
    assert response["message"] == "User not found!"


@pytest.mark.api
def test_verify_login_missing_parameter(playwright):
    api_utils = APIUtils()
    response = api_utils.verifyLogin(playwright, email="someone@example.com")
    assert response["responseCode"] == 400


@pytest.mark.api
def test_get_user_detail_by_email(playwright, newUser):
    api_utils = APIUtils()
    response = api_utils.getUserByEmail(playwright, newUser["email"])
    assert response["responseCode"] == 200
    assert response["user"]["email"] == newUser["email"]
