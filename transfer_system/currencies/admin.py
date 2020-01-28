from django.contrib import admin
from . import models


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(models.ForeignExchangeRate)
class ForeignExchangeRateAdmin(admin.ModelAdmin):
    list_filter = (
        'base',
    )
    list_display = (
        'base',
        'rate_currency',
        'val',
        'date',
    )

