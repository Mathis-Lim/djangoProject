from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import  JsonResponse
from django.core.serializers import serialize
from django.contrib.auth import login, authenticate, logout as django_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView

from cocktails.forms import CocktailCreation
from cocktails.models import Cocktail, Ingredient, IngredientCategory

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'cocktails/index.html'
    login_url = 'login'

    def get_context_data(self):
        context = {}
        context['bartender'] = self.request.user.has_perm('cocktails.add_cocktail')
        return context

class CocktailDetailView(LoginRequiredMixin, DetailView):
    model = Cocktail
    template_name = 'cocktails/detail.html'
    login_url = 'login'

    def get_object(self):
        cocktail = super().get_object()
        self.context = { 'cocktail': cocktail,}
        return cocktail

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ingredient_list = self.object.ingredients.all()
        context['ingredient_list'] = ingredient_list
        return context

class IngredientDetailView(LoginRequiredMixin, DetailView):
    model = Ingredient
    template_name = 'ingredients/detail.html'
    login_url = 'login'

    def get_object(self):
        ingredient = super().get_object()
        self.context = { 'ingredient': ingredient,}
        return ingredient

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cocktails_used_in = self.object.cocktail_set.all()
        context['cocktails_used_in'] = cocktails_used_in
        return context



def get_all_cocktails(request):
    if request.user.is_authenticated:
        cocktail_list = Cocktail.objects.all()
        data = serialize('json', cocktail_list)
        return JsonResponse(data, safe=False)
    else:
        return redirect('login')

class CocktailsAjax(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, *args):
        cocktail_list = Cocktail.objects.all()
        data = serialize('json', cocktail_list)
        return JsonResponse(data, safe=False)

class IngredientAjax(LoginRequiredMixin, DetailView):
    model = Ingredient
    login_url = 'login'

    def get_object(self):
        ingredient = super().get_object()
        return ingredient

    def get(self, *args, **kwargs):
        data = serialize('json', [self.get_object(),])
        return JsonResponse(data, safe=False)

class CategoryAjax(LoginRequiredMixin, DetailView):
    model = IngredientCategory
    login_url = 'login'

    def get_object(self):
        category = super().get_object()
        return category

    def get(self, *args, **kwargs):
        data = serialize('json', [self.get_object(),])
        return JsonResponse(data, safe=False)


class CocktailCreationView(LoginRequiredMixin, FormView):
    form_class = CocktailCreation
    template_name = 'forms/cocktail_creation.html'
    login_url = 'login'

    def check_authorization(self):
        return self.request.user.has_perm('cocktails.add_cocktail')

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return render(request, self.template_name, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        if not self.check_authorization():
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

class SignupView(FormView):
    form_class = UserCreationForm
    template_name = 'forms/signup.html'

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, self.template_name, {'form': form})

class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'forms/login.html'

    def post(self,request):
        form = self.form_class(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return redirect('login')
        else:
            return redirect('login')

def logout(request):
    django_logout(request)
    return redirect('login')











