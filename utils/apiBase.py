import json
import time
import uuid

from playwright.sync_api import Playwright

BASE_URL = "https://automationexercise.com"


class APIUtils:

    """ Notes about this site's API:
    - Requests are sent as form data (form=...), not JSON.
    - The real result is in the body's "responseCode", not the HTTP status.
    - Some responses come back as text/html, so we parse response.text() ourselves.
    """

    def buildUser(self, profile):
        # Unique email per run so reruns and parallel tests never collide
        user = dict(profile)
        user["email"] = f"qa_{uuid.uuid4().hex[:8]}@example.com"
        return user

    def _context(self, playwright: Playwright):
        return playwright.request.new_context(base_url=BASE_URL)

    def _send(self, playwright: Playwright, method, url, **kwargs):
        # method is "get", "post" or "delete"
        api_request_context = self._context(playwright)
        text = ""
        try:
            for attempt in range(3):
                response = getattr(api_request_context, method)(url, **kwargs)
                text = response.text()
                if text.lstrip().startswith("{"):
                    return json.loads(text)
                time.sleep(3)  # got an HTML page, wait and try again
        finally:
            api_request_context.dispose()
        raise AssertionError(f"{method.upper()} {url} kept returning a non-JSON page: {text[:150]}")

    def createAccount(self, playwright: Playwright, user):
        return self._send(playwright, "post", "/api/createAccount", form=user)

    def deleteAccount(self, playwright: Playwright, email, password):
        return self._send(playwright, "delete", "/api/deleteAccount",
                          form={"email": email, "password": password})

    def verifyLogin(self, playwright: Playwright, email=None, password=None):
        form = {}
        if email is not None:
            form["email"] = email
        if password is not None:
            form["password"] = password
        return self._send(playwright, "post", "/api/verifyLogin", form=form)

    def getUserByEmail(self, playwright: Playwright, email):
        return self._send(playwright, "get", "/api/getUserDetailByEmail", params={"email": email})

    def getProductsList(self, playwright: Playwright):
        return self._send(playwright, "get", "/api/productsList")

    def postToProductsList(self, playwright: Playwright):
        # This method is not supported by the site: we expect responseCode 405
        return self._send(playwright, "post", "/api/productsList")

    def searchProduct(self, playwright: Playwright, searchTerm):
        return self._send(playwright, "post", "/api/searchProduct",
                          form={"search_product": searchTerm})