from django.urls import path
from . import views

app_name = 'liquidaciones'

urlpatterns = [
    path('', views.liquidacion_list, name='liquidacion_list'),
    path('nueva/', views.liquidacion_create, name='liquidacion_create'),
    path('<int:pk>/', views.liquidacion_detail, name='liquidacion_detail'),
    path('<int:pk>/editar/', views.liquidacion_update, name='liquidacion_update'),
    path('<int:pk>/eliminar/', views.liquidacion_delete, name='liquidacion_delete'),
    path('<int:pk>/finalizar/', views.liquidacion_finalizar, name='liquidacion_finalizar'),
    path('detalle/<int:pk>/actualizar/', views.liquidacion_detalle_update, name='liquidacion_detalle_update'),
    path('detalle/<int:pk>/eliminar/', views.liquidacion_detalle_delete, name='liquidacion_detalle_delete'),
] 