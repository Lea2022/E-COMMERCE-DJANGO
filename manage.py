#!/usr/bin/env python
"""Utilidad de línea de comandos de Django para tareas administrativas."""
import os
import sys

def main():
    """Ejecuta las tareas administrativas de Django."""
    
    # Establece la configuración predeterminada del proyecto Django (archivo settings.py dentro de ecommerce)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
    
    try:
        # Importa la función para ejecutar comandos desde la línea de comandos de Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Si Django no se pudo importar, muestra un error indicando posibles problemas
        raise ImportError(
            "No se pudo importar Django. ¿Estás seguro de que está instalado "
            "y disponible en la variable de entorno PYTHONPATH? ¿Olvidaste "
            "activar el entorno virtual?"
        ) from exc
    
    # Ejecuta el comando pasado desde la línea de comandos
    execute_from_command_line(sys.argv)

# Si este archivo es ejecutado directamente (no importado), llama a la función main()
if __name__ == '__main__':
    main()