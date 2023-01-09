from django.urls import path
from pages.views import validate_link, register_mechanic, mechanic_portal, client_login, client_signup


urlpatterns = [
    path("", validate_link),
    path("register", register_mechanic, name="register_mechanic"),
    path("mechanic-portal/<int:request_pk>/", mechanic_portal ,name="mechanic_portal"),
    #path("mechanic-requests/(?P<uuid>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/", mechanic_requests ,name="display_mechanic_requests")
    path("client-login", client_login, name="client_login"),
    path("client-signup", client_signup, name="client_signup"),
]
