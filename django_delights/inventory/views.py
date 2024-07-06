from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login, authenticate
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, ListView
from django.db.models import Sum, DateField, F
from django.urls import reverse_lazy
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.contrib.auth import views 
from django.contrib.auth.forms import UserCreationForm

from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from .forms import IngredientItemCreateForm, MenuItemCreateForm, RecipeRequirementCreateForm, PurchaseCreateForm

#HOME
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/menu.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.all()
        context["menuitems"] = MenuItem.objects.all()
        context["purchases"] = Purchase.objects.all()
        context["reqs"] = RecipeRequirement.objects.all()
        return context
    
#Sign Up
class SignUpView(CreateView):
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
    form_class = UserCreationForm
    
#Login
class LoginView(views.LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True
    
#MENU VIEWS
class MenuItemList(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = "inventory/menu.html"
    
    def get_context_data(self):
        context = super().get_context_data()
        context["menuitems"] = MenuItem.objects.all()
        context["reqs"] = RecipeRequirement.objects.all()
        return context
    
class MenuItemCreate(LoginRequiredMixin, CreateView):
    model = MenuItem
    template_name = "inventory/menu_item_create_form.html"
    form_class = MenuItemCreateForm
    success_url = reverse_lazy("menu")

class MenuItemUpdate(LoginRequiredMixin, UpdateView):
    model = MenuItem
    template_name = "inventory/menu_item_update_form.html"
    success_url = reverse_lazy("menu")
    fields = "__all__"
    
class MenuItemDelete(LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = "inventory/menu_item_delete_form.html"
    success_url = reverse_lazy("menu")
   
#INGREDIENTS
class IngredientList(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "inventory/inventory.html"
    #context_object_name = "ingredient_list"
    def get_context_data(self):
        context = super().get_context_data()
        context["ingredients"] = Ingredient.objects.all()
        return context
     
class IngredientCreate(LoginRequiredMixin, CreateView):
    model = Ingredient
    template_name = "inventory/ingredient_create_form.html"
    form_class = IngredientItemCreateForm
    success_url = reverse_lazy("inventory")

class IngredientUpdate(LoginRequiredMixin, UpdateView):
    model = Ingredient
    template_name = "inventory/ingredient_update_form.html"
    fields = ["quantity", "unit", "unit_price"]
    success_url = reverse_lazy("inventory")
    
class IngredientDelete(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = "inventory/ingredient_delete_form.html"
    success_url = reverse_lazy("inventory")
    
#RECIPE
class RecipeList(LoginRequiredMixin, ListView):
    model = RecipeRequirement
    template_name = "inventory/recipes.html"
    context_object_name = "recipe_list"
    
class RecipeCreate(LoginRequiredMixin, CreateView):
    model = RecipeRequirement
    template_name = "inventory/recipe_create_form.html" 
    form_class = RecipeRequirementCreateForm 
    success_url = reverse_lazy("menu")
   
class RecipeUpdate(LoginRequiredMixin, UpdateView):
    model = RecipeRequirement
    template_name = "inventory/recipe_update_form.html"
    fields = ["quantity"]
    success_url = reverse_lazy("menu")
    
class RecipeDelete(LoginRequiredMixin, DeleteView):
    model = RecipeRequirement
    template_name = "inventory/recipe_delete_form.html"
    success_url = reverse_lazy("menu")
     
#PURCHASE
class PurchaseList(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = "inventory/purchase_list.html"
    ordering = ["-timestamp"]
    context_object_name = "purchase_list"

class PurchaseUpdate(LoginRequiredMixin, UpdateView):
    model = Purchase
    template_name = "inventory/purchase_update_form.html"
    success_url = reverse_lazy("purchase") 
    fields = "__all__"
     
class NewPurchase(LoginRequiredMixin, TemplateView):
    template_name = "inventory/add_purchase.html"
    model = Purchase
    form_class = PurchaseCreateForm
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context["menu_items"] = [X for X in MenuItem.objects.all() if X.available()]
        return context
    
    def post(self, request):
        menu_item_id = request.POST["menu_item"]
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        reqs = RecipeRequirement.objects.filter(menu_item=menu_item)
        purchase = Purchase(menu_item=menu_item)
        
        for req in reqs:
            req.ingredient.quantity -= req.quantity
            req.ingredient.save()
        purchase.save()
        return redirect("purchases")

#REPORT
class ReportView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/reports.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["purchases"] = Purchase.objects.all() 
        context["revenues"] = [purchase.revenue() for purchase in Purchase.objects.all()]
        context["costs"] = [purchase.cost() for purchase in Purchase.objects.all()]
        context["profit"] = sum([purchase.profit() for purchase in Purchase.objects.all()])
        context["totalRevenue"] = sum([purchase.revenue() for purchase in Purchase.objects.all()])
        context["totalCost"] = sum([purchase.cost() for purchase in Purchase.objects.all()])
        return context 

#LOGOUT 
def log_out(request):
    logout(request)
    return redirect("/")
