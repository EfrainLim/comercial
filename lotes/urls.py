from django.urls import path
from . import views

app_name = 'lotes'

urlpatterns = [
    path('', views.lote_list, name='lote_list'),
    path('nuevo/', views.lote_create, name='lote_create'),
    path('<int:pk>/', views.lote_detail, name='lote_detail'),
    path('<int:pk>/editar/', views.lote_update, name='lote_update'),
    path('<int:pk>/eliminar/', views.lote_delete, name='lote_delete'),
    path('obtener-siguiente-codigo/<str:codigo_sistema>/', views.obtener_siguiente_codigo, name='obtener_siguiente_codigo'),
    path('campanas/', views.campana_list, name='campana_list'),
    path('campanas/nueva/', views.campana_create, name='campana_create'),
    path('campanas/<int:pk>/editar/', views.campana_update, name='campana_update'),
    path('campanas/<int:pk>/eliminar/', views.campana_delete, name='campana_delete'),
    path('campanas/<int:pk>/', views.campana_detail, name='campana_detail'),
    path('<int:pk>/agregar-a-campana/', views.lote_add_to_campana, name='lote_add_to_campana'),
    path('campanas/<int:pk>/agregar-lotes/', views.campana_agregar_lotes, name='campana_agregar_lotes'),
    path('campanas/<int:campana_pk>/quitar-lote/<int:lote_pk>/', views.campana_quitar_lote, name='campana_quitar_lote'),
    path('campanas/<int:pk>/finalizar/', views.campana_finalizar, name='campana_finalizar'),
] 