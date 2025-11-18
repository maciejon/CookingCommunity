from django.shortcuts import render, redirect, get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *

@api_view(['GET'])
def hello_world(request):
    content = {'message': 'Hello, World! The connection from Django is successful!'}
    return Response(content, status=status.HTTP_200_OK)

@api_view(['GET'])
def index(request):
    content = {'title': 'Mam smaka na ptaka'}
    
    return Response(content, status=status.HTTP_200_OK)

@api_view(['GET'])
def recipe_detail(request, slug):
    try:
        recipe = Recipe.objects.get(slug=slug)
    except Recipe.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RecipeDetailSerializer(recipe)
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

GO_IMAGE_SERVICE_URL = "http://localhost:8080/upload"

def recipe_upload_view(request):

    return render('recipe_upload.html')
        