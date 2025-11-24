from django.shortcuts import render, redirect, get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import requests

from .models import *
from .serializers import *

@api_view(['GET'])
def hello_world(request):
    content = {'message': 'Hello, World! The connection from Django is successful!'}
    return Response(content, status=status.HTTP_200_OK)

@api_view(['GET'])
def index(request):
    recipes = Recipe.objects.all().order_by('-number_of_views')[:5]
    content = []
    for r in recipes:
        content.append(RecipeCategoryDetailSerializer(r).data)
    
    return Response(content, status=status.HTTP_200_OK)

@api_view(['GET'])
def recipe_detail(request, slug):
    try:
        recipe = Recipe.objects.get(slug=slug)
    except Recipe.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RecipeDetailSerializer(recipe)
        recipe.number_of_views_up()
        recipe.save()
        return Response(serializer.data)

@api_view(['GET'])
def category_detail(request, slug):
    try:
        category = Category.objects.get(slug=slug)
    except Recipe.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategoryDetailSerializer(category)  
        return Response(serializer.data)

# ----------------------------------------------------------------------------------------------
# ------- OBSŁUGA IMAGE -------
# ----------------------------------------------------------------------------------------------

IMAGE_URL = "http://localhost:8080/"

def recipe_upload_view(request):

    return render(request, 'recipe_upload.html')

def images_view(request):
    recipes = Recipe.objects.prefetch_related('steps').all()

    context = {
        'recipes': recipes,
        'image_base_url': IMAGE_URL
    }

    return render(request,'images.html', context)

def delete_image(request):

    return 
        