import pytest
from pageObjects.login import LoginPage

CARD = {
    "name": "QA Tester",
    "number": "4111111111111111",
    "cvc": "123",
    "expiry_month": "12",
    "expiry_year": "2030",
}


@pytest.mark.hybrid
def test_hybrid_end_to_end_order(browserInstance, newUser):
    # newUser: the API already created this account before the test starts
    page = browserInstance

    # 1. Login in the browser
    loginPage = LoginPage(page)
    loginPage.navigate()
    homePage = loginPage.login(newUser["email"], newUser["password"])
    homePage.verifyLoggedInAs(newUser["name"])

    # 2. Search for a product and add it to the cart
    productsPage = homePage.openProductsPage()
    productsPage.searchProduct("Men Tshirt")
    productsPage.verifySearchResults("Men Tshirt")
    productsPage.addToCartFromList("Men Tshirt")
    productsPage.continueShopping()

    # 3. Check the cart
    cartPage = productsPage.openCart()
    cartPage.verifyItemCount(1)
    cartPage.verifyItemPresent("Men Tshirt")
    cartPage.verifyPrice("Men Tshirt", "Rs. 400")
    cartPage.verifyQuantity("Men Tshirt", 1)

    # 4. Checkout
    checkoutPage = cartPage.proceedToCheckout()
    checkoutPage.verifyDeliveryAddress(newUser)
    checkoutPage.verifyOrderItem("Men Tshirt")

    # 5. Pay and verify the order
    paymentPage = checkoutPage.placeOrder("Hybrid test order")
    paymentPage.enterCardDetails(CARD)
    paymentPage.confirmOrder()
    paymentPage.verifyOrderPlaced()

    # newUser teardown now deletes the account through the API