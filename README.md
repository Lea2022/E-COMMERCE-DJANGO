# E-COMMERCE-DJANGO

This is an e-commerce project built with Django. The application allows users to browse products, view details for each item, add products to their shopping cart, and proceed with purchases.

## Features

- **Product Management**: View, browse, and manage inventory.
- **Shopping Cart**: Add products to the cart and proceed to checkout.
- **User Authentication**: Register and log in to keep track of orders and cart contents.
- **Admin Interface**: Django admin panel to manage products, orders, and users.

## Technologies Used

- **Django**: Main backend framework.
- **SQLite**: Database used for development.
- **Bootstrap**: For responsive front-end design.
- **HTML/CSS/JavaScript**: For the user interface.

## Prerequisites

- Python 3.x
- pip (comes with Python installation)

## Installation

Clone this repository:

```bash
git clone <YOUR_REPOSITORY_URL>
cd E-COMMERCE-DJANGO


Create and activate a virtual environment:

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:   
    pip install -r requirements.txt

Apply database migrations:
    python manage.py migrate

Create a superuser to access the admin panel:
    python manage.py createsuperuser

Run the development server:
    python manage.py runserver



## Usage
Access the Store: Open http://127.0.0.1:8000/ in your browser. Browse the catalog and add items to the shopping cart.
Admin Panel: Log in to the Django admin panel at http://127.0.0.1:8000/admin/ with your superuser credentials to manage products, users, and orders.
Shopping and Checkout:
Add items to the cart.
View the cart to update quantities or proceed to checkout.
Once logged in, place orders directly from your cart.



Project Structure
store: Contains views, models, and templates for the store functionality.
ecommerce: General project configuration.
templates: HTML templates for the store pages and admin panel.
static: Static files (CSS, JavaScript, images).



Adding Products
You can add products either through the admin panel or by running a custom migration to preload products into the database.



Troubleshooting
If you encounter any issues with database setup or migrations, ensure you have applied all migrations (python manage.py migrate) and check that your virtual environment is active with dependencies installed.


License
This project is open-source and distributed under the MIT License.
