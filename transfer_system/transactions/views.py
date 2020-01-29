from rest_framework import generics
from rest_framework import status
from . import models
from . import serializers
from django.db.models import Q


class SendMoneyView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        pass


class MyTransactionsListView(generics.ListAPIView):
    """Получить все мои оперции"""
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer

    def get_queryset(self):
        accounts = self.request.user.account_set.all()

        return self.queryset.filter(Q(from_account__in=accounts) | Q(to_account__in=accounts))

