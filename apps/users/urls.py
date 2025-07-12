from django.urls import path
from apps.users.views.user_registration import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

]