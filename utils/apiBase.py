import json
import time
import uuid

from playwright.sync_api import Playwright

BASE_URL = "https://automationexercise.com"


class APIUtils:
    """Same idea as the course's APIUtils, for automationexercise.com.

    Notes about this site's API:
    - Requests are sent as form data (form=...), not JSON.
    - The real result is in the body's "responseCode", not the HTTP status.
    - Some responses come back as text/html, so we parse response.text() ourselves.
    """

    def buildUser(self, profile):
        # Unique email per run so reruns and parallel tests never collide
        user = dict(profile)
        user["email"] = f"qa_{uuid.uuid4().hex[:8]}@example.com"
        return user

    def _parse(self, response):
        return json.loads(response.text())

    def _context(self, playwright: Playwright):
        return playwright.request.new_context(base_url=BASE_URL)

    def createAccount(self, playwright: Playwright, user):
        api_request_context = self._context(playwright)
        for attempt in range(3):
            response = api_request_context.post("/api/createAccount", form=user)
            text = response.text()
            if text.lstrip().startswith("{"):
                return json.loads(text)
            time.sleep(3)  # the site sent an HTML page, wait and try again
        raise AssertionError(f"createAccount kept returning a non-JSON page: {text[:150]}")

    def deleteAccount(self, playwright: Playwright, email, password):
        api_request_context = self._context(playwright)
        response = api_request_context.delete("/api/deleteAccount",
                                              form={"email": email, "password": password})
        return self._parse(response)

    def verifyLogin(self, playwright: Playwright, email=None, password=None):
        form = {}
        if email is not None:
            form["email"] = email
        if password is not None:
            form["password"] = password
        api_request_context = self._context(playwright)
        response = api_request_context.post("/api/verifyLogin", form=form)
        return self._parse(response)

    def getUserByEmail(self, playwright: Playwright, email):
        api_request_context = self._context(playwright)
        response = api_request_context.get("/api/getUserDetailByEmail", params={"email": email})
        return self._parse(response)

    def getProductsList(self, playwright: Playwright):
        api_request_context = self._context(playwright)
        response = api_request_context.get("/api/productsList")
        return self._parse(response)

    def postToProductsList(self, playwright: Playwright):
        # This method is not supported by the site: we expect responseCode 405
        api_request_context = self._context(playwright)
        response = api_request_context.post("/api/productsList")
        return self._parse(response)

    def searchProduct(self, playwright: Playwright, searchTerm):
        api_request_context = self._context(playwright)
        response = api_request_context.post("/api/searchProduct",
                                            form={"search_product": searchTerm})
        return self._parse(response)
