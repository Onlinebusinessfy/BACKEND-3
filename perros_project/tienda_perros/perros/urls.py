from django.urls import path
from . import views

urlpatterns = [

    path('', views.home_page),

    path('dogs/', views.listar_perros),

    path('dogs/<int:id>/', views.obtener_perro),

    path(
        'dogs/breed/<str:raza>/',
        views.perros_por_raza
    ),

    path(
        'dogs/search/<str:nombre>/',
        views.buscar_perro
    ),

    path(
        'dogs/adoptable/',
        views.perros_adoptables
    ),

]