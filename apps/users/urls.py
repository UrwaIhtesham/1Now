from django.urls import path
from apps.users.views.user_registration import RegisterView
from apps.users.views.login import LoginView
from apps.users.views.create_list_vehicle import VehicleListCreateView
from apps.users.views.vehicle_management import VehicleManagementView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('vehicles/', VehicleListCreateView.as_view(), name='add-list-vehicle'),
    path('vehicles/<int:id>/', VehicleManagementView.as_view(), name='update-delete-vehicle'),
]