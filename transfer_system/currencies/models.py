from django.db import models


class Currency(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'


# EUR, USD, GPB, RUB, BTC


class ForeignExchangeRate(models.Model):
    base = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='rates',
        verbose_name='Основа',
    )
    rate_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        verbose_name='Валюта',
    )
    val = models.FloatField(
        verbose_name='Значение',
    )
    date = models.DateField(
        verbose_name='Дата',
    )

    def __str__(self):
        return '{} - {} {}'.format(self.base,
                                   self.val,
                                   self.rate_currency)

    class Meta:
        verbose_name = 'Курс валюты'
        verbose_name_plural = 'Курсы валют'
        unique_together = (
            'base',
            'rate_currency',
        )

