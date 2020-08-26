from django.contrib import admin
from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('<int:id>', views.deactivate_user, name = 'deactivate'),
    path('mail/', views.mail_user, name = 'send_mail'),
]