from rest_framework import serializers
from .models import User
# from rest_framework.exceptions import PermissionDenied
# from rest_framework_simplejwt.tokens import AccessToken
# from django.shortcuts import get_object_or_404


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True
            }
        }


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'new_password',
            'current_password'
        )


# class AuthSerializer(serializers.ModelSerializer):
#     # username = serializers.CharField(read_only=True)
#     # confirmation_code = serializers.CharField(
#     #     read_only=True, source='confirm_code'
#     # )
#     # token = serializers.CharField(read_only=True)

#     class Meta:
#         model = User
#         fields = ('email', 'password', 'token')

#     def create(self, validated_data):
#         user = get_object_or_404(User, **validated_data)
#         # if user.confirm_code != validated_data.get("confirmation_code"):
#         #     raise PermissionDenied('Код подтверждния или учетная запись')
#         token = AccessToken.for_user(user)
#         return token
