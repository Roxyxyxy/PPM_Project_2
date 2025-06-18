# Roxy's Shop - E-commerce Platform

## Project Information

**Author:** Roxana Merla (Matricola: 7074963)  
**Course:** Progettazione e Produzione Multimediale - Multimedia Design and Production 2024/2025
**Academic Year:** 2024-2025

## Features

- **User Authentication**: Register, login, and user profiles
- **Product Management**: Browse products by categories
- **Shopping Cart**: Add/remove items, adjust quantities
- **Checkout Process**: Secure payment processing
- **Order Management**: View order history and status
- **Admin Dashboard**: Manage products, view orders, and mark orders as complete

### Prerequisites

- Python 3.8+ installed
- pip package manager

### Installation

git clone https://github.com/yourusername/roxyshop.git cd roxyshop

2. Create a virtual environment

python -m venv env

3. Activate the virtual environment

On Windows
env\Scripts\activate

On macOS/Linux
source env/bin/activate

4. Install dependencies

pip install -r requirements.txt

### Database Setup

1. Run migrations

python manage.py migrate

2. (Optional) Load sample data

python manage.py loaddata initial_data.json

3. Create a superuser for admin access

python manage.py createsuperuser

### Running the Server

Start the development server:

The site will be accessible at http://127.0.0.1:8000/

### Access Information

- Admin panel: http://127.0.0.1:8000/admin/
- Store management: http://127.0.0.1:8000/management/
