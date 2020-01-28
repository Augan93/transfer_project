from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Transaction(models.Model):
    PENDING = 0
    EXECUTED = 1
    FAILED = 2

    STATUS_CHOICES = (
        (PENDING, 'Pengind'),
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='my_transactions',
        verbose_name='Отправитель',
    )
    recipient = models.ForeignKey(
        User,
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
        return '{} -> {}: {}'.format(self.sender,
                                     self.recipient,
                                     self.amount)

