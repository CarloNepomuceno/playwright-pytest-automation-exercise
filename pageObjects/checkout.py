from playwright.sync_api import Page, expect

from pageObjects.payment import PaymentPage


class CheckoutPage:

    def __init__(self, page: Page):
        self.page = page

    def verifyDeliveryAddress(self, user):
        address = self.page.locator("#address_delivery")
        expect(address).to_contain_text(user["firstname"])
        expect(address).to_contain_text(user["lastname"])
        expect(address).to_contain_text(user["address1"])
        expect(address).to_contain_text(user["city"])
        expect(address).to_contain_text(user["country"])

    def verifyOrderItem(self, productName):
        row = self.page.locator("#cart_info tbody tr").filter(has_text=productName)
        expect(row).to_be_visible()

    def placeOrder(self, comment=""):
        if comment:
            self.page.locator('textarea[name="message"]').fill(comment)
        self.page.locator('a[href="/payment"]').click()
        paymentPage = PaymentPage(self.page)
        return paymentPage