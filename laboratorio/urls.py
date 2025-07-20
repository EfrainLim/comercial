from django.urls import path
from . import views

app_name = 'laboratorio'

urlpatterns = [
    path('', views.ley_list, name='ley_list'),
    path('nueva/', views.ley_create, name='ley_create'),
    path('<int:pk>/', views.ley_detail, name='ley_detail'),
    path('<int:pk>/editar/', views.ley_update, name='ley_update'),
    path('<int:pk>/eliminar/', views.ley_delete, name='ley_delete'),
] 