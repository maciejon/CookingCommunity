from django.contrib import admin
from django.urls import path
from main.views import *

from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world, name='hello-world'),

    # path('recipes/<int:id>/', recipe_detail, name='recipe-detail'),
    path('top5/', top5, name='top5'),
    path('recipe/<slug:slug>/', recipe_detail, name='recipe-detail'),
    path('category/<slug:slug>/', category_detail, name='category-detail'),
    path('search/', search, name='search'),

    # path('recipe_upload/', recipe_upload_view, name='recipe-upload'),
    path('images/', images_view, name='images'),

    path('token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('create_review/', create_review, name='create_review'),
    path('update_review/', update_review, name='update_review'),

    path('recipe/upload/', RecipeManageView.as_view(), name='recipe-upload')
]
