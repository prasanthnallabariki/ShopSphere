from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from orders.api.pagination import OrderPagination

from orders.services.order_service import OrderService
from .serializers import OrderSerializer

class CheckoutView(APIView):
    permission_classes= [IsAuthenticated]
    def post(self, request):
        order= OrderService.checkout(request.user)
        serializer=OrderSerializer(order)
        return Response(serializer.data, status= status.HTTP_201_CREATED)

class OrderListView(APIView):
    permission_classes= [IsAuthenticated]
    def get(self, request):
        status_filter= request.query_params.get("status")
        sort_by= request.query_params.get("sort_by", "-created_at")
        orders= OrderService.get_user_orders(user=request.user, status_filter=status_filter, sort_by=sort_by)
        paginator= OrderPagination()
        page= paginator.paginate_queryset(orders, request)
        serializer= OrderSerializer(page, many= True)
        return paginator.get_paginated_response(serializer.data)

class OrderDetailView(APIView):
    permission_classes= [IsAuthenticated]
    def get(self, request, order_id):
        order= OrderService.get_order(order_id, request.user)
        serializer= OrderSerializer(order)
        return Response(serializer.data, status= status.HTTP_200_OK)

    def post(self, request, order_id):
        order= OrderService.cancel_order(order_id, request.user)
        return Response({
            "message": "Order cancelled successfully",
            "order_id": order.id,
            "status": order.status
        },
        status= status.HTTP_200_OK)