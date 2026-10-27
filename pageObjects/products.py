from playwright.sync_api import Page, expect

from pageObjects.cart import CartPage

class ProductsPage:

    def __init__(self, page: Page):
        self.page = page

    def openCategory(self, category, subcategory):
        # e.g. openCategory("Men", "Tshirts")
        self.page.locator(f'a[href="#{category}"]').click()
        self.page.locator(f"#{category}").get_by_role("link", name=subcategory).click()

    def searchProduct(self, searchTerm):
        self.page.goto("https://automationexercise.com/products")
        self.page.locator("#search_product").fill(searchTerm)
        self.page.locator("#submit_search").click()

    def verifySearchResults(self, expectedName):
        results = self.page.locator("div.col-sm-4").filter(has_text=expectedName)
        expect(results.first).to_be_visible()

    def viewProduct(self, name):
        card = self.page.locator("div.col-sm-4").filter(has_text=name)
        card.get_by_role("link", name="View Product").first.click()
        self.page.wait_for_load_state("load")

    def addToCartFromDetails(self):
        # on the product details page
        self.page.get_by_role("button", name="Add to cart").click()

    def addToCartFromList(self, name):
        # on a product list page, without opening the details
        card = self.page.locator("div.col-sm-4").filter(has_text=name).first
        card.hover()
        overlayLink = card.locator(".product-overlay a.add-to-cart")
        expect(overlayLink).to_be_visible()
        overlayLink.click()

    def continueShopping(self):
        modal = self.page.locator("#cartModal")
        expect(modal).to_be_visible(timeout=15000)
        modal.get_by_role("button", name="Continue Shopping").click()

    def openCart(self):
        self.page.get_by_role("link", name="Cart").first.click()
        cartPage = CartPage(self.page)
        return cartPage