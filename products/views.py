from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from products.models import Product, Category
from products.serializers import (ProductSerializer,
                                  CategorySerializer,
                                  ProductListSerializer,
                                  ProductCreationSerializer,
                                  ProductShortSerializer)


# Create your views here.
@api_view(['GET', 'PUT', 'DELETE'])
def product_view(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        product.delete()
        return Response({"message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = ProductSerializer(product).data
    return Response(data)


@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    data = CategorySerializer(categories, many=True).data
    return Response(data)


@api_view(['GET'])
def get_products(request):
    paginator = PageNumberPagination()
    paginator.page_size = 2
    products = Product.objects.all()

    result_page = paginator.paginate_queryset(products, request)
    if products.count() > 1:
        serializer = ProductListSerializer(result_page)
    elif products.count() == 1:
        serializer = ProductShortSerializer(products.first())
    else:
        return Response({"error": "No products found"}, status=status.HTTP_404_NOT_FOUND)

    data = serializer.data

    return paginator.get_paginated_response(data)
    # return Response(data)


@api_view(['POST'])
def create_product(request):
    if request.method == 'POST':
        serializer = ProductCreationSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.errors)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
