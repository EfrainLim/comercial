from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('', views.reporte_list, name='reporte_list'),
    path('crear/', views.reporte_create, name='reporte_create'),
    path('<int:pk>/descargar/', views.reporte_download, name='reporte_download'),
    path('<int:pk>/eliminar/', views.reporte_delete, name='reporte_delete'),
    path('balanza/<int:balanza_id>/pdf/', views.balanza_pdf, name='balanza_pdf'),
    path('liquidacion/<int:liquidacion_id>/pdf/', views.liquidacion_pdf, name='liquidacion_pdf'),
] 