from django.db import models
from django.core.validators import MinValueValidator
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=254)
    color = models.CharField(max_length=16)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Recipe(models.Model):
    # ingredients
    tags = models.ManyToManyField(Tag)
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


class Ingredient(models.Model):
    name = models.CharField(max_length=254)
    measurement_unit = models.CharField(max_length=2)

    def __str__(self):
        return self.name


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
