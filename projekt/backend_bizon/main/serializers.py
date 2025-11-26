from rest_framework import serializers
from .models import *

# prosty opis do kategorii
class RecipeCategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'slug', 'image', 'preparation_time', 'number_of_views'] # Tylko kluczowe dane

# wiekszy do kategorii calej
class CategoryDetailSerializer(serializers.ModelSerializer):
    recipes = RecipeCategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'recipes']

# prosty do wyswietlenia w podstronie przepisu
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']

class RecipeStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep
        fields = ['step_number', 'image', 'text']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    unit = serializers.ReadOnlyField() 
    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'quantity', 'unit']

# szczegolowy
class RecipeDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    steps = RecipeStepSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 
            'name', 
            'description', 
            'preparation_time', 
            'number_of_views', 
            'image', 
            'slug',
            'categories',
            'steps',
            'ingredients'
        ]


