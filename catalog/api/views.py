from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import CategorySerializer, ProductSerializer
from catalog.services.category_service import CategoryService
from catalog.services.product_service import ProductService
from accounts.permissions import IsAdmin, IsSellerOrAdmin
from django.shortcuts import get_object_or_404
from catalog.models import Product
from .pagination import ProductPagination

from django.core.cache import cache
from catalog.cache import get_product_cache_version, get_product_cache_key

class CategoryListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdmin()]
        return [IsAuthenticated()]

    def get(self, request):
        categories = CategoryService.get_all_categories()
        serializer = CategorySerializer(categories, many= True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    def post(self, request):
            
            serializer = CategorySerializer(data= request.data)
            serializer.is_valid(raise_exception= True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

class ProductListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsSellerOrAdmin()]
        return [IsAuthenticated()]

    # def get(self, request):
    #     products = ProductService.get_all_products()
    #     serializer = ProductSerializer(products, many= True)
    #     return Response(
    #         serializer.data,
    #         status=status.HTTP_200_OK
    #     )

    def get(self,request):
        category_id= request.query_params.get("category")
        search= request.query_params.get("search")
        sort_by= request.query_params.get("sort_by")
        order= request.query_params.get("order","asc")
        #version= get_product_cache_version()
        cache_key= get_product_cache_key(request)
        cached_data= cache.get(cache_key)
        if cached_data is not None:
            print("Cache hit")
            return Response(cached_data)
        print("Cache miss")
        products= ProductService.get_products(category_id=category_id, search= search, sort_by=sort_by, order_by= order)
        paginator= ProductPagination()
        paginated_products= paginator.paginate_queryset(products, request)
        serializer= ProductSerializer(paginated_products, many=True)
        response= paginator.get_paginated_response(serializer.data)
        cache.set(cache_key, response.data, timeout=60)
        print("Data stored in Cache")
        return response
    
    def post(self, request):
            
            serializer = ProductSerializer(data= request.data)
            serializer.is_valid(raise_exception= True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

class ProductDetailView(APIView):

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAdmin()]
        if self.request.method == "PATCH":
            return [IsSellerOrAdmin()]
        return [IsAuthenticated()]

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product)
        return Response(
             serializer.data,
             status = status.HTTP_200_OK
        )
    def patch(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product, data=request.data, partial= True)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(
                serializer.data,
                status = status.HTTP_200_OK
        )
    def delete(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return Response(
            {
                "message": "Product deleted successfully."
            },
            status = status.HTTP_200_OK
        )