from django.urls import path
from apps.users.views.user_registration import RegisterView
from apps.users.views.login import LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]