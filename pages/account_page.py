from playwright.sync_api import Page, expect


class AccountPage:

    def __init__(self, page: Page):
        self.page = page

        self.page_title = page.get_by_test_id("page-title")
        self.nav_menu = page.get_by_test_id("nav-menu")

    def verify_account_page(self):
        expect(self.page_title).to_have_text("My account")

    def verify_logged_in_user(
        self,
        first_name: str,
        last_name: str
    ):
        expect(self.nav_menu).to_contain_text(
            f"{first_name} {last_name}"
        )