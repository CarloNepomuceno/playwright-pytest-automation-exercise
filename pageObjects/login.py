from playwright.sync_api import expect

from pageObjects.home import HomePage
from pageObjects.signup import SignupPage

BASE_URL = "https://automationexercise.com"


class LoginPage:

    def __init__(self, page):
        self.page = page

    def navigate(self):
        self.page.goto(f"{BASE_URL}/login", wait_until="domcontentloaded", timeout=60000)

    def login(self, userEmail, userPassword):
        self.page.locator('[data-qa="login-email"]').wait_for(timeout=60000)
        self.page.locator('[data-qa="login-email"]').fill(userEmail)
        self.page.locator('[data-qa="login-password"]').fill(userPassword)
        self.page.locator('[data-qa="login-button"]').click()
        homePage = HomePage(self.page)
        return homePage

    def verifyLoginError(self):
        expect(self.page.get_by_text("Your email or password is incorrect!")).to_be_visible()

    def startSignup(self, name, email):
        self.page.locator('[data-qa="signup-name"]').fill(name)
        self.page.locator('[data-qa="signup-email"]').fill(email)
        self.page.locator('[data-qa="signup-button"]').click()
        signupPage = SignupPage(self.page)
        return signupPage