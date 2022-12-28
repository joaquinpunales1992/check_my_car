
from django.contrib import admin
from django.urls import path, include
from pages.views import validate_link


urlpatterns = [
    path("", validate_link),
]
