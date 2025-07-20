from django.urls import path
from . import views

app_name = 'entidades'

urlpatterns = [
    # URLs para Facturador
    path('facturadores/', views.facturador_list, name='facturador_list'),
    path('facturadores/nuevo/', views.facturador_create, name='facturador_create'),
    path('facturadores/<int:pk>/', views.facturador_detail, name='facturador_detail'),
    path('facturadores/<int:pk>/editar/', views.facturador_update, name='facturador_update'),
    path('facturadores/<int:pk>/eliminar/', views.facturador_delete, name='facturador_delete'),
    
    # URLs para Vehiculo
    path('vehiculos/', views.vehiculo_list, name='vehiculo_list'),
    path('vehiculos/nuevo/', views.vehiculo_create, name='vehiculo_create'),
    path('vehiculos/<int:pk>/', views.vehiculo_detail, name='vehiculo_detail'),
    path('vehiculos/<int:pk>/editar/', views.vehiculo_update, name='vehiculo_update'),
    path('vehiculos/<int:pk>/eliminar/', views.vehiculo_delete, name='vehiculo_delete'),
    
    # URLs para Conductor
    path('conductores/', views.conductor_list, name='conductor_list'),
    path('conductores/nuevo/', views.conductor_create, name='conductor_create'),
    path('conductores/<int:pk>/', views.conductor_detail, name='conductor_detail'),
    path('conductores/<int:pk>/editar/', views.conductor_update, name='conductor_update'),
    path('conductores/<int:pk>/eliminar/', views.conductor_delete, name='conductor_delete'),
    
    # URLs para ProveedorIngemmet
    path('proveedores-ingemmet/', views.proveedor_ingemmet_list, name='proveedor_ingemmet_list'),
    path('proveedores-ingemmet/nuevo/', views.proveedor_ingemmet_create, name='proveedor_ingemmet_create'),
    path('proveedores-ingemmet/<int:pk>/', views.proveedor_ingemmet_detail, name='proveedor_ingemmet_detail'),
    path('proveedores-ingemmet/<int:pk>/editar/', views.proveedor_ingemmet_update, name='proveedor_ingemmet_update'),
    path('proveedores-ingemmet/<int:pk>/eliminar/', views.proveedor_ingemmet_delete, name='proveedor_ingemmet_delete'),
    
    # URLs para TipoProducto
    path('tipos-producto/', views.TipoProductoListView.as_view(), name='tipo_producto_list'),
    path('tipos-producto/nuevo/', views.TipoProductoCreateView.as_view(), name='tipo_producto_create'),
    path('tipos-producto/<int:pk>/editar/', views.TipoProductoUpdateView.as_view(), name='tipo_producto_update'),
    path('tipos-producto/<int:pk>/eliminar/', views.TipoProductoDeleteView.as_view(), name='tipo_producto_delete'),
] 