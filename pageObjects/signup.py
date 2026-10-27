from playwright.sync_api import Page, expect

from pageObjects.home import HomePage


class SignupPage:

    def __init__(self, page: Page):
        self.page = page

    def fillAccountInformation(self, user):
        genderId = "#id_gender1" if user["title"] == "Mr" else "#id_gender2"
        self.page.locator(genderId).check()
        self.page.locator('[data-qa="password"]').fill(user["password"])
        self.page.locator('[data-qa="days"]').select_option(user["birth_date"])
        self.page.locator('[data-qa="months"]').select_option(user["birth_month"])
        self.page.locator('[data-qa="years"]').select_option(user["birth_year"])

    def fillAddressInformation(self, user):
        self.page.locator('[data-qa="first_name"]').fill(user["firstname"])
        self.page.locator('[data-qa="last_name"]').fill(user["lastname"])
        self.page.locator('[data-qa="company"]').fill(user["company"])
        self.page.locator('[data-qa="address"]').fill(user["address1"])
        self.page.locator('[data-qa="address2"]').fill(user["address2"])
        self.page.locator('[data-qa="country"]').select_option(user["country"])
        self.page.locator('[data-qa="state"]').fill(user["state"])
        self.page.locator('[data-qa="city"]').fill(user["city"])
        self.page.locator('[data-qa="zipcode"]').fill(user["zipcode"])
        self.page.locator('[data-qa="mobile_number"]').fill(user["mobile_number"])

    def createAccount(self):
        self.page.locator('[data-qa="create-account"]').click()

    def verifyAccountCreated(self):
        expect(self.page.locator('[data-qa="account-created"]')).to_contain_text(
            "Account Created!", ignore_case=True)

    def continueToHome(self):
        self.page.locator('[data-qa="continue-button"]').click()
        homePage = HomePage(self.page)
        return homePage