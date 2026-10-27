import pytest
from pageObjects.login import LoginPage

CARD = {
    "name": "QA Tester",
    "number": "4111111111111111",
    "cvc": "123",
    "expiry_month": "12",
    "expiry_year": "2030",
}


@pytest.mark.ui
def test_place_order(page, newUser):
    loginPage = LoginPage(page)
    loginPage.navigate()
    homePage = loginPage.login(newUser["email"], newUser["password"])
    homePage.verifyLoggedInAs(newUser["name"])

    productsPage = homePage.openProductsPage()
    productsPage.openCategory("Men", "Tshirts")
    productsPage.viewProduct("Men Tshirt")
    productsPage.addToCartFromDetails()
    productsPage.continueShopping()

    cartPage = productsPage.openCart()
    checkoutPage = cartPage.proceedToCheckout()
    checkoutPage.verifyDeliveryAddress(newUser)
    checkoutPage.verifyOrderItem("Men Tshirt")

    paymentPage = checkoutPage.placeOrder("Please pack carefully")
    paymentPage.enterCardDetails(CARD)
    paymentPage.confirmOrder()
    paymentPage.verifyOrderPlaced()