from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('low-stock/', views.low_stock_report, name='low_stock'),
    path('overdue/', views.overdue_report, name='overdue'),
    path('upcoming-due/', views.upcoming_due_report, name='upcoming_due'),
]
