from playwright.sync_api import Page, expect

from pageObjects.checkout import CheckoutPage


class CartPage:

    ROWS = "#cart_info_table tbody tr"

    def __init__(self, page: Page):
        self.page = page

    def _row(self, productName):
        return self.page.locator(self.ROWS).filter(has_text=productName)

    def verifyItemCount(self, expectedCount):
        expect(self.page.locator(self.ROWS)).to_have_count(expectedCount)

    def verifyItemPresent(self, productName):
        expect(self._row(productName)).to_be_visible()

    def verifyPrice(self, productName, expectedPrice):
        expect(self._row(productName).locator(".cart_price")).to_contain_text(expectedPrice)

    def verifyQuantity(self, productName, expectedQuantity):
        expect(self._row(productName).locator(".cart_quantity")).to_have_text(str(expectedQuantity))

    def verifyTotal(self, productName, expectedTotal):
        expect(self._row(productName).locator(".cart_total")).to_contain_text(expectedTotal)

    def removeItem(self, productName):
        self._row(productName).locator(".cart_quantity_delete").click()

    def verifyCartEmpty(self):
        expect(self.page.locator("#empty_cart")).to_be_visible()

    def proceedToCheckout(self):
        self.page.get_by_text("Proceed To Checkout").first.click()
        self.page.wait_for_url("**/checkout", timeout=30000)
        checkoutPage = CheckoutPage(self.page)
        return checkoutPage