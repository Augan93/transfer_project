from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('transfer/', views.TransferView.as_view(), name='transfer'),
    path('my/', views.MyTransactionsListView.as_view(), name='my_operations'),
]
