from rest_framework import serializers
from .models import User, Subscribe
from recipes.models import Recipe
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed',
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True
            }
        }

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        subscribe = Subscribe.objects.filter(
            user_id=user,
            subscribing_user_id=obj
        ).first()
        if subscribe:
            return True
        return False


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'new_password',
            'current_password'
        )


class SubscribeSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    id = serializers.IntegerField(
        source='subscribing_user_id.id',
        required=False)

    class Meta:
        model = Subscribe
        fields = (
            'email',
            'id',
            'subscribing_user_id',
            'user_id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        extra_kwargs = {
            'subscribing_user_id': {
                'write_only': True,
                'required': True
            },
            'user_id': {
                'write_only': True,
                'required': True
            },
        }
        validators = [
            UniqueTogetherValidator(
                queryset=Subscribe.objects.all(),
                fields=('user_id', 'subscribing_user_id'),
                message='This following already exists.'
            )
        ]

    def get_username(self, obj):
        return User.objects.get(id=obj.subscribing_user_id.id).username

    def get_first_name(self, obj):
        return User.objects.get(id=obj.subscribing_user_id.id).first_name

    def get_last_name(self, obj):
        return User.objects.get(id=obj.subscribing_user_id.id).last_name

    def get_email(self, obj):
        return User.objects.get(id=obj.subscribing_user_id.id).last_name

    def get_is_subscribed(self, obj):
        return True

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj.id)
        return RecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.id).count()

    def validate_subscribing_user_id(self, obj):
        subscribing = get_object_or_404(User, username=obj)
        if (self.initial_data.get('user_id') == subscribing.id):
            raise serializers.ValidationError('Нельзя подписаться на себя')
        return subscribing
