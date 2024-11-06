from django.apps import AppConfig

# Clase de configuración de la aplicación Store
class StoreConfig(AppConfig):
    # Especifica el tipo de campo auto-incremental por defecto para los modelos
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Nombre de la aplicación, debe coincidir con el nombre de la carpeta donde está la app
    name = 'store'

    def ready(self):
        import store.signals # Importa las señales cuando la app está lista