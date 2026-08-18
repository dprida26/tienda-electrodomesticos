from django.urls import path
from . import views

app_name = 'credits'

urlpatterns = [
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('customers/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('sales/', views.credit_sale_list, name='credit_sale_list'),
    path('sales/create/', views.credit_sale_create, name='credit_sale_create'),
    path('sales/<int:pk>/', views.credit_sale_detail, name='credit_sale_detail'),
    path('installments/<int:installment_id>/pay/', views.payment_register, name='payment_register'),
    path('installments/<int:installment_id>/payments/', views.installment_payments, name='installment_payments'),
]
