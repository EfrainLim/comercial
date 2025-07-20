from django.urls import path
from . import views

app_name = 'balanza'

urlpatterns = [
    path('', views.balanza_list, name='balanza_list'),
    path('nuevo/', views.balanza_create, name='balanza_create'),
    path('<int:pk>/', views.balanza_detail, name='balanza_detail'),
    path('<int:pk>/editar/', views.balanza_update, name='balanza_update'),
    path('<int:pk>/eliminar/', views.balanza_delete, name='balanza_delete'),
    path('obtener-lotes-temporales/', views.obtener_lotes_temporales, name='obtener_lotes_temporales'),
] 