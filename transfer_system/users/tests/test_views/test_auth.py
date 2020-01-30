import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_unauthorized_request(api_client):
    url = reverse('transactions:my_operations')
    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_authorized_request(api_client_with_credentials):
    url = reverse('transactions:my_operations')
    api_client, user, account = api_client_with_credentials
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.fixture
def login_data(test_password):
    data = {
        "email": "test@mail.ru",
        "password": test_password,
    }
    return data


@pytest.fixture
def wrong_login_data(test_password):
    data = {
        "email": "test@mail.ru",
        "password": "wrong_password",
    }
    return data


@pytest.mark.django_db
def test_login(api_client, login_data, create_user):
    create_user(email='test@mail.ru')
    url = reverse('users:login')
    response = api_client.post(url,
                               data=login_data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_wrong_login_data(api_client, wrong_login_data, create_user):
    create_user(email='test@mail.ru')
    url = reverse('users:login')
    response = api_client.post(url,
                               data=wrong_login_data)
    assert response.status_code == 400
    assert 'wrong_username_or_password' == response.data['message']
