import base64
# import webcolors

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import (
    Recipe, Tag, Favorite, Ingredient, IngradientRecipe, TagRecipe)
from users.serializer import UserSerializer
from django.shortcuts import get_object_or_404


# class Hex2NameColor(serializers.Field):
#     def to_representation(self, value):
#         return value

#     def to_internal_value(self, data):
#         try:
#             data = webcolors.hex_to_name(data)
#         except ValueError:
#             raise serializers.ValidationError('Для этого цвета нет имени')
#         return data


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    # color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
        )
        read_only_fields = ('name',)
        # extra_kwargs = {
        #     "id": {
        #         "read_only": False,
        #         "required": False,
        #     },
        # }


class IngradientRecipeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    measurement_unit = serializers.SerializerMethodField(read_only=True)
    # id = serializers.SerializerMethodField(source='ingradient.id')
    id = serializers.IntegerField(source='ingradient.id')
    # recipe_id = serializers.IntegerField(source='recipe', write_only=True)

    class Meta():
        model = IngradientRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
            # 'recipe_id',
        )
        extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
        }

    def get_name(self, obj):
        return obj.ingradient.name

    def get_measurement_unit(self, obj):
        return obj.ingradient.measurement_unit

    def create(self, validated_data):
        ingradient = validated_data.pop('ingradient')
        ingredientrecipe = IngradientRecipe.objects.get_or_create(
            **validated_data, ingradient=ingradient.get('id'))

        return ingredientrecipe

    # def get_id(self, obj):
    #     return obj.ingradient.id


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        extra_kwargs = {
            "user": {"required": False},
            "recipe": {"required": False}
        }


class RecipeGetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngradientRecipeSerializer(
        source='ingradientrecipe_set', many=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            # 'is_favorited',
            # 'is_in_shopping_cart',
            'image',
            'name',
            'text',
            'cooking_time')


class RecipePostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True)

    # ingredients = IngradientRecipeSerializer(
    #     source='ingradientrecipe_set', many=True)
    ingredients = serializers.PrimaryKeyRelatedField(
        queryset=IngradientRecipe.objects.all(),
        many=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            # 'is_favorited',
            # 'is_in_shopping_cart',
            'image',
            'name',
            'text',
            'cooking_time')

    # def create(self, validated_data):
    #     ingredients_data = validated_data.pop('ingradientrecipe_set')
    #     recipe = Recipe.objects.create(**validated_data)
    #     ingredients = []
    #     for ingredient_data in ingredients_data:
    #         # ingredient_id = ingredient_data.pop('id', None)
    #         ingredient_id = ingredient_data.get('ingradient')
    #         ingredient_amount = ingredient_data.get('amount')
    #         ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    #         ingredientrecipe, _ = IngradientRecipe.objects.get_or_create(
    #             recipe=recipe, ingradient=ingredient, amount=ingredient_amount)
    #         ingredients.append(ingredient)
    #     recipe.ingredients.add(*ingredients)
    #     return recipe
