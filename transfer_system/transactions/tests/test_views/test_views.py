import pytest
from django.urls import reverse
from transactions.models import Transaction


@pytest.fixture
def create_transactions(api_client_with_credentials, create_accounts):
    account1, account2 = create_accounts
    api_client, user, account = api_client_with_credentials
    Transaction.objects.create(
        from_account=account,
        to_account=account1,
        amount=100,
        status=1,
    )
    return api_client


@pytest.mark.django_db
def test_get_my_transactions(create_transactions):
    url = reverse('transactions:my_operations')
    api_client = create_transactions
    resp = api_client.get(url)
    assert resp.status_code == 200
    assert len(resp.data) == 1
    print(resp.data)


@pytest.mark.django_db
def test_transform(api_client_with_credentials, create_accounts):
    account1, account2 = create_accounts
    api_client, user, account = api_client_with_credentials
    url = reverse('transactions:transfer')
    data = {
        "from_account": account.id,
        "to_account": account1.id,
        "amount": 100
    }
    resp = api_client.post(url, data=data)
    assert resp.status_code == 201


@pytest.mark.django_db
def test_transform_forbidden(api_client_with_credentials, create_accounts):
    account1, account2 = create_accounts
    api_client, user, account = api_client_with_credentials
    url = reverse('transactions:transfer')
    data = {
        "from_account": account2.id,
        "to_account": account1.id,
        "amount": 100
    }
    resp = api_client.post(url, data=data)
    assert resp.status_code == 403


@pytest.mark.django_db
def test_transform_not_enough_balance(api_client_with_credentials, create_accounts):
    account1, account2 = create_accounts
    api_client, user, account = api_client_with_credentials
    url = reverse('transactions:transfer')
    data = {
        "from_account": account.id,
        "to_account": account1.id,
        "amount": 100000
    }
    resp = api_client.post(url, data=data)
    assert resp.status_code == 400

