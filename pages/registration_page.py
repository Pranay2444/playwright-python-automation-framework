from playwright.sync_api import Page, expect
import re


class RegistrationPage:

    def __init__(self, page: Page):
        self.page = page

        # Locators
        self.nav_sign_in = page.get_by_test_id("nav-sign-in")
        self.register_link = page.get_by_test_id("register-link")

        self.first_name = page.get_by_test_id("first-name")
        self.last_name = page.get_by_test_id("last-name")
        self.dob = page.get_by_test_id("dob")
        self.country = page.get_by_test_id("country")
        self.postal_code = page.get_by_test_id("postal_code")
        self.house_number = page.get_by_test_id("house_number")
        self.street = page.get_by_test_id("street")
        self.city = page.get_by_test_id("city")
        self.state = page.get_by_test_id("state")
        self.phone = page.get_by_test_id("phone")
        self.email = page.get_by_test_id("email")
        self.password = page.get_by_test_id("password")

        self.register_submit = page.get_by_test_id("register-submit")

    def open(self):
        self.page.goto("/", wait_until="domcontentloaded")
        self.nav_sign_in.click()
        self.register_link.click()

    def register_user(self, user: dict):
        self.first_name.fill(user["first_name"])
        self.last_name.fill(user["last_name"])
        self.dob.fill(user["dob"])

        self.country.select_option(user["address"]["country"])

        self.postal_code.fill(user["address"]["postal_code"])
        self.house_number.fill(user["address"]["house_number"])
        self.street.fill(user["address"]["street"])
        self.city.fill(user["address"]["city"])
        self.state.fill(user["address"]["state"])

        self.phone.fill(user["phone"])
        self.email.fill(user["email"])
        self.password.fill(user["password"])

        self.register_submit.click()

    def verify_registration_successful(self):
        expect(self.page).to_have_url(
            re.compile(r".*/auth/login/?$")
        )

        expect(
            self.page.get_by_test_id("login-form")
        ).to_be_visible()