from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

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

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['user', 'stars', 'text', 'created_at', 'updated_at']

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
    reviews = ReviewSerializer(many=True)

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
            'ingredients',
            'reviews'
        ]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Hasła nie są identyczne."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email')
        )
        return user
