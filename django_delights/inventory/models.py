from django.db import models 

UNIT_CHOICES = [
    ("G", "Gram"),
    ("TBSP", "Tablespoon"),
    ("TSP", "Teaspoon"),
    ("L", "Liter"),
    ("EA", "Each"),
    ("Cup", "Cup"),
    ("Oz", "Ounce"),
    ("lbs", "Pound"),
    ("", ""),
]
class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)
    quantity = models.FloatField(default=0.0)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default="")
    unit_price = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"Name: {self.name}"
    
    def get_absolute_url(self):
        return "/inventory"
    
    class Meta:
        ordering = ["name"]
         
class MenuItem(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=400)
    price = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"Name:{self.name}: Price:${self.price}"
    
    def get_absolute_url(self):
        return "/menu"
    
    def available(self):
        return  all(i.enough() for i in RecipeRequirement.objects.filter(menu_item=self.id))
    
    class Meta:
        ordering = ["name"]
    

class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE) 
    quantity = models.FloatField(default=0)
    
    def __str__(self):
        return f"menu_item={self.menu_item.name}; Ingredient={self.ingredient.name}; Quantity={self.quantity}" 
    
    def get_absolute_url(self):
        return "/menu"
    
    def enough(self):
        return self.quantity <= self.ingredient.quantity
    
    class Meta:
        ordering = ["menu_item"]
        
class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"menu_item=[{self.menu_item.__str__()}] order at {self.timestamp}"
    
    def get_absolute_url(self):
        return "/purchases"  
    
    def revenue(self):
        return self.menu_item.price

    def cost(self):
        total = 0 
        reqs = RecipeRequirement.objects.filter(menu_item=self.menu_item.id)
        for req in reqs:
            price = req.quantity * req.ingredient.unit_price
            total += price
        return total 

    def profit(self): 
        return self.revenue() - self.cost() 

    def __str__(self):
        return f"menu_item={self.menu_item.name}; timestamp={self.timestamp}"
    
    class Meta:
        ordering = ["timestamp"]
        