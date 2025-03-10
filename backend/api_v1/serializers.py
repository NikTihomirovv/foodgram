import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from django.db.models import F

from backend.constants import (RECIPE_INGREDIENT_AMOUNT_MAX,
                               RECIPE_INGREDIENT_AMOUNT_MIN,
                               RECIPE_INGREDIENT_COOKING_TIME_MAX,
                               RECIPE_INGREDIENT_COOKING_TIME_MIN)
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """Класс для обработки фото в base64."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователя."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class CustomUserSerializer(UserSerializer):
    """Сериализатор для пользователя."""
    avatar = Base64ImageField(required=False, allow_null=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'avatar',
            'is_subscribed',
        )

    def get_is_subscribed(self, author):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.is_subscribed.all().exists()


class SubscriptionSerializer(UserSerializer):
    """Сериализатор для подписки или отписки пользователей."""

    recipes_count = serializers.IntegerField(source="recipes.count")
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_subscribed',
            'avatar',
            'recipes_count',
            'recipes',
        )

    def get_recipes(self, author):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = author.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        return RecipeShortSerializer(recipes, many=True, read_only=True).data

    def get_is_subscribed(self, author):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.is_subscribed.all().exists()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингридиентов."""

    measurement_unit = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения рецептов."""

    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',

            'tags',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        recipe = obj
        ingredients = recipe.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('recipeingredient__amount')
        )
        return ingredients

    def get_is_favorited(self, recipe):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.shoppingcarts.filter(recipe=recipe).exists()


class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для промежуточной таблицы
    между рецептом и ингридиентом. Для записи и обновления.
    """

    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(
        required=True,
        max_value=RECIPE_INGREDIENT_AMOUNT_MAX,
        min_value=RECIPE_INGREDIENT_AMOUNT_MIN
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount',)


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи и обновления рецептов."""

    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientWriteSerializer(many=True)
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        required=True,
        max_value=RECIPE_INGREDIENT_COOKING_TIME_MAX,
        min_value=RECIPE_INGREDIENT_COOKING_TIME_MIN
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',

            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def create_amount_for_ingredients(self, recipe, ingredients):

        RecipeIngredient.objects.bulk_create(
            [RecipeIngredient(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                amount=ingredient['amount'],
                recipe=recipe
            ) for ingredient in ingredients]
        )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        self.create_amount_for_ingredients(
            recipe=recipe,
            ingredients=ingredients
        )
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        instance.ingredients.clear()
        instance.tags.set(validated_data.pop('tags'))
        ingredients = validated_data.pop('ingredients')

        self.create_amount_for_ingredients(
            recipe=instance,
            ingredients=ingredients
        )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serializer = RecipeReadSerializer(instance, context=self.context)
        return serializer.data


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для короткого описания рецепта."""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
