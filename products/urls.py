from django.urls import path, re_path
from products.views import product_view, get_categories, get_products, create_product

app_name = 'products'

urlpatterns = [
    path('products/<int:product_id>', product_view, name='products'),
    path('categories/', get_categories, name='categories'),
    path('products/', get_products, name='products'),
    path('products/create/', create_product, name='create_product'),
]
