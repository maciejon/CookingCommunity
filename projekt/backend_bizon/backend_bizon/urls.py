from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('hello/', hello_world, name='hello-world'),
    # path('')
]
