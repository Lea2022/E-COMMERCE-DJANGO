from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json
import datetime
from .models import *  # Importa todos los modelos del archivo models.py
from .utils import cookieCart, cartData, guestOrder  # Funciones auxiliares para manejar el carrito y pedidos de invitados

def store(request):
    """Vista para la página principal de la tienda."""
    data = cartData(request)  # Obtiene los datos del carrito, usuario y productos
    
    # Se obtienen los ítems del carrito, la orden actual y los productos
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        try:
            # Intenta obtener el cliente asociado al usuario
            customer = request.user.customer
        except Customer.DoesNotExist:
            # Si no existe un cliente, se crea uno para el usuario
            customer = Customer.objects.create(user=request.user, name=request.user.username, email=request.user.email)
    
    # Obtiene todos los productos disponibles en la tienda
    products = Product.objects.all()
    
    # Envía los productos y la cantidad de ítems en el carrito al contexto para renderizar en el template
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)  # Renderiza la vista con el contexto

def cart(request):
    """Vista para la página del carrito de compras."""
    data = cartData(request)  # Obtiene los datos del carrito

    cartItems = data['cartItems']  # Cantidad de ítems en el carrito
    order = data['order']  # Orden actual
    items = data['items']  # Ítems del carrito

    # Contexto para renderizar el carrito de compras
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)  # Renderiza la vista del carrito con el contexto

def checkout(request):
    """Vista para la página de pago (checkout)."""
    data = cartData(request)  # Obtiene los datos del carrito

    cartItems = data['cartItems']  # Cantidad de ítems en el carrito
    order = data['order']  # Orden actual
    items = data['items']  # Ítems del carrito

    # Contexto para renderizar la vista de checkout
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)  # Renderiza la vista de checkout con el contexto

def updateItem(request):
    """Actualiza la cantidad de un ítem en el carrito de compras."""
    data = json.loads(request.body)  # Carga el cuerpo de la solicitud como JSON
    productId = data['productId']  # Obtiene el ID del producto
    action = data['action']  # Obtiene la acción ('add' para agregar o 'remove' para quitar)
    
    # Imprime la acción y el producto en la consola (para depuración)
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer  # Obtiene el cliente autenticado
    product = Product.objects.get(id=productId)  # Obtiene el producto a partir del ID
    order, created = Order.objects.get_or_create(customer=customer, complete=False)  # Obtiene o crea la orden del cliente

    # Obtiene o crea el ítem de la orden correspondiente al producto
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    # Aumenta o disminuye la cantidad del ítem dependiendo de la acción
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()  # Guarda los cambios en el ítem de la orden

    # Si la cantidad del ítem es 0 o menos, lo elimina
    if orderItem.quantity <= 0:
        orderItem.delete()

    # Devuelve una respuesta JSON indicando que el ítem fue agregado o actualizado
    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    """Procesa la orden de compra cuando se completa el pago."""
    transaction_id = datetime.datetime.now().timestamp()  # Genera un ID de transacción único basado en el tiempo
    data = json.loads(request.body)  # Carga los datos enviados como JSON

    # Si el usuario está autenticado, usa su cuenta para crear o recuperar la orden
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        # Si es un usuario invitado, crea la orden usando la función guestOrder
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])  # Obtiene el total de la orden desde el formulario enviado
    order.transaction_id = transaction_id  # Asigna el ID de la transacción a la orden

    # Verifica si el total enviado coincide con el total calculado en la orden
    if total == order.get_cart_total:
        order.complete = True  # Marca la orden como completa
    order.save()  # Guarda la orden

    # Si la orden requiere envío, crea la dirección de envío
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    # Devuelve una respuesta JSON indicando que el pago fue enviado correctamente
    return JsonResponse('Payment submitted..', safe=False)


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, 'Usuario creado con éxito.')
            return redirect('login')  # Redirigir a la página de inicio de sesión
        except Exception as e:
            messages.error(request, str(e))
    
    return render(request, 'registration/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')  # Redirige a la tienda
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')

            return render(request, 'registration/login.html', {'error': 'Credenciales inválidas.'})
    return render(request, 'registration/login.html')



def payment_success(request):
    return render(request, 'store/payment_success.html')