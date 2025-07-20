from django.urls import path
from . import views

app_name = 'valorizacion'

urlpatterns = [
    path('', views.valorizacion_list, name='valorizacion_list'),
    path('nueva/', views.valorizacion_create, name='valorizacion_create'),
    path('<int:pk>/', views.valorizacion_detail, name='valorizacion_detail'),
    path('<int:pk>/editar/', views.valorizacion_update, name='valorizacion_update'),
    path('<int:pk>/eliminar/', views.valorizacion_delete, name='valorizacion_delete'),
] 