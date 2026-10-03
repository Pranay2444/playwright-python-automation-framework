import pytest

from pages.catalog_page import CatalogPage


@pytest.mark.ui
@pytest.mark.smoke
def test_catalog_displays_products(
    catalog_page: CatalogPage
) -> None:

    catalog_page.open()

    catalog_page.verify_catalog_page_loaded()

    catalog_page.verify_products_are_displayed()