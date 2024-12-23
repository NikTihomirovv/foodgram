# Generated by Django 3.2 on 2024-12-23 21:23

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Избранный рецепт',
                'verbose_name_plural': 'Избранные рецепты',
                'ordering': ('user',),
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Укажите название ингридиента.', max_length=50, verbose_name='Ингридиент')),
                ('measurement_unit', models.CharField(help_text='Выберите единицу измерения.', max_length=100, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингридиент',
                'verbose_name_plural': 'Ингридиенты',
                'ordering': ('name',),
                'default_related_name': 'ingredients',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Укажите название рецепта.', max_length=50, verbose_name='Название рецепта')),
                ('image', models.ImageField(help_text='Добавте фото вашего рецепта.', upload_to='recipe_images', verbose_name='Фото рецепта')),
                ('text', models.TextField(help_text='Напишите описание рецепта.', verbose_name='Описание рецепта')),
                ('cooking_time', models.IntegerField(help_text='Укажите время приготовления в минутах', validators=[django.core.validators.MinValueValidator(1, 'Минимальное значение - 1'), django.core.validators.MaxValueValidator(32000, 'Максимальное значение - 32000')], verbose_name='Время приготовления')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Минимальное значение - 1'), django.core.validators.MaxValueValidator(32000, 'Максимальное значение - 32000')], verbose_name='Количество ингридиента в рецепте')),
            ],
            options={
                'verbose_name': 'Количество ингредиента в рецепте',
                'verbose_name_plural': 'Количество ингредиента в рецептах',
                'ordering': ('ingredient',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Укажите тег.', max_length=50, verbose_name='Тег')),
                ('slug', models.SlugField(help_text='Укажите слаг.', unique=True, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_in_shopping_cart', to='recipes.recipe', verbose_name='Рецепт, добавленный в корзину пользователем.')),
            ],
            options={
                'verbose_name': 'Добавленный рецепт',
                'verbose_name_plural': 'Добавленные рецепты',
                'ordering': ('user',),
            },
        ),
    ]
