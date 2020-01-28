from django.contrib import admin
from . import models


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'sender',
        'recipient',
        'amount',
        'status',
        'date',
    )
