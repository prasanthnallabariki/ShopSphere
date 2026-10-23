from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, ProfileView, LogoutView, CustomerDashboardView, SellerDashboardView, AdminDashboardView, CustomTokenObtainPairView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(),name="login"),
    path("profile/", ProfileView.as_view(),name="profile"),
    path("refresh/", TokenRefreshView.as_view(),name="refresh"),
    path("logout/", LogoutView.as_view(),name="logout"),
    path("customer/dashboard/", CustomerDashboardView.as_view(),name="customer-dashboard"),
    path("seller/dashboard/", SellerDashboardView.as_view(),name="seller-dashboard"),
    path("admin/dashboard/", AdminDashboardView.as_view(),name="admin-dashboard"),

]