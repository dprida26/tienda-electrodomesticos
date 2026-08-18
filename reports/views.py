from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import models
from datetime import timedelta
from inventory.models import Product
from credits.models import Installment


@login_required
def low_stock_report(request):
    products = Product.objects.filter(stock_quantity__lte=models.F('min_stock_quantity'), is_active=True).order_by('stock_quantity')
    return render(request, 'reports/low_stock.html', {'products': products})


@login_required
def overdue_report(request):
    overdue = Installment.objects.filter(status='PENDING', due_date__lt=timezone.now().date()).select_related('credit_sale__customer').order_by('due_date')
    return render(request, 'reports/overdue.html', {'overdue_installments': overdue})


@login_required
def upcoming_due_report(request):
    today = timezone.now().date()
    next_week = today + timedelta(days=7)
    upcoming = Installment.objects.filter(
        status='PENDING',
        due_date__gte=today,
        due_date__lte=next_week
    ).select_related('credit_sale__customer').order_by('due_date')
    return render(request, 'reports/upcoming_due.html', {'upcoming_installments': upcoming})
