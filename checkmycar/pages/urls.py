from django.urls import path
from pages.views import validate_link, register_mechanic


urlpatterns = [
    path("", validate_link),
    path("register", register_mechanic, name="register_mechanic")
]
