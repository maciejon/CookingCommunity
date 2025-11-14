from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(IngredientCategory)
admin.site.register(Ingredient)
admin.site.register(RecipieCategory)
admin.site.register(Recipe)
admin.site.register(RecipeStep)
admin.site.register(RecipeIngredient)


