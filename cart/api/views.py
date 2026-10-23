from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from cart.services.cart_service import CartService
from .serilaizers import AddToCartSerializer, CartItemSerializer, UpdateCartItemSerializer

class AddToCartView(APIView):
    permission_classes= [IsAuthenticated]
    def post(self, request):
        serializer= AddToCartSerializer(data= request.data)
        serializer.is_valid(raise_exception= True)
        product= serializer.validated_data["product"]
        quantity= serializer.validated_data["quantity"]
        cart_item= CartService.add_item(user=request.user, product_id= product.id, quantity= quantity)
        response_serializer= CartItemSerializer(cart_item)

        return Response(response_serializer.data, status= status.HTTP_201_CREATED)

class CartView(APIView):
    permission_classes= [IsAuthenticated]
    def get(self, request):
        cart= CartService.get_cart(request.user)
        response_serializer=CartItemSerializer(cart.items.all(),many= True)

        return Response(response_serializer.data, status= status.HTTP_200_OK)

class CartItemDetailView(APIView):
    permission_classes= [IsAuthenticated]
    def patch(self, request, item_id):
        serializer= UpdateCartItemSerializer(data= request.data)
        serializer.is_valid(raise_exception= True)
        quantity= serializer.validated_data["quantity"]
        cart_item= CartService.update_item(user= request.user, item_id=item_id, quantity=quantity)
        response_serializer= CartItemSerializer(cart_item)

        return Response(response_serializer.data, status= status.HTTP_200_OK)

    def delete(self, request, item_id):
        CartService.remove_item(user= request.user, item_id=item_id)
        return Response({"message": "item removed from cart"}, status= status.HTTP_200_OK)
