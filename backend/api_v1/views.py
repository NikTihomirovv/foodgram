from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api_v1.filters import (FilterForFavouritesAndShopingCard,
                            FilterForIngredients)
from api_v1.pagination import CustomPagination
from api_v1.permissions import IsAdminAuthorOrReadOnly, IsAdminOrReadOnly
from api_v1.serializers import (CustomUserSerializer, IngredientSerializer,
                                RecipeReadSerializer, RecipeShortSerializer,
                                RecipeWriteSerializer, SubscriptionSerializer,
                                TagSerializer)
from recipes.models import (Favourite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import Subscription

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""

    queryset = Recipe.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterForFavouritesAndShopingCard

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        if self.request.method == 'POST' or 'PATCH':
            return RecipeWriteSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
        url_path='favorite',
    )
    def favourite_add_or_delete(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'POST':
            Favourite.objects.create(user=request.user, recipe=recipe)
            return Response(
                RecipeShortSerializer(recipe).data,
                status=status.HTTP_201_CREATED
            )

        else:
            Favourite.objects.filter(user=request.user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
        url_path='shopping_cart',
    )
    def shopping_cart_add_or_delete(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'POST':
            ShoppingCart.objects.create(user=request.user, recipe=recipe)
            return Response(
                RecipeShortSerializer(recipe).data,
                status=status.HTTP_201_CREATED
            )

        else:
            ShoppingCart.objects.filter(
                user=request.user,
                recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
        url_path='download_shopping_cart',
    )
    def download_shopping_cart(self, request):

        ingredients = RecipeIngredient.objects.filter(
            recipes__is_in_shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(sum=Sum('amount'))

        shopping_list = ''
        for ingredient in ingredients:
            shopping_list += (
                f"{ingredient['ingredient__name']}  - "
                f"{ingredient['sum']}"
                f"({ingredient['ingredient__measurement_unit']})\n"
            )
        return HttpResponse(shopping_list, content_type='text/plain')


class TagViewSet(viewsets.ModelViewSet):
    """Вьюсет для тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(viewsets.ModelViewSet):
    """Вьюсет для ингридиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    http_method_names = ['get']
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterForIngredients


class CustomUserViewSet(UserViewSet):
    """Вьюсет для пользователя."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    @action(
        detail=False,
        methods=['PUT', 'PATCH', 'DELETE'],
        url_path='me/avatar',
    )
    def avatar(self, request):
        user = request.user
        serializer = CustomUserSerializer(
            user, data=request.data,
            partial=True
        )

        if request.method == 'DELETE':
            if user.avatar:
                user.avatar.delete(save=True)
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response('Аватар не найден',
                            status=status.HTTP_404_NOT_FOUND)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'avatar': user.avatar.url},
                        status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_path='subscribe',
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if user == author:
            return Response(
                'Нельзя подписаться на самого себя.',
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.method == 'POST':
            created = Subscription.objects.get_or_create(
                user=user,
                author=author
            )
            if created:
                recipes_limit = request.query_params.get('recipes_limit')
                serializer = SubscriptionSerializer(
                    author,
                    context={'request': request,
                             'recipes_limit': recipes_limit}
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            subscription = Subscription.objects.filter(
                user=user,
                author=author
            )
            if subscription.exists():
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        url_path='subscriptions',
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(is_subscribed__user=user)
        recipes_limit = request.query_params.get('recipes_limit')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscriptionSerializer(
                page,
                many=True,
                context={'request': request, 'recipes_limit': recipes_limit},
            )
            return self.get_paginated_response(serializer.data)
        serializer = SubscriptionSerializer(
            queryset,
            many=True,
            context={'request': request, 'recipes_limit': recipes_limit},
        )
        return Response(serializer.data)
