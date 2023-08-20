from rest_framework import routers
from django.urls import include, path
# from .views import (TagsViewSet,
#                     RecipesViewSet,
#                     IngredientsViewSet,
#                     FavoritesViewSet)
from recipes.views import (
    TagsViewSet,
    RecipesViewSet,
    IngredientsViewSet,
    FavoritesViewSet)
from users.views import UsersViewSet, ChangePasswordView


router = routers.DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'recipes', RecipesViewSet)
# router.register(r'users/subscriptions/')
# router.register(r'recipes/download_shopping_cart')
router.register(r'recipes/(?P<recipe>\d+)/favorite', FavoritesViewSet)
router.register(r'ingredients', IngredientsViewSet)

urlpatterns = [
    path(r'^auth/', include('djoser.urls.authtoken')),
    path('users/set_password',
         ChangePasswordView.as_view(),
         name='set_password'),
    path('', include(router.urls)),
]
