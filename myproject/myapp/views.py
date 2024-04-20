from django.shortcuts import render, redirect
from .models import Recipe
from .forms import RecipeForm, UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def home(request):
    random_recipes = Recipe.objects.order_by('?')[:5]
    return render(request, 'home.html', {'random_recipes': random_recipes})

def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})

def add_edit_recipe(request, recipe_id=None):
    if recipe_id:
        recipe = Recipe.objects.get(id=recipe_id)
        form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)
        editing = True
    else:
        form = RecipeForm(request.POST or None, request.FILES or None)
        editing = False
    if request.method == 'POST':
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('home')
    return render(request, 'add_edit_recipe.html', {'form': form, 'editing': editing})

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} был успешно создан! Теперь вы можете войти')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Вы вошли как {username}")
                return redirect('home')
            else:
                messages.error(request, "Неправильное имя пользователя или пароль")
        else:
            messages.error(request, "Неправильное имя пользователя или пароль")
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "Вы успешно вышли из системы")
    return redirect('home')