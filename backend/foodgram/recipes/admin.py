from django.contrib import admin
from recipes.models import Recipe, Tag, Favorite, Ingredient


admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(Ingredient)
