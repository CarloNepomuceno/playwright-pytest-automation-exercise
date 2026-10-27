import pytest
from pytest_bdd import given, when, then, parsers, scenarios

from pageObjects.login import LoginPage

scenarios('Features/purchase.feature')

CARD = {
    "name": "QA Tester",
    "number": "4111111111111111",
    "cvc": "123",
    "expiry_month": "12",
    "expiry_year": "2030",
}


@pytest.fixture
def shared_data():
    return {}


@given('a registered user exists')
def registered_user(newUser, shared_data):
    # newUser already created the account through the API
    shared_data['user'] = newUser


@given('the user is on the login page')
def user_on_login_page(browserInstance, shared_data):
    loginPage = LoginPage(browserInstance)
    loginPage.navigate()
    shared_data['login_page'] = loginPage


@when('I log in with the registered user')
def login_with_registered_user(shared_data):
    user = shared_data['user']
    homePage = shared_data['login_page'].login(user['email'], user['password'])
    homePage.verifyLoggedInAs(user['name'])
    shared_data['home_page'] = homePage


@when(parsers.parse('I search for {product} and add it to the cart'))
def search_and_add_to_cart(product, shared_data):
    productsPage = shared_data['home_page'].openProductsPage()
    productsPage.searchProduct(product)
    productsPage.verifySearchResults(product)
    productsPage.addToCartFromList(product)
    productsPage.continueShopping()
    shared_data['products_page'] = productsPage
    shared_data['product'] = product


@when('I check out and pay with a test card')
def check_out_and_pay(shared_data):
    cartPage = shared_data['products_page'].openCart()
    cartPage.verifyItemPresent(shared_data['product'])
    checkoutPage = cartPage.proceedToCheckout()
    checkoutPage.verifyDeliveryAddress(shared_data['user'])
    paymentPage = checkoutPage.placeOrder("BDD order")
    paymentPage.enterCardDetails(CARD)
    paymentPage.confirmOrder()
    shared_data['payment_page'] = paymentPage


@then('the order is placed successfully')
def order_placed_successfully(shared_data):
    shared_data['payment_page'].verifyOrderPlaced()