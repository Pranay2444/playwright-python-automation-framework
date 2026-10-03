from typing import Any
from uuid import uuid4

import pytest
from playwright.sync_api import APIRequestContext


@pytest.fixture
def user_data() -> dict[str, Any]:
    return {
        "first_name": "Test",
        "last_name": "Learner",
        "email": f"qa_{uuid4().hex}@example.com",
        "password": f"Qa!{uuid4().hex}9",
        "dob": "2000-01-01",
        "phone": "1234567890",
        "address": {
            "street": "Test Street",
            "house_number": "12",
            "city": "Pune",
            "state": "Maharashtra",
            "country": "IN",
            "postal_code": "411001",
        },
    }


@pytest.fixture
def registered_user(
    api_context: APIRequestContext,
    user_data: dict[str, Any],
) -> dict[str, Any]:

    response = api_context.post(
        "/users/register",
        data=user_data
    )

    assert response.status == 201

    return user_data