from rest_framework import serializers
from . import models
from .exceptions import CustomException
from currencies.models import ForeignExchangeRate
from django.db import DatabaseError, transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = (
            'id',
            'from_account',
            'to_account',
            'amount',
            'status',
            'date',
        )


def convert(from_currency, to_currency, amount):
    rate = ForeignExchangeRate.objects.get(
        base=from_currency,
        rate_currency=to_currency,
    )

    # if from_currency != 'EUR':
    #     amount = amount / self.rates[from_currency]

    to_amount = round(amount * rate.val, 2)
    print('{} {} = {} {}'.format(amount, from_currency, to_amount, to_currency))
    return to_amount


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = (
            'id',
            'from_account',
            'to_account',
            'amount',
        )

    def validate(self, attrs):
        user = self.context.get('user')
        from_account = attrs.get('from_account')
        amount = attrs.get('amount')

        if from_account not in user.account_set.all():
            raise CustomException(detail='forbidden1')

        if from_account.balance < amount:
            raise CustomException(detail='not_enough')

        return attrs

    def create(self, validated_data):
        from_account = validated_data.get('from_account')
        to_account = validated_data.get('to_account')

        with transaction.atomic():
            trans = models.Transaction.objects.create(
                status=2,
                **validated_data
            )

            from_account.balance -= trans.amount
            from_account.save()

            if from_account.currency == to_account.currency:
                """Если валюты отправителя и получателя одинаковые"""
                to_account.balance += trans.amount
                to_account.save()
            else:
                to_amount = convert(from_account.currency,
                                    to_account.currency,
                                    trans.amount)
                to_account.balance += to_amount
                to_account.save()

        return trans
