from django.shortcuts import render, redirect, get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView 
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.db.models import Q, Case, When, Value, IntegerField

import requests
from django.conf import settings

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request):
    # input: { "recipe_id": 1, "stars": 1, "text": "niejadalne!" } uwaga dac id
    recipe_id = request.data.get('recipe_id')
    if not recipe_id:
        return Response({"detail": "insert recipe id"}, status=status.HTTP_400_BAD_REQUEST)

    recipe = get_object_or_404(Recipe, id=recipe_id)

    if Review.objects.filter(user=request.user, recipe=recipe).exists():
        return Response(
            {"detail": "one user one review"}, 
            status=status.HTTP_409_CONFLICT
        )
    serializer = ReviewSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(user=request.user, recipe=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_review(request):
    recipe_id = request.data.get('recipe_id')
    if not recipe_id:
        return Response({"detail": "insert recipe id"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        review = Review.objects.get(user=request.user, recipe__id=recipe_id)
    except Review.DoesNotExist:
        return Response(
            {"detail": "review not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = ReviewSerializer(review, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recipe_upload(request):
    if request.method == 'POST':
        request.headers['API-Key'] = settings.IMAGE_SECRET_KEY

    return render(request, 'recipe_upload.html')

# ----------------------------------------------------------------------------------------------
# ------- LOGOWANIE -------
# ----------------------------------------------------------------------------------------------

class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('access'):
            access_max_age = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
            refresh_max_age = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
            
            # cookie access
            response.set_cookie(
                'access_token',
                response.data['access'],
                max_age=access_max_age,
                httponly=True,
                samesite='Lax',
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            )
            
            # cookie refresh
            if response.data.get('refresh'):
                response.set_cookie(
                    'refresh_token',
                    response.data['refresh'],
                    max_age=refresh_max_age,
                    httponly=True,
                    samesite='Lax',
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                )
            
            del response.data['access']
            if response.data.get('refresh'):
                del response.data['refresh']
                
        return super().finalize_response(request, response, *args, **kwargs)

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        if 'refresh_token' in request.COOKIES:
            request.data['refresh'] = request.COOKIES['refresh_token']
        
        response = super().post(request, *args, **kwargs)
        
        if response.data.get('access'):
            access_max_age = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
            response.set_cookie(
                'access_token',
                response.data['access'],
                max_age=access_max_age,
                httponly=True,
                samesite='Lax',
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            )
            del response.data['access']

        # rotacja
        if response.data.get('refresh'):
            refresh_max_age = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
            response.set_cookie(
                'refresh_token',
                response.data['refresh'],
                max_age=refresh_max_age,
                httponly=True,
                samesite='Lax',
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            )
            del response.data['refresh']
            
        return response

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except TokenError:
            pass

        response = Response({"message": "Wylogowano"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,) 
    serializer_class = RegisterSerializer

# ----------------------------------------------------------------------------------------------
# ------- OBSŁUGA IMAGE -------
# ----------------------------------------------------------------------------------------------

IMAGE_BASE_URL = "http://localhost:8080/"

# def recipe_upload_view(request):
#     if request.method == 'POST':
#         request.headers['API-Key'] = settings.IMAGE_SECRET_KEY

#     return render(request, 'recipe_upload.html')

def images_view(request):
    recipes = Recipe.objects.prefetch_related('steps').all()

    context = {
        'recipes': recipes,
        'image_base_url': IMAGE_BASE_URL
    }

    return render(request,'images.html', context)

def delete_image(request):

    return redirect('images')
        