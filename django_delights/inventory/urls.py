from django.urls import path
#from django.contrib.auth import views 
from . import views
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path("account/login", views.LoginView.as_view(), name="login"),
    #path('accounts/login/', auth_views.LoginView.as_view(), name="login"), 
    path('inventory/', views.IngredientList.as_view(), name="inventory"),
    path('inventory/new', views.IngredientCreate.as_view(), name="add_ingredient"),
    path('ingredients/update/<slug:pk>', views.IngredientUpdate.as_view(), name="update_ingredient"),
    path('ingredients/delete/<slug:pk>', views.IngredientDelete.as_view(), name="delete_ingredient"),
    path("logout/", views.log_out, name="logout"),
    path('menu/', views.MenuItemList.as_view(), name="menu"),
    path('menu/new', views.MenuItemCreate.as_view(), name="menu_item_create"),
    path("menu/update/<int:pk>", views.MenuItemUpdate.as_view(), name="menu_item_update"),
    path("menu/delete/<int:pk>/", views.MenuItemDelete.as_view(), name="menu_item_delete"),
    path('purchases', views.PurchaseList.as_view(), name="purchases"),
    path('purchases/new', views.NewPurchase.as_view(), name="add_purchase"),
    path("recipes/", views.RecipeList.as_view(), name="recipes"),
    path('recipes/new', views.RecipeCreate.as_view(), name="add_recipe"),
    path('recipes/update/<int:pk>', views.RecipeUpdate.as_view(), name="update_recipe"),
    path('recipes/delete/<int:pk>', views.RecipeDelete.as_view(), name="delete_recipe"),
    path('reports', views.ReportView.as_view(), name="reports"),
    path("signup", views.SignUpView.as_view(), name="signup"),
] 
  