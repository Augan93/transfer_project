from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers
from transactions.models import Account
from currencies.models import Currency
from transactions.exceptions import CustomException

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'},
    )
    balance = serializers.FloatField()
    currency = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(),
    )

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
            'password2',
            'balance',
            'currency',
        )

    def validate(self, data):
        balance = data.get('balance')

        if data['password'] != data['password2']:
            raise CustomException(detail="password_mismatch")
        password2 = data['password2']
        password_validation.validate_password(password2)

        if balance < 0:
            raise CustomException(detail='zero')

        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        balance = validated_data.pop('balance')
        currency = validated_data.pop('currency')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        Account.objects.create(
            user=user,
            balance=balance,
            currency=currency,
        )

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
    )
    password = serializers.CharField(
        required=True,
    )



