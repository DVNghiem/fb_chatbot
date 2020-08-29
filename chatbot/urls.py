from django.urls import path
from . import views

urlpatterns = [
    path('chatbot/', views.BotView.as_view(), name='chatbot')
]