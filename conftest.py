"""Shared setup: pytest discovers this file automatically."""

from collections.abc import Generator
from typing import Any

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from config.settings import API_BASE_URL, BASE_URL, PW_PROXY_SERVER, REQUEST_TIMEOUT_MS


@pytest.fixture(scope="session", autouse=True)
def configure_test_ids(playwright: Playwright) -> None:
    # Toolshop uses data-test="..." rather than the default data-testid="...".
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict[str, Any]) -> dict[str, Any]:
    # Extend the plugin's options so options such as device emulation still work.
    options = {**browser_context_args, "base_url": BASE_URL}
    if PW_PROXY_SERVER:
        options["proxy"] = {"server": PW_PROXY_SERVER}
    return options


@pytest.fixture
def api_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    # Standalone API requests do not need a browser or share browser cookies.
    context = playwright.request.new_context(
        base_url=API_BASE_URL,
        extra_http_headers={"Accept": "application/json"},
        timeout=REQUEST_TIMEOUT_MS,
        proxy={"server": PW_PROXY_SERVER} if PW_PROXY_SERVER else None,
    )
    try:
        yield context
    finally:
        # Free response bodies/connections even if a test assertion fails.
        context.dispose()
