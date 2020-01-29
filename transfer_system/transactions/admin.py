from django.contrib import admin
from . import models


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'from_account',
        'to_account',
        'amount',
        'status',
        'date',
    )


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'balance',
        'currency',
        'created_at',
    )
