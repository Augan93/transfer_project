from transfer_system.celery import app

import requests
from . import models


site_url = 'https://api.exchangeratesapi.io/latest?base={base}&symbols={currencies}'


def get_exchange_rates():
    currencies = models.Currency.objects.all()
    for cur in currencies:
        rate_currencies = currencies.exclude(pk=cur.pk)
        symbols = ''
        for i, item in enumerate(rate_currencies):
            symbols += item.name + ','

        url = site_url.format(base=cur.name,
                              currencies=symbols[:len(symbols)-1])
        resp = requests.get(url).json()
        print(resp)
        for rate_currency_name, val in resp['rates'].items():
            print(rate_currency_name, val)
            rate_currency = models.Currency.objects.get(name=rate_currency_name)
            try:
                exchange_rate = models.ForeignExchangeRate.objects.get(
                    base=cur,
                    rate_currency=rate_currency,
                )
                exchange_rate.val = val
                exchange_rate.date = resp['date']
                exchange_rate.save()
            except models.ForeignExchangeRate.DoesNotExist:
                models.ForeignExchangeRate.objects.create(
                    base=cur,
                    rate_currency=rate_currency,
                    val=val,
                    date=resp['date'],
                )


@app.task
def get_rates():
    get_exchange_rates()
    print("Hello there!")
