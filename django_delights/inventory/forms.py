from django import forms
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase

class MenuItemCreateForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = "__all__"
        
class IngredientItemCreateForm(forms.ModelForm):
    class Meta: 
        model = Ingredient
        fields = "__all__"
        
class RecipeRequirementCreateForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirement
        fields = "__all__"

class PurchaseCreateForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = "__all__"
        