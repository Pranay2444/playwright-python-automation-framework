from playwright.sync_api import Page, expect
import re


class LoginPage:

    def __init__(self, page: Page):
        self.page = page

        self.email = page.get_by_test_id("email")
        self.password = page.get_by_test_id("password")
        self.login_submit = page.get_by_test_id("login-submit")
        self.login_form = page.get_by_test_id("login-form")

    def login(self, email: str, password: str):
        self.email.fill(email)
        self.password.fill(password)
        self.login_submit.click()

    def verify_login_page(self):
        expect(self.login_form).to_be_visible()

    def verify_login_successful(self):
        expect(self.page).to_have_url(
            re.compile(r".*/account/?$")
        )