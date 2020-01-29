from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers
from transactions.models import Account
from currencies.models import Currency

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
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {
                    "Error": "Пароли не совпадают"
                }
            )
        password2 = data['password2']
        password_validation.validate_password(password2)

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


# class PasswordChangeSerializer(serializers.ModelSerializer):
#     oldPassword = serializers.CharField()
#     passwordConfirm = serializers.CharField()
#
#     class Meta:
#         model = User
#         fields = (
#             'id',
#             'oldPassword',
#             'password',
#             'passwordConfirm',
#         )
#
#     def validate(self, data):
#         user = self.context.get('request').user
#
#         if not user.check_password(data['oldPassword']):
#             raise CustomException(detail=3)  # wrong_old_password
#
#         if data['password'] != data['passwordConfirm']:
#             raise CustomException(detail=2)  # password_mismatch
#         password_validation.validate_password(data['password'])
#         return data
#
#     def create(self, validated_data):
#         user = self.context.get('request').user
#         user.set_password(validated_data['password'])
#         user.save()
#
#         user.profile.password_changed = True
#         user.profile.save()
#
#         return user


