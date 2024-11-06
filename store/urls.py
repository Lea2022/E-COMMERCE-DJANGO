from django.urls import path
from . import views
from .views import store, cart, checkout, updateItem, processOrder
from .views import register, login_view  
from django.contrib.auth import views as auth_views

# Definición de las rutas (URLs) que corresponden a las vistas en la aplicación
urlpatterns = [
    path('', store, name="store"),  # Página principal de la tienda
    path('cart/', cart, name="cart"),  # Vista del carrito de compras
    path('checkout/', checkout, name="checkout"),  # Vista de la página de pago
    path('update_item/', updateItem, name="update_item"),  # Actualización de ítems del carrito
    path('process_order/', processOrder, name="process_order"),  # Procesamiento de la orden
    path('register/', register, name='register'),  # Ruta para el registro de usuarios
    path('login/', login_view, name='login'),
    path('payment_success/', views.payment_success, name='payment_success'),

]