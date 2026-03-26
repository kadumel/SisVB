from django.urls import path
# from django.views.generic import TemplateView

from . import views

app_name = 'links'

urlpatterns = [
    # path("", views.indexLinks),
    path('', views.indexLinks, name='indexLinks'),
    path('painel/<int:id>/', views.painel, name='painel'),
]
   

