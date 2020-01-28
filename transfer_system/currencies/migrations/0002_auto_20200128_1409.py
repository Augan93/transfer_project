# Generated by Django 3.0.2 on 2020-01-28 08:09

from django.db import migrations


def create_currencies(apps, schema_editor):
    currencies = ['EUR', 'USD', 'GBP', 'RUB']  # 'BTC'
    Currency = apps.get_model('currencies', 'Currency')
    for currency in currencies:
        Currency.objects.create(name=currency)
        # print('{} created'.format(currency))


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_currencies),
    ]
