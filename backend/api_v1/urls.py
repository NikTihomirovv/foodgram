from django.urls import include, path
from rest_framework.routers import SimpleRouter
from api_v1.views import (CustomUserViewSet, IngredientViewSet, RecipeViewSet,
                          TagViewSet)

router = SimpleRouter()
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),

    path('', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),
]
