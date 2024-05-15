from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('homepage/', HomeView.as_view(), name='homepage'),
    path('interaction/', InteractionView.as_view(), name='interaction'),
    path('history/<int:user_id>/', HistoryView.as_view(), name='history'),
]
