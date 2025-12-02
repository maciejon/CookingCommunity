from django.shortcuts import render, redirect, get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q, Case, When, Value, IntegerField

import requests

from .models import *
from .serializers import *

@api_view(['GET'])
def hello_world(request):
    content = {'message': 'Hello, World! The connection from Django is successful!'}
    return Response(content, status=status.HTTP_200_OK)

@api_view(['GET'])
def top5(request):
    recipes = Recipe.objects.all().order_by('-number_of_views')[:5]
    listaaa = []
    for r in recipes:
        listaaa.append(RecipeCategoryDetailSerializer(r).data)
    
    content = {'top5' : listaaa}
    
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
    
@api_view(['GET'])
def search(request):
    search_query = request.query_params.get('query', None)

    if search_query:
        recipes = Recipe.objects.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(ingredients__ingredient__name__icontains=search_query)
        ).distinct()
    else:
        recipes = Recipe.objects.none()
    
    # punktujemy waznosc podobienstwa do hasla
    recipes = recipes.annotate(
        relevance=Case(
            When(name__icontains=search_query, then=Value(10)),
            When(description__icontains=search_query, then=Value(5)),
            When(ingredients__ingredient__name__icontains=search_query, then=Value(1)),
            
            default=Value(0),
            output_field=IntegerField(),
        )
    ).order_by('-relevance')

    serializer = RecipeCategoryDetailSerializer(recipes, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

# ----------------------------------------------------------------------------------------------
# ------- LOGOWANIE -------
# ----------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------
# ------- OBSŁUGA IMAGE -------
# ----------------------------------------------------------------------------------------------

IMAGE_BASE_URL = "http://localhost:8080/"

def recipe_upload_view(request):

    return render(request, 'recipe_upload.html')

def images_view(request):
    recipes = Recipe.objects.prefetch_related('steps').all()

    context = {
        'recipes': recipes,
        'image_base_url': IMAGE_BASE_URL
    }

    return render(request,'images.html', context)

def delete_image(request):

    return redirect('images')
        