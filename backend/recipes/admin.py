from django.contrib import admin

from recipes.models import (Favourite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)


class RecipeAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'image',
        'text',
        'cooking_time',
    )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Favourite)
admin.site.register(ShoppingCart)
admin.site.register(RecipeIngredient)
