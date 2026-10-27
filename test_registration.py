import pytest
from pageObjects.login import LoginPage


@pytest.mark.ui
def test_register_new_user(page, registrationUser):
    loginPage = LoginPage(page)
    loginPage.navigate()

    signupPage = loginPage.startSignup(registrationUser["name"], registrationUser["email"])
    signupPage.fillAccountInformation(registrationUser)
    signupPage.fillAddressInformation(registrationUser)
    signupPage.createAccount()
    signupPage.verifyAccountCreated()

    homePage = signupPage.continueToHome()
    homePage.verifyLoggedInAs(registrationUser["name"])