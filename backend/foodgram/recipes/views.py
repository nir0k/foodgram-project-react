from django.db.models import Exists, OuterRef, Value
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_condition import Or
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.permissions import IsAdmin, IsAuthorOrReadOnly, ReadOnly

from .filters import RecipeFilter
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          TagSerializer)


class CustomSearchFilter(filters.SearchFilter):
    search_param = "name"


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (Or(ReadOnly, IsAdmin),)
    filter_backends = (DjangoFilterBackend,)
    search_fields = ('slug',)


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
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = (
        Or(IsAuthorOrReadOnly, ReadOnly),
    )
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Recipe.objects.annotate(
                is_in_shopping_cart=Value(False),
                is_favorited=Value(False)
            ).all()

        queryset = Recipe.objects.annotate(
            is_favorited=Exists(Favorite.objects.filter(
                user=self.request.user, recipe=OuterRef('pk'))),
            is_in_shopping_cart=Exists(ShoppingCart.objects.filter(
                user=self.request.user, recipe=OuterRef('pk')))
        ).all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request, *args, **kwargs):
        file_name = 'shopping_cart.txt'
        lines = []
        num = 1
        for shoppingcart in self.request.user.shoppingscart.all():
            lines.append('{0}. {1}:'.format(
                num,
                shoppingcart.recipe.name
            ))
            for ingredient in shoppingcart.recipe.recipe_ingredients.all():
                lines.append('    - {0}: {1} ({2});'.format(
                    ingredient.ingredient,
                    ingredient.amount,
                    ingredient.ingredient.measurement_unit
                ))
            lines.append('')
            num += 1
        response_content = '\n'.join(lines)
        response = HttpResponse(response_content,
                                content_type="text/plain,charset=utf8")
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            file_name)
        return response


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (Or(ReadOnly, IsAdmin),)
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend, CustomSearchFilter)
    search_fields = ('name',)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    http_method_names = ['post', 'delete', 'get']

    def create(self, request, *args, **kwargs):
        data = {
            'user': self.request.user.id,
            'recipe': int(kwargs.get('recipe')),
        }
        serializer = ShoppingCartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = get_object_or_404(
            ShoppingCart,
            user=self.request.user,
            recipe=Recipe.objects.get(id=self.kwargs.get('recipe')))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
