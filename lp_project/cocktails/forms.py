from django.forms import ModelForm
from .models import Cocktail, Ingredient

class CocktailCreation(ModelForm):
    class Meta:
        model = Cocktail
        fields = '__all__'