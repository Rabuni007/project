from django.urls import path
from . import views

urlpatterns = [
    path('distributors/', views.distributor_list_create, name='distributor-list-create'),
    path('distributors/<int:pk>/', views.distributor_retrieve_update, name='distributor-retrieve-update'),
    path('payments/', views.payment_list_create, name='payment-list-create'),
    path('payments/<int:pk>/', views.payment_retrieve, name='payment-retrieve'),
    path('payments/<int:pk>/confirm/', views.payment_confirm, name='payment-confirm'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
]
