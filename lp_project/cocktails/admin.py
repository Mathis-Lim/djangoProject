from django.contrib import admin
from .models import IngredientCategory, Ingredient, Cocktail

admin.site.register(IngredientCategory)
admin.site.register(Ingredient)
admin.site.register(Cocktail)
