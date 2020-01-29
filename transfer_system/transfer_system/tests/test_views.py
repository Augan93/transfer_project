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
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200


