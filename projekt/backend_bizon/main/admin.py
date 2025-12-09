from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  
    search_fields = ('name', 'slug')  

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', )  
    search_fields = ('name', )  

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image')  
    search_fields = ('name', 'categories', 'slug', 'image')  
    list_filter = ('categories',)

@admin.register(RecipeStep)
class RecipeStepAdmin(admin.ModelAdmin):
    list_display = ('recipe__name','step_number',  'text', 'image')  
    search_fields = ('step_number', 'recipe__name', 'image')  
    list_filter = ('step_number', )

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe__name', 'ingredient__name', 'quantity', 'unit_choice')  
    search_fields = ('recipe__name', 'ingredient__name', 'unit_choice')  
    list_filter = ('recipe__name', 'ingredient__name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('recipe__name', 'user', 'stars')
    search_fields = ('recipe__name', 'user', 'stars')
    list_filter = ('recipe__name', 'user', 'stars')