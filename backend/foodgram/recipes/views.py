# from django.shortcuts import render
from rest_framework import viewsets

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import Tag, Favorite, Recipe, Ingredient
from .serializers import (
    TagSerializer,
    FavoriteSerializer,
    RecipeSerializer,
    IngredientSerializer,
)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    http_method_names = ['post', 'delete', 'get']

    def create(self, request, *args, **kwargs):
        data = {
            'user': self.request.user.id,
            'recipe': int(kwargs.get('recipe')),
        }
        serializer = FavoriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Favorite,
            user=self.request.user,
            recipe=Recipe.objects.get(id=self.kwargs.get('recipe')))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
