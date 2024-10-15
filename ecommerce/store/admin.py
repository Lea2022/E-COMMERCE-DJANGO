from django.contrib import admin
from .models import *

# Registro de los modelos para que sean accesibles desde el panel de administración de Django

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
