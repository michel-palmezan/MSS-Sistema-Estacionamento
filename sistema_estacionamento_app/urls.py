from django.urls import path
#importa as funções de controle (controllers em MVC) que em django estão no views.py
from sistema_estacionamento_app import views

urlpatterns = [
    path("",views.home, name="home"),
    path("precoePromocao/", views.precoePromocao, name="precoePromocao"),
]
