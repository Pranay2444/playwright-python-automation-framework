import pytest

from pages.account_page import AccountPage
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage


@pytest.mark.ui
@pytest.mark.regression
def test_new_user_can_register_and_log_in(
    registration_page: RegistrationPage,
    login_page: LoginPage,
    account_page: AccountPage,
    user_data: dict,
) -> None:

    registration_page.open()
    registration_page.register_user(user_data)
    registration_page.verify_registration_successful()

    login_page.login(
        user_data["email"],
        user_data["password"],
    )
    login_page.verify_login_successful()

    account_page.verify_account_page()
    account_page.verify_logged_in_user(
        user_data["first_name"],
        user_data["last_name"],
    )