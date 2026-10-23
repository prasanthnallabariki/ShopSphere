from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, LogoutSerializer 
from accounts.permissions import IsCustomer, IsSeller, IsAdmin
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.throttling import ScopedRateThrottle

class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "User registered successfully."
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class ProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def  get(self,request):
        return Response({
            "message":"Acess granted to profile view",
            "user_id":request.user.id,
            "username":request.user.username,
            "email":request.user.email,
        })

class CustomTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"

class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = LogoutSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            {"message": "Logout successful"},
            status=status.HTTP_205_RESET_CONTENT
        )

class CustomerDashboardView(APIView):
    permission_classes=[IsCustomer]

    def get(self,request):
        return Response({
            "message":"Access granted to customer dashboard",
            "user_id": request.user.id,
            "username": request.user.username,
            "role": request.user.role,
            "email": request.user.email
        })
class SellerDashboardView(APIView):
    permission_classes=[IsSeller]

    def get(self,request):
        return Response({
            "message":"Access granted to seller dashboard",
            "user_id": request.user.id,
            "username": request.user.username,
            "role": request.user.role,
            "email": request.user.email
        })

class AdminDashboardView(APIView):
    permission_classes=[IsAdmin]

    def get(self,request):
        return Response({
            "message":"Access granted to Admin dashboard",
            "user_id": request.user.id,
            "username": request.user.username,
            "role": request.user.role,
            "email": request.user.email
        })