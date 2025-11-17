from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/submit/', views.submit_message, name='submit_message'),
    path('api/messages/', views.get_messages, name='get_messages'),
    path('api/delete/<int:message_id>/', views.delete_message, name='delete_message'),
]