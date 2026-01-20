from django.shortcuts import render, redirect, get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView 
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.db.models import Q, Case, When, Value, IntegerField

import jwt
import time
import requests
from django.conf import settings

from .emails import send_welcome_email

from .models import *
from .serializers import *

IMAGE_BASE_URL = "http://127.0.0.1:8080/"

@api_view(['GET'])
def hello_world(request):
    content = {'message': 'Hello, World! The connection from Django is successful!'}
    return Response(content, status=status.HTTP_200_OK)

@api_view(['GET'])
def top5(request):
    recipes = Recipe.objects.all().order_by('-number_of_views')[:6]
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

        data = serializer.data
        
        if request.user.is_authenticated:
            data['requesting_user'] = request.user.username
        else:
            data['requesting_user'] = None
        return Response(data)

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

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_image(request):
    recipe_id = request.data.get('id')
    
    if not recipe_id:
        return Response({"error": "no id"}, status=400)

    recipe = get_object_or_404(Recipe, id=recipe_id, created_by=request.user)
    
    if not recipe.image:
        return Response({"message": "no photo for recipe"}, status=200)

    image_slug = recipe.image

    try:
        response = requests.delete(
            f"{IMAGE_BASE_URL}{image_slug}",
            headers={"API-Key": settings.IMAGE_SECRET_KEY},
            timeout=5
        )
        
        if response.status_code not in [200, 404]:
            return Response({"error": "IMAGE service error"}, status=502)
            
    except requests.RequestException:
        return Response({"error": "IMAGE service down"}, status=503)

    recipe.image = None
    recipe.save()

    return Response(status=200)

# ----------------------------------------------------------------------------------------------
# ------- KOBYŁA DO UPLOADU -------
# ----------------------------------------------------------------------------------------------

class RecipeManageView(APIView):
    permission_classes = [IsAuthenticated]

    def get_recipe_safe(self, recipe_id, user):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        
        if recipe.created_by != user and not user.is_superuser:
            return None 
            
        return recipe

    def get(self, request):
        categories = Category.objects.all()
        ingredients = Ingredient.objects.all()

        units = [
            {"value": value, "label": label} 
            for value, label in RecipeIngredient.Unit.choices
        ]

        return Response({
            "categories": CategorySerializer(categories, many=True).data,
            "ingredients": IngredientSerializer(ingredients, many=True).data,
            "units": units
        }, status=status.HTTP_200_OK)
    
    # upload
    def post(self, request):
        serializer = RecipeCreateSerializer(data=request.data)

        if serializer.is_valid():
            recipe:Recipe = serializer.save(created_by=request.user)
            
            img_slug = f"r_{recipe.id}_{int(time.time())}.jpg"
            recipe.image = img_slug
            recipe.save()
            
            payload = {
                "sub": request.user.id,
                "action": "upload_image",
                "filename": img_slug,  # nazwa pliku wymuszona
                "exp": int(time.time()) + 300
            }
            token = jwt.encode(payload, settings.IMAGE_SECRET_KEY, algorithm="HS256")
            
            return Response({
                "Upload-Token": token,
                "Upload-Url": IMAGE_BASE_URL + "upload"
            }, status=201)
            
        return Response(serializer.errors, status=400)
    
    # aktualizacja
    def put(self, request):
        recipe_id = request.data.get('id')
        if not recipe_id:
            return Response({"error": "no id"}, status=400)
            
        recipe = self.get_recipe_safe(recipe_id, request.user)

        if recipe is None:
            return Response({"error": "Nie można edytowac nie swojego przepisu"}, status=403)
        
        serializer = RecipeCreateSerializer(recipe, data=request.data, partial=True)
        
        if serializer.is_valid():
            with transaction.atomic():
                recipe = serializer.save()
                
                response_data = serializer.data
                
                # takie cos jak dokleic update_image
                if request.data.get('update_image'):
                    new_slug = f"r_{recipe.id}_{int(time.time())}"
                    recipe.image = new_slug
                    recipe.save()
                    
                    payload = {
                        "sub": request.user.id,
                        "action": "upload_image",
                        "filename": new_slug,
                        "exp": int(time.time()) + 300
                    }
                    token = jwt.encode(payload, settings.IMAGE_SECRET_KEY, algorithm="HS256")
                    
                    response_data["Upload-Token"] = token
                    response_data["Upload-Url"] = IMAGE_BASE_URL + "upload"
            
            return Response(response_data, status=200)
            
        return Response(serializer.errors, status=400)

    def delete(self, request):
        recipe_id = request.data.get('id') or request.query_params.get('id')
        
        if not recipe_id:
            return Response({"error": "no id"}, status=400)
            
        recipe = self.get_recipe_safe(recipe_id, request.user)

        if recipe is None:
            return Response({"error": "Nie można edytowac nie swojego przepisu"}, status=403)
        
        if recipe.image:
            try:
                requests.delete(
                    f"{IMAGE_BASE_URL}{recipe.image}", 
                    headers={"API-Key": settings.IMAGE_SECRET_KEY},
                    timeout=5
                )
            except requests.RequestException:
                print(f"error while deleting {recipe.image}")

        recipe.delete()
        
        return Response(status=200)


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

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])

        send_welcome_email(user.email, user.username)
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        access_max_age = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
        refresh_max_age = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()

        response.set_cookie(
            'access_token',
            access_token,
            max_age=access_max_age,
            httponly=True,
            samesite='Lax',
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        )
        response.set_cookie(
            'refresh_token',
            refresh_token,
            max_age=refresh_max_age,
            httponly=True,
            samesite='Lax',
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        )

        return response

# ----------------------------------------------------------------------------------------------
# ------- OBSŁUGA IMAGE -------
# ----------------------------------------------------------------------------------------------

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
        