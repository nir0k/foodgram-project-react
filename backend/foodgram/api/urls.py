from django.urls import include, path
from recipes.views import (FavoritesViewSet, IngredientsViewSet,
                           RecipesViewSet, ShoppingCartViewSet, TagsViewSet)
from rest_framework import routers
from users.views import SubscribeViewSet, UsersViewSet, change_password

router = routers.DefaultRouter()
router.register(r'users/subscriptions', SubscribeViewSet)
router.register(r'users/(?P<id>\d+)/subscribe', SubscribeViewSet)
router.register(r'users', UsersViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'recipes/(?P<recipe>\d+)/shopping_cart', ShoppingCartViewSet)
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(r'recipes/(?P<recipe>\d+)/favorite', FavoritesViewSet)
router.register(r'ingredients', IngredientsViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/set_password', change_password, name='set_password'),
    path('', include(router.urls)),
]
