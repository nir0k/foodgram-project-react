# Generated by Django 3.2.3 on 2023-08-23 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_ingradientrecipe_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingradientrecipe',
            name='ingradient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipes.ingredient'),
        ),
    ]
