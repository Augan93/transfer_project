from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from . import models
from . import serializers
from django.db.models import Q


class TransferView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        serializer = serializers.TransferSerializer(data=request.data,
                                                    context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class MyTransactionsListView(generics.ListAPIView):
    """Получить все мои оперции"""
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer

    def get_queryset(self):
        accounts = self.request.user.account_set.all()

        return self.queryset.filter(Q(from_account__in=accounts) | Q(to_account__in=accounts))

