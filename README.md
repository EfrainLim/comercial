# Sistema de Liquidaciones

Sistema de gestión de liquidaciones para minerales, desarrollado con Django.

## Características

- Gestión de proveedores y facturadores
- Control de vehículos y conductores
- Registro de pesajes en balanza
- Gestión de lotes y campañas
- Análisis de laboratorio
- Cálculo de costos
- Valorización de minerales
- Liquidaciones automáticas
- Reportes en Excel y PDF

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Entorno virtual (recomendado)

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd sistema-comercial
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
Crear archivo `.env` en la raíz del proyecto con:
```
SECRET_KEY=tu-clave-secreta
DEBUG=True
```

5. Realizar migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Crear superusuario:
```bash
python manage.py createsuperuser
```

7. Iniciar servidor de desarrollo:
```bash
python manage.py runserver
```

## Estructura del Proyecto

- `usuarios/`: Gestión de usuarios y autenticación
- `entidades/`: Proveedores, vehículos y conductores
- `productos/`: Tipos de productos
- `balanza/`: Registro de pesajes
- `lotes/`: Gestión de lotes y campañas
- `laboratorio/`: Análisis y leyes
- `costos/`: Cálculo de costos
- `valorizacion/`: Valorización de minerales
- `liquidaciones/`: Proceso de liquidación
- `reportes/`: Generación de reportes

## Roles de Usuario

1. **Planta**
   - Crear/editar/eliminar Lote
   - Ingresar datos de Balanza
   - Crear vehículos, proveedores, conductores
   - Gestionar tipos de producto

2. **Laboratorio**
   - Crear y editar Ley (1 por lote)

3. **Comercial**
   - Ver todo
   - Crear Costos y Valorización
   - Realizar Liquidación

4. **Administrador**
   - Acceso total
   - Gestión de usuarios
   - Auditoría

## Contribución

1. Fork el proyecto
2. Crear rama para nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 