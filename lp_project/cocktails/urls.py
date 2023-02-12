from django.urls import path

from . import views
from .views import IndexView, CocktailDetailView, IngredientDetailView, CocktailsAjax, IngredientAjax, CategoryAjax, \
    CocktailCreationView, SignupView, LoginView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', CocktailDetailView.as_view(), name='cocktail_detail'),
    path('ingredient/<int:pk>/', IngredientDetailView.as_view(), name='ingredient_detail'),
    path('get_all_cocktails', CocktailsAjax.as_view(), name='get_all_cocktails'),
    path('get_ingredient/<int:pk>', IngredientAjax.as_view(), name='get_ingredient'),
    path('get_category/<int:pk>', CategoryAjax.as_view(), name='get_category'),
    path('cocktail_creation/', CocktailCreationView.as_view(), name='cocktail_creation'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
]
