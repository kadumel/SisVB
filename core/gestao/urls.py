from django.urls import include, path

from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("alterar-senha/", views.change_password, name="change_password"),
    path("", include("links.urls")),
]
