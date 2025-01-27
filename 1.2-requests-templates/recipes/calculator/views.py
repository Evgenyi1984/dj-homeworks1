from django.shortcuts import redirect, render
from django.http import HttpResponseNotFound

DATA = {
    "omlet": {
        "яйца, шт": 2,
        "молоко, л": 0.1,
        "соль, ч.л.": 0.5,
    },
    "pasta": {
        "макароны, г": 0.3,
        "сыр, г": 0.05,
    },
    "buter": {
        "хлеб, ломтик": 1,
        "колбаса, ломтик": 1,
        "сыр, ломтик": 1,
        "помидор, ломтик": 1,
    },
    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }


def index_view(request):
    """Redirect to the recipes list."""
    return redirect("recipes_list")


def recipes_list_view(request):
    """Display a list of all available recipes."""
    context = {"recipes": DATA}
    return render(request, "calculator/recipes_list.html", context)


SERVINGS_PARAM_ERR_MSG = (
    "Неверный параметр servings. Должно быть положительное целое число."
)


def recipe_view(request, recipe_name):
    recipe = DATA.get(recipe_name)
    if not recipe:
        return HttpResponseNotFound(f"Рецепт '{recipe_name}' не найден.")

    servings = request.GET.get("servings", 1)
    try:
        servings = int(servings)
    except ValueError:
        return HttpResponseNotFound(SERVINGS_PARAM_ERR_MSG)

    if servings < 1:
        return HttpResponseNotFound(SERVINGS_PARAM_ERR_MSG)

    # Adjust ingredient quantities based on servings
    scaled_recipe = {
        ingredient: amount * servings for ingredient, amount in recipe.items()
    }

    context = {"recipe_name": recipe_name, "recipe": scaled_recipe}
    return render(request, "calculator/index.html", context)
