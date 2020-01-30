import pytest
import uuid
from transactions.models import Account, Transaction
from currencies.models import Currency, ForeignExchangeRate


@pytest.fixture
def test_password():
    return 'strong-test-pass'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'email' not in kwargs:
            kwargs['email'] = '{}@mail.ru'.format(str(uuid.uuid4()))
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def create_currencies(db):
    currencies = ['EUR', 'USD', 'GBP', 'RUB']  # 'BTC'
    for currency in currencies:
        Currency.objects.create(name=currency)


@pytest.fixture
def create_accounts(create_user, create_currencies):
    user1 = create_user()
    user2 = create_user()
    account1 = Account.objects.create(
        user=user1,
        currency_id=1,
        balance=1000,
    )
    account2 = Account.objects.create(
        user=user2,
        currency_id=2,
        balance=1000,
    )
    return account1, account2


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def api_client_with_credentials(db, create_currencies, create_user, api_client):
    user = create_user()
    account = Account.objects.create(
        user=user,
        currency_id=1,
        balance=1000,
    )
    api_client.force_authenticate(user=user)
    yield api_client, user, account
    api_client.force_authenticate(user=None)




