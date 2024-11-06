from django.db import models
from django.contrib.auth.models import User

# Creación de los modelos aquí.

# Modelo para representar a un cliente
class Customer(models.Model):
    # Relación uno a uno con el modelo User para conectar un cliente con un usuario del sistema de autenticación de Django
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name="customer")
    
    # Campos adicionales para el cliente
    name = models.CharField(max_length=200, null=True)  # Nombre del cliente
    email = models.CharField(max_length=200)  # Correo electrónico del cliente

    # Método para devolver el nombre del cliente como representación del objeto
    def __str__(self):
        return self.name


# Modelo para representar un producto en la tienda
class Product(models.Model):
    name = models.CharField(max_length=200)  # Nombre del producto
    price = models.FloatField()  # Precio del producto
    digital = models.BooleanField(default=False, null=True, blank=True)  # Indica si el producto es digital o físico
    image = models.ImageField(null=True, blank=True)  # Imagen del producto, opcional

    # Método para devolver el nombre del producto como representación del objeto
    def __str__(self):
        return self.name

    # Propiedad para obtener la URL de la imagen del producto
    @property
    def imageURL(self):
        try:
            url = self.image.url  # Obtiene la URL si existe una imagen
        except:
            url = ''  # Si no hay imagen, devuelve una cadena vacía
        return url


# Modelo para representar una orden de compra
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)  # Cliente asociado a la orden
    date_ordered = models.DateTimeField(auto_now_add=True)  # Fecha en la que se realizó la orden
    complete = models.BooleanField(default=False)  # Indica si la orden está completa
    transaction_id = models.CharField(max_length=100, null=True)  # ID de transacción para la orden

    # Método para devolver el ID de la orden como representación del objeto
    def __str__(self):
        return str(self.id)
    
    # Propiedad que indica si la orden requiere envío (si al menos uno de los productos no es digital)
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()  # Obtiene todos los elementos de la orden
        for i in orderitems:
            if i.product.digital == False:
                shipping = True  # Requiere envío si algún producto no es digital
        return shipping

    # Propiedad para obtener el total de la orden sumando los totales de cada ítem
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])  # Suma los totales de cada ítem en la orden
        return total 

    # Propiedad para obtener el número total de ítems en el carrito
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])  # Suma las cantidades de cada ítem en la orden
        return total 


# Modelo para representar un ítem dentro de una orden
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)  # Producto asociado al ítem
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)  # Orden a la que pertenece el ítem
    quantity = models.IntegerField(default=0, null=True, blank=True)  # Cantidad del producto
    date_added = models.DateTimeField(auto_now_add=True)  # Fecha en la que se añadió el ítem

    # Propiedad para calcular el total de este ítem multiplicando el precio por la cantidad
    @property
    def get_total(self):
        total = self.product.price * self.quantity  # Total = precio del producto * cantidad
        return total


# Modelo para representar una dirección de envío
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)  # Cliente asociado a la dirección
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)  # Orden asociada a la dirección
    address = models.CharField(max_length=200, null=False)  # Dirección de envío
    city = models.CharField(max_length=200, null=False)  # Ciudad
    state = models.CharField(max_length=200, null=False)  # Estado/Provincia
    zipcode = models.CharField(max_length=200, null=False)  # Código postal
    date_added = models.DateTimeField(auto_now_add=True)  # Fecha en la que se añadió la dirección

    # Método para devolver la dirección como representación del objeto
    def __str__(self):
        return self.address