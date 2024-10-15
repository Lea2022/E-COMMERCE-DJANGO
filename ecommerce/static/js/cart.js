// Obtiene todos los botones con la clase 'update-cart'
var updateBtns = document.getElementsByClassName('update-cart')

// Recorre cada botón para agregar un evento 'click'
for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		// Obtiene el ID del producto y la acción del botón
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)

		// Verifica si el usuario está autenticado
		if (user == 'AnonymousUser'){
			addCookieItem(productId, action) // Si no está autenticado, llama a la función para agregar al carrito en cookies
		}else{
			updateUserOrder(productId, action) // Si está autenticado, llama a la función para actualizar el pedido del usuario
		}
	})
}

// Función para actualizar el pedido del usuario autenticado
function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

	var url = '/update_item/' // URL donde se envían los datos

	fetch(url, {
		method:'POST', // Método de la petición
		headers:{
			'Content-Type':'application/json', // Tipo de contenido
			'X-CSRFToken':csrftoken, // Token CSRF para seguridad
		}, 
		body:JSON.stringify({'productId':productId, 'action':action}) // Datos a enviar en formato JSON
	})
	.then((response) => {
	   return response.json(); // Convierte la respuesta en JSON
	})
	.then((data) => {
	    location.reload() // Recarga la página para actualizar el contenido
	});
}

// Función para agregar elementos al carrito en cookies
function addCookieItem(productId, action){
	console.log('User is not authenticated')

	// Si la acción es agregar un producto
	if (action == 'add'){
		if (cart[productId] == undefined){
			// Si el producto no está en el carrito, lo añade
			cart[productId] = {'quantity':1}
		}else{
			// Si ya está en el carrito, aumenta la cantidad
			cart[productId]['quantity'] += 1
		}
	}

	// Si la acción es eliminar un producto
	if (action == 'remove'){
		cart[productId]['quantity'] -= 1 // Disminuye la cantidad

		// Si la cantidad es menor o igual a cero, elimina el producto del carrito
		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart) // Muestra el carrito en la consola
	// Almacena el carrito en una cookie
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload() // Recarga la página para actualizar el contenido
}