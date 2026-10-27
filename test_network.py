import time

import pytest
from pageObjects.login import LoginPage


@pytest.mark.network
def test_shopping_works_without_images(browserInstance, newUser):
    page = browserInstance
    blocked = []

    def block_images(route):
        if route.request.resource_type == "image":
            blocked.append(route.request.url)
            route.abort()
        else:
            route.fallback()

    page.route("**/*", block_images)

    loginPage = LoginPage(page)
    loginPage.navigate()
    homePage = loginPage.login(newUser["email"], newUser["password"])
    homePage.verifyLoggedInAs(newUser["name"])

    productsPage = homePage.openProductsPage()
    productsPage.addToCartFromList("Men Tshirt")
    productsPage.continueShopping()
    cartPage = productsPage.openCart()
    cartPage.verifyItemPresent("Men Tshirt")

    assert len(blocked) > 0, "No image requests were intercepted"
    time.sleep(4)

@pytest.mark.network
def test_cart_stays_empty_when_add_to_cart_request_fails(browserInstance, newUser):
    page = browserInstance

    page.route("**/add_to_cart/*", lambda route: route.abort())

    loginPage = LoginPage(page)
    loginPage.navigate()
    homePage = loginPage.login(newUser["email"], newUser["password"])
    productsPage = homePage.openProductsPage()
    productsPage.addToCartFromList("Men Tshirt")

    cartPage = productsPage.openCart()
    cartPage.verifyCartEmpty()
    time.sleep(4)

