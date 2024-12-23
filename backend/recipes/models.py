from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from backend.constants import (RECIPE_INGREDIENT_AMOUNT_MAX,
                               RECIPE_INGREDIENT_AMOUNT_MIN,
                               RECIPE_INGREDIENT_COOKING_TIME_MAX,
                               RECIPE_INGREDIENT_COOKING_TIME_MIN)

User = get_user_model()


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(
        verbose_name='Тег',
        help_text='Укажите тег.',
        max_length=50,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        help_text='Укажите слаг.',
        unique=True,
        max_length=50,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингридиента."""

    name = models.CharField(
        verbose_name='Ингридиент',
        help_text='Укажите название ингридиента.',
        max_length=50,
    )
    measurement_unit = models.CharField(
        max_length=100,
        verbose_name="Единица измерения",
        help_text='Выберите единицу измерения.',
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        default_related_name = 'ingredients'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""

    name = models.CharField(
        verbose_name='Название рецепта',
        help_text='Укажите название рецепта.',
        max_length=50,
    )
    image = models.ImageField(
        verbose_name='Фото рецепта',
        help_text='Добавте фото вашего рецепта.',
        upload_to='recipe_images'
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Напишите описание рецепта.',
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        help_text='Укажите время приготовления в минутах',
        validators=[
            MinValueValidator(
                RECIPE_INGREDIENT_COOKING_TIME_MIN,
                'Минимальное значение - 1'
            ),
            MaxValueValidator(
                RECIPE_INGREDIENT_COOKING_TIME_MAX,
                'Максимальное значение - 32000'
            )
        ]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        help_text='Укажите автора рецепта',
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингридиенты для рецепта',
        help_text='Укажите ингридиенты, необходимые для приготовления.',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги для рецепта',
        help_text='Выберете подходящие теги.',
        related_name='recipes'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель для связи ингредиента и рецепта."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиента в рецепте',
        validators=[
            MinValueValidator(
                RECIPE_INGREDIENT_AMOUNT_MIN,
                'Минимальное значение - 1'
            ),
            MaxValueValidator(
                RECIPE_INGREDIENT_AMOUNT_MAX,
                'Максимальное значение - 32000'
            )
        ],
    )

    class Meta:
        default_related_name = 'recipe_ingredients'
        verbose_name = 'Количество ингредиента в рецепте'
        verbose_name_plural = 'Количество ингредиента в рецептах'
        ordering = ('ingredient',)

    def __str__(self):
        return f'Количество {self.ingredient} -  {self.amount}'


class Favourite(models.Model):
    """Модель для избранного рецепта."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь, выбравший рецепт.'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт, выбранный пользователем.',
        related_name='is_favorited'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favourites',
            )
        ]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        ordering = ('user',)

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в избранное.'


class ShoppingCart(models.Model):
    """Модель для корзины покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppingcarts',
        verbose_name='Пользователь, добавивший рецепт в корзину.'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт, добавленный в корзину пользователем.',
        related_name='is_in_shopping_cart'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart'
            )
        ]
        ordering = ('user',)
        verbose_name = 'Добавленный рецепт'
        verbose_name_plural = 'Добавленные рецепты'

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в корзтну.'
