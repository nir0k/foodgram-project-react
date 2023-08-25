from django.contrib import admin
from recipes.models import (
    Recipe,
    Tag,
    Favorite,
    Ingredient,
    RecipeIngredient,
    TagRecipe,
    ShoppingCart
)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeTagInLine(admin.TabularInline):
    model = TagRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'text', 'cooking_time')
    search_fields = ('author', 'name', 'tag')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'
    inlines = (RecipeIngredientInline, RecipeTagInLine)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(Ingredient)
admin.site.register(ShoppingCart)
