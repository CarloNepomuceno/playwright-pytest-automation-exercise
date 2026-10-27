from playwright.sync_api import Page, expect


class PaymentPage:

    def __init__(self, page: Page):
        self.page = page

    def enterCardDetails(self, card):
        self.page.locator('[data-qa="name-on-card"]').fill(card["name"])
        self.page.locator('[data-qa="card-number"]').fill(card["number"])
        self.page.locator('[data-qa="cvc"]').fill(card["cvc"])
        self.page.locator('[data-qa="expiry-month"]').fill(card["expiry_month"])
        self.page.locator('[data-qa="expiry-year"]').fill(card["expiry_year"])

    def confirmOrder(self):
        self.page.locator('[data-qa="pay-button"]').click()

    def verifyOrderPlaced(self):
        expect(self.page.locator('[data-qa="order-placed"]')).to_contain_text(
            "Order Placed!", ignore_case=True)