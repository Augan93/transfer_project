from django.db import models
from django.contrib.auth import get_user_model
from currencies.models import Currency

User = get_user_model()


class Account(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    balance = models.FloatField(
        verbose_name='начальный баланс',
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        verbose_name='валюта счета',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата открытия',
    )

    def __str__(self):
        return '{} - {} {}'.format(self.user,
                                   self.balance,
                                   self.currency)

    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'


class Transaction(models.Model):
    PENDING = 0
    EXECUTED = 1
    FAILED = 2

    STATUS_CHOICES = (
        (PENDING, 'Penging'),
        (EXECUTED, 'EXECUTED'),
        (FAILED, 'FAILED'),
    )

    from_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='my_transactions',
        verbose_name='Отправитель',
    )
    to_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        verbose_name='Получатель',
    )
    amount = models.FloatField(
        verbose_name='Сумма',
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        verbose_name='Статус',
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата совершения',
    )

    def __str__(self):
        return '{} -> {}: {}'.format(self.from_account,
                                     self.to_account,
                                     self.amount)

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
