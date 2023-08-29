from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=254)
    color = models.CharField(max_length=16)
    slug = models.SlugField()

    class Meta:
        unique_together = ('name', 'color', 'slug')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=254, null=False, blank=False)
    measurement_unit = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

    class Meta:
        unique_together = ('name', 'measurement_unit')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name="ingredients"
    )
    author = models.ForeignKey(
        User,
        related_name='author',
        on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(Tag, through='TagRecipe')
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )
    name = models.CharField(max_length=200, null=False, blank=False)
    text = models.TextField(null=False, blank=False)
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)],
        default=1
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name="ingredients",
                                   null=True,
                                   blank=True,)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name="recipe_ingredients",
                               null=True,
                               blank=True,)
    amount = models.FloatField(null=False,
                               blank=False,
                               validators=[MinValueValidator(0.1)],
                               default=0.1)

    class Meta:
        verbose_name = "Колличество ингридиентов"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="value_amount",
            ),
        ]

    def __str__(self):
        return f'{self.recipe} {self.ingredient} {self.amount}'


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag,
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name="recipe_tags",
                               null=True,
                               blank=True,
                               )

    def __str__(self):
        return f'{self.recipe} {self.tag}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='favorites',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ('user', 'recipe')


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        related_name='shoppingscart',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='shoppingscart',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ('user', 'recipe')
