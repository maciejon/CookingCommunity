from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('hello/', hello_world, name='hello-world'),
    # path('recipes/<int:id>/', recipe_detail, name='recipe-detail'),
    path('recipe/<slug:slug>/', recipe_detail, name='recipe-detail'),
    path('category/<slug:slug>/', category_detail, name='category-detail'),
    path('recipe_upload/', recipe_upload_view, name='recipe-upload')
]
