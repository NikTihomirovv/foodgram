from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(
        verbose_name='Тег',
        help_text='Укажите тег.',
        max_length=50,
        null=False,
        blank=False
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        help_text='Укажите слаг.',
        unique=True,
        max_length=50,
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингридиента."""

    name = models.CharField(
        verbose_name='Ингридиент',
        help_text='Укажите название ингридиента.',
        max_length=50,
        null=False,
        blank=False
    )
    measurement_unit = models.CharField(
        max_length=100,
        verbose_name="Единица измерения",
        help_text='Выберите единицу измерения.',
        blank=False
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        default_related_name = 'ingredients'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""

    name = models.CharField(
        verbose_name='Название рецепта',
        help_text='Укажите название рецепта.',
        max_length=50,
        null=False,
        blank=False
    )
    image = models.ImageField(
        verbose_name='Фото рецепта',
        help_text='Добавте фото вашего рецепта.',
        upload_to='recipe_images',
        null=False,
        blank=False
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Напишите описание рецепта.',
        max_length=1000,
        null=False,
        blank=False
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        help_text='Укажите время приготовления в минутах',
        null=False,
        blank=False
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        help_text='Укажите автора рецепта',
        null=False,
        blank=False,
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        'RecipeIngredient',
        verbose_name='Ингридиенты для рецепта',
        help_text='Укажите ингридиенты, необходимые для приготовления.',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги для рецепта',
        help_text='Выберете подходящие теги.',
        blank=False,
        related_name='recipes'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель для связи ингридиента и рецепта."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент'
    )
    amount = models.IntegerField(
        verbose_name='Количество ингридиента в рецепте'
    )

    class Meta:
        verbose_name = 'Количество ингредиента в рецепте'
        verbose_name_plural = 'Количество ингредиента в рецептах'

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
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

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
        verbose_name = 'Добавленный рецепт'
        verbose_name_plural = 'Добавленные рецепты'

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в корзтну.'
