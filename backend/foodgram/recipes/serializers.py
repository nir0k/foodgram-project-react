import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import (
    Recipe,
    Tag,
    Favorite,
    Ingredient,
    RecipeIngredient,
    TagRecipe
)
from users.serializer import UserSerializer
from django.shortcuts import get_object_or_404


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
        read_only_fields = ('name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
        )
        read_only_fields = ('name',)


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
    ingredients = IngredientRecipeSerializer(many=True, source='recipe')
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
        many=True,
        write_only=True,
    )
    tags_show = TagSerializer(read_only=True, many=True, source='tags')
    ingredients = IngredientRecipeSerializer(many=True,
                                             source='recipe_ingredients')
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'tags_show',
            'author',
            'ingredients',
            # 'is_favorited',
            # 'is_in_shopping_cart',
            'image',
            'name',
            'text',
            'cooking_time')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['tags'] = response.pop('tags_show')
        return response

    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for tag_data in tags_data:
            tag = get_object_or_404(Tag, pk=tag_data.id)
            TagRecipe.objects.create(recipe=recipe, tag=tag)
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
        return recipe
