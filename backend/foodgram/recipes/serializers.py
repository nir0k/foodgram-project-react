import base64
# import webcolors

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Recipe, Tag, Favorite, Ingredient


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
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        extra_kwargs = {
            "user": {"required": False},
            "recipe": {"required": False}
        }


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'image', 'name', 'text', 'cooking_time')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
