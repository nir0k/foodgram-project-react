# Generated by Django 3.2.3 on 2023-08-23 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_remove_recipe_ingredients'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.IngredientRecipe', to='recipes.Ingredient', verbose_name='ingredients'),
        ),
    ]
