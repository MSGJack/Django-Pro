from django.contrib import admin
from .models import Purchase, MenuItem, RecipeRequirement, Ingredient
from .models import MenuItem

# Register your models here.
admin.site.register(Ingredient)
admin.site.register(MenuItem)
admin.site.register(RecipeRequirement)
admin.site.register(Purchase)