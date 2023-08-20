# from rest_framework import routers
# from django.urls import include, path
# from .views import (TagsViewSet,
#                     RecipesViewSet,
#                     IngredientsViewSet,
#                     FavoritesViewSet)


# router = routers.DefaultRouter()
# router.register(r'tags', TagsViewSet)
# router.register(r'recipes', RecipesViewSet)
# # router.register(r'users/subscriptions/')
# # router.register(r'recipes/download_shopping_cart')
# router.register(r'recipes/(?P<recipe>\d+)/favorite', FavoritesViewSet)
# router.register(r'ingredients', IngredientsViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
#     # path('/', include('djoser.urls')),
#     # path('/', include('djoser.urls.jwt')),
# ]
