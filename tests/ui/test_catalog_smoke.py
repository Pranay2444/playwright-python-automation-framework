"""Day 1 deliberately uses direct locators; extract a POM on Day 2."""

import re

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.ui
@pytest.mark.smoke
def test_catalog_displays_products(page: Page) -> None:
    page.goto("/", wait_until="domcontentloaded")

    expect(page).to_have_title(re.compile("Toolshop", re.IGNORECASE))
    # The first locator is a property in Python: .first, not .first().
    products = page.locator('[data-test^="product-"]')
    expect(products.first).to_be_visible()
    assert products.count() > 0
