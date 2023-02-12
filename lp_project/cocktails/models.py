from django.db import models
from django.contrib.auth.models import User

class IngredientCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(IngredientCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Cocktail(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.name


