from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']

# prosty opis do kategorii
class RecipeCategoryDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'slug', 'image', 'preparation_time', 'number_of_views', 'created_by'] # Tylko kluczowe dane

# wiekszy do kategorii calej
class CategoryDetailSerializer(serializers.ModelSerializer):
    recipes = RecipeCategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'recipes']

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

class RecipeIngredientSerializer_C(serializers.ModelSerializer):
    ingredient = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'quantity', 'unit_choice']

class RecipeCreateSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    steps = RecipeStepSerializer(many=True, required=False)
    ingredients = RecipeIngredientSerializer_C(many=True, required=False)
    
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'preparation_time', 'categories', 'steps', 'ingredients', 'created_by']
    
    def create(self, validated_data):
        steps_data = validated_data.pop('steps')
        ingredients_data = validated_data.pop('ingredients')
        categories_data = validated_data.pop('categories')

        recipe = Recipe.objects.create(**validated_data)

        recipe.categories.set(categories_data)

        for step_data in steps_data:
            RecipeStep.objects.create(recipe=recipe, **step_data)

        for ing_data in ingredients_data:
            RecipeIngredient.objects.create(recipe=recipe, **ing_data)

        return recipe

    # do put - aktualizacja przepisu
    def update(self, instance, validated_data):
        steps_data = validated_data.pop('steps', None)
        ingredients_data = validated_data.pop('ingredients', None)
        categories_data = validated_data.pop('categories', None)
        
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.preparation_time = validated_data.get('preparation_time', instance.preparation_time)
        instance.save()
        
        if categories_data is not None:
            instance.categories.set(categories_data)
        
        if steps_data is not None:
            instance.steps.all().delete()
            RecipeStep.objects.bulk_create([
                RecipeStep(recipe=instance, **step) for step in steps_data
            ])
            
        if ingredients_data is not None:
            instance.ingredients.all().delete()
            for ing_data in ingredients_data:
                RecipeIngredient.objects.create(recipe=instance, **ing_data)
                
        return instance

# szczegolowy
class RecipeDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    steps = RecipeStepSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 
            'name', 
            'created_by',
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
