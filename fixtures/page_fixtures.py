import pytest
from playwright.sync_api import Page

from pages.catalog_page import CatalogPage
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from pages.account_page import AccountPage


@pytest.fixture
def catalog_page(page: Page) -> CatalogPage:
    return CatalogPage(page)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def registration_page(page: Page) -> RegistrationPage:
    return RegistrationPage(page)

@pytest.fixture
def account_page(page: Page) -> AccountPage:
    return AccountPage(page)