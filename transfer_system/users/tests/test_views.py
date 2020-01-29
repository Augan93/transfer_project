import pytest
from django.urls import reverse


@pytest.fixture
def valid_user_data():
    data = {
        "email": "diko@mail.ru",
        "password": "auganenu123",
        "password2": "auganenu123",
        "balance": 20000,
        "currency": 2
    }
    return data


@pytest.fixture
def minus_balance_user_data():
    data = {
        "email": "diko@mail.ru",
        "password": "auganenu123",
        "password2": "auganenu123",
        "balance": -20000,
        "currency": 2
    }
    return data


@pytest.mark.django_db
def test_register(api_client, user_data):
    """Тест регистрации пользователя"""
    url = reverse('users:register')
    response = api_client.post(url, data=user_data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_register_minus_balance(api_client, minus_balance_user_data):
    """Тест регистрации пользователя"""
    url = reverse('users:register')
    response = api_client.post(url, data=minus_balance_user_data)
    assert response.status_code == 400
    assert 'zero' == response.data['message']
    print(response.data['message'])

