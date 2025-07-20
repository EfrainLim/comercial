from django.urls import path
from . import views

app_name = 'costos'

urlpatterns = [
    path('', views.costo_list, name='costo_list'),
    path('crear/', views.costo_create, name='costo_create'),
    path('<int:pk>/', views.costo_detail, name='costo_detail'),
    path('<int:pk>/editar/', views.costo_update, name='costo_update'),
    path('<int:pk>/eliminar/', views.costo_delete, name='costo_delete'),
] 