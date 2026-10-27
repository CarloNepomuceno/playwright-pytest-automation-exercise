from playwright.sync_api import expect
from pageObjects.products import ProductsPage

class HomePage:

    def __init__(self, page):
        self.page = page

    def verifyLoggedInAs(self, name):
        expect(self.page.locator("a", has_text=f"Logged in as {name}")).to_be_visible()

    def openProductsPage(self):
        self.page.locator('a[href="/products"]').first.click()
        productsPage = ProductsPage(self.page)
        return productsPage