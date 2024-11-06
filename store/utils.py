import json
from .models import *  # Importa todos los modelos del archivo models.py

def cookieCart(request):
    """
    Maneja el carrito de compras de usuarios no autenticados usando cookies.
    Si no hay un carrito, crea uno vacío.
    """
    # Intenta cargar el carrito desde las cookies del navegador
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        # Si no existe la cookie 'cart', crea un carrito vacío
        cart = {}
        print('CARRITO:', cart)

    # Inicializa las variables del carrito
    items = []  # Lista de ítems en el carrito
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}  # Información de la orden
    cartItems = order['get_cart_items']  # Cantidad total de ítems en el carrito

    # Recorre los ítems en el carrito almacenado en las cookies
    for i in cart:
        # Se usa un bloque try para evitar errores si un producto fue eliminado
        try:
            cartItems += cart[i]['quantity']  # Suma la cantidad de ítems al total del carrito

            product = Product.objects.get(id=i)  # Obtiene el producto por su ID
            total = (product.price * cart[i]['quantity'])  # Calcula el total para ese producto

            # Actualiza el total de la orden y la cantidad de ítems
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            # Crea un diccionario que representa el ítem del carrito
            item = {
                'id': product.id,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart[i]['quantity'],
                'digital': product.digital,
                'get_total': total,
            }
            items.append(item)  # Agrega el ítem a la lista de ítems del carrito

            # Si el producto no es digital, requiere envío
            if product.digital == False:
                order['shipping'] = True
        except:
            # Si ocurre un error (por ejemplo, si el producto fue eliminado), se ignora el ítem
            pass

    # Devuelve la información del carrito, la orden y los ítems
    return {'cartItems': cartItems, 'order': order, 'items': items}

def cartData(request):
    """
    Obtiene los datos del carrito, ya sea para un usuario autenticado o no autenticado.
    """
    # Si el usuario está autenticado, se obtiene su orden y sus ítems
    if request.user.is_authenticated:
        customer = request.user.customer  # Obtiene el cliente autenticado
        order, created = Order.objects.get_or_create(customer=customer, complete=False)  # Crea o recupera la orden
        items = order.orderitem_set.all()  # Obtiene todos los ítems de la orden
        cartItems = order.get_cart_items  # Obtiene la cantidad de ítems en el carrito
    else:
        # Si el usuario no está autenticado, usa los datos almacenados en las cookies
        cookieData = cookieCart(request)  # Obtiene los datos del carrito de las cookies
        cartItems = cookieData['cartItems']  # Cantidad de ítems en el carrito
        order = cookieData['order']  # Información de la orden
        items = cookieData['items']  # Ítems en el carrito

    # Devuelve los datos del carrito, la orden y los ítems
    return {'cartItems': cartItems, 'order': order, 'items': items}

def guestOrder(request, data):
    """
    Crea una orden para un usuario invitado (no autenticado) basado en los datos del formulario y las cookies.
    """
    name = data['form']['name']  # Obtiene el nombre del formulario
    email = data['form']['email']  # Obtiene el email del formulario

    cookieData = cookieCart(request)  # Obtiene los ítems del carrito almacenado en las cookies
    items = cookieData['items']  # Ítems del carrito

    # Crea o recupera un cliente basado en el email proporcionado
    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name  # Asigna el nombre al cliente
    customer.save()  # Guarda el cliente

    # Crea una orden para el cliente
    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    # Crea ítems de la orden basados en los ítems del carrito
    for item in items:
        product = Product.objects.get(id=item['id'])  # Obtiene el producto por su ID
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )

    # Devuelve el cliente y la orden creada
    return customer, order