from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('view/<int:pk>/', views.view_inbox, name='view-inbox'),
    path('new/', views.new_inbox, name='new-inbox'),
    path('new-message/<int:pk>/', views.new_message, name='new-message')
]
