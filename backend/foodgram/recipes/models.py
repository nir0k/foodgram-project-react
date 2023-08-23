from django.db import models
from django.core.validators import MinValueValidator
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=254)
    color = models.CharField(max_length=16)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=254)
    measurement_unit = models.CharField(max_length=2)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        Ingredient, through='IngradientRecipe')
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
        validators=[MinValueValidator(1)]
    )
    # is_favorited = models.ForeignKey(
    #     User,
    #     related_name='recipe_favorite',
    #     blank=True
    # )

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipe} {self.tag}'


class IngradientRecipe(models.Model):
    ingradient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='ingredients',)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.recipe} {self.ingradient} {self.amount}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE,

    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='favorites',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('user', 'recipe')
