import re

from playwright.sync_api import Page, expect


class CatalogPage:
    def __init__(self, page: Page):
        self.page = page
        self.products = page.locator('[data-test^="product-"]')

    def open(self) -> None:
        self.page.goto("/", wait_until="domcontentloaded")

    def verify_catalog_page_loaded(self) -> None:
        expect(self.page).to_have_title(
            re.compile("Toolshop", re.IGNORECASE)
        )

    def verify_products_are_displayed(self) -> None:
        expect(self.products.first).to_be_visible()
        assert self.products.count() > 0