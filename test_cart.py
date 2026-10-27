import pytest
from pageObjects.login import LoginPage

@pytest.mark.smoke
@pytest.mark.ui
def test_add_product_to_cart(page, newUser):
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
    cartPage.verifyItemCount(1)
    cartPage.verifyItemPresent("Men Tshirt")
    cartPage.verifyPrice("Men Tshirt", "Rs. 400")
    cartPage.verifyQuantity("Men Tshirt", 1)