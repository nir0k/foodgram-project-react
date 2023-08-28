import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.serializer import UserSerializer

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag, TagRecipe)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class IngredientRecipeSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')
    id = serializers.IntegerField(source='ingredient.id')

    class Meta():
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
    )
    tags_show = TagSerializer(read_only=True, many=True, source='tags')
    ingredients = IngredientRecipeSerializer(many=True,
                                             source='recipe_ingredients')
    image = Base64ImageField(required=True, allow_null=True)
    is_in_shopping_cart = serializers.BooleanField(required=False)
    is_favorited = serializers.BooleanField(required=False)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'tags_show',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'image',
            'name',
            'text',
            'cooking_time')
        read_only_fields = (
            'is_favorited',
            'is_in_shopping_cart',
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['tags'] = response.pop('tags_show')
        return response

    def list_of_ingredients(self, recipe, ingredients_data):
        for ingredient_data in ingredients_data:
            ingredient = get_object_or_404(
                Ingredient,
                pk=ingredient_data.get('ingredient').get('id')
            )
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=ingredient_data.get('amount')
            )

    def list_of_tags(self, recipe, tags_data):
        for tag_data in tags_data:
            tag = get_object_or_404(Tag, pk=tag_data.id)
            TagRecipe.objects.create(recipe=recipe, tag=tag)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.list_of_tags(recipe=recipe, tags_data=tags_data)
        self.list_of_ingredients(
            recipe=recipe, ingredients_data=ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients')
        tags_data = validated_data.pop('tags')
        super().update(instance, validated_data)
        instance.ingredients.clear()
        instance.tags.clear()
        self.list_of_tags(recipe=instance, tags_data=tags_data)
        self.list_of_ingredients(
            recipe=instance, ingredients_data=ingredients_data)
        return instance


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source='recipe.id',
        required=False)
    name = serializers.CharField(
        source='recipe.name',
        required=False)
    image = serializers.CharField(
        source='recipe.image',
        required=False)
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time',
        required=False)

    class Meta:
        model = Favorite
        fields = (
            'id',
            'user',
            'recipe',
            'name',
            'image',
            'cooking_time'
        )
        extra_kwargs = {
            'user': {
                'required': False,
                'write_only': True
            },
            'recipe': {
                'required': False,
                'write_only': True
            }
        }


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source='recipe.id',
        required=False)
    name = serializers.CharField(
        source='recipe.name',
        required=False)
    image = serializers.CharField(
        source='recipe.image',
        required=False)
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time',
        required=False)

    class Meta:
        model = ShoppingCart
        fields = (
            'id',
            'user',
            'recipe',
            'name',
            'image',
            'cooking_time',
        )
        extra_kwargs = {
            'user': {
                'required': False,
                'write_only': True
            },
            'recipe': {
                'required': False,
                'write_only': True
            }
        }
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='This following already exists.'
            )
        ]
