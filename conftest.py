import json
from pathlib import Path

import pytest

from utils.apiBase import APIUtils

AD_DOMAINS = ("googlesyndication.com", "doubleclick.net", "googleadservices.com",
              "adservice.google.com")


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )
    parser.addoption(
        "--run_headless", action="store_true", default=False, help="run without a visible browser (for CI)"
    )


def loadProfiles():
    # Json file -> util -> access into test (same pattern as the course)
    BASE_DIR = Path(__file__).parent
    with open(BASE_DIR / "data" / "user_profiles.json") as f:
        return json.load(f)["user_credentials"]


@pytest.fixture
def browserInstance(playwright, request):
    browser_name = request.config.getoption("browser_name")
    headless = request.config.getoption("run_headless")
    if browser_name == "chrome":
        browser = playwright.chromium.launch(headless=headless)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=headless)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    context = browser.new_context()
    # Ad requests can cover buttons and break clicks to block them
    context.route("**/*", lambda route: route.abort()
                  if any(domain in route.request.url for domain in AD_DOMAINS)
                  else route.continue_())
    page = context.new_page()
    yield page
    context.close()
    browser.close()


@pytest.fixture
def newUser(playwright, request):
    """Create a user through the API, give it to the test, then always delete it.

    Works with or without parametrize:
    - plain use: takes the first profile from user_profiles.json
    - @pytest.mark.parametrize("newUser", profiles, indirect=True): uses that profile
    """
    profile = getattr(request, "param", None) or loadProfiles()[0]
    api_utils = APIUtils()
    user = api_utils.buildUser(profile)
    response = api_utils.createAccount(playwright, user)
    assert response["responseCode"] == 201, f"Account setup failed: {response}"
    yield user
    deleted = api_utils.deleteAccount(playwright, user["email"], user["password"])
    if deleted.get("responseCode") != 200:
        print(f"WARNING: could not delete {user['email']}: {deleted}")


@pytest.fixture
def registrationUser(playwright):
    """Prepare unique user data (no account yet), then always delete it after the test."""
    api_utils = APIUtils()
    user = api_utils.buildUser(loadProfiles()[0])
    yield user
    deleted = api_utils.deleteAccount(playwright, user["email"], user["password"])
    if deleted.get("responseCode") != 200:
        print(f"WARNING: could not delete {user['email']}: {deleted}")