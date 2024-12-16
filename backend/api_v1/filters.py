import django_filters
from django_filters import rest_framework
from django_filters.rest_framework import FilterSet
from recipes.models import Ingredient, Recipe, Tag


class FilterForIngredients(FilterSet):
    """Фильтр для поиска по названию ингредиента."""

    name = rest_framework.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class FilterForFavouritesAndShopingCard(FilterSet):
    """Фильтр для обеспечения корректного отображения избранных товаров
       и товаров в списке покупок."""

    tags = rest_framework.filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    is_favorited = django_filters.filters.NumberFilter(
        method='favourited_filter'
    )

    is_in_shopping_cart = django_filters.filters.NumberFilter(
        method='shopping_card_filter'
    )

    def favourited_filter(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(is_favorited__user=user)
        return queryset

    def shopping_card_filter(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(is_in_shopping_cart__user=user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')
