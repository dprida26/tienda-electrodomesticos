from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as rest_status
from .models import Customer, CreditSale, Installment, Payment, CreditConfiguration
from .forms import CustomerForm, CreditSaleForm, CreditSaleItemFormSet, PaymentForm
from .services import generate_installment_schedule
from .serializers import CreditConfigurationSerializer
from inventory.models import StockMovement


@login_required
def customer_list(request):
    query = request.GET.get('q', '')
    customers = Customer.objects.all()
    if query:
        customers = customers.filter(
            Q(full_name__icontains=query) | Q(document_number__icontains=query)
        )
    return render(request, 'credits/customer_list.html', {'customers': customers, 'query': query})


@login_required
@require_http_methods(['GET', 'POST'])
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado correctamente.')
            return redirect('credits:customer_list')
    else:
        form = CustomerForm()
    return render(request, 'credits/customer_form.html', {'form': form, 'title': 'Crear Cliente'})


@login_required
@require_http_methods(['GET', 'POST'])
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('credits:customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'credits/customer_form.html', {'form': form, 'customer': customer, 'title': 'Editar Cliente'})


@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    sales = customer.credit_sales.all()
    return render(request, 'credits/customer_detail.html', {
        'customer': customer,
        'sales': sales,
    })


@login_required
def credit_sale_list(request):
    status = request.GET.get('status', '')
    sales = CreditSale.objects.select_related('customer').order_by('-start_date')
    if status:
        sales = sales.filter(status=status)
    return render(request, 'credits/credit_sale_list.html', {
        'sales': sales,
        'statuses': CreditSale.STATUS_CHOICES,
        'selected_status': status,
    })


@login_required
@require_http_methods(['GET', 'POST'])
def credit_sale_create(request):
    if request.method == 'POST':
        form = CreditSaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.created_by = request.user
            sale.save()
            generate_installment_schedule(sale)
            messages.success(request, 'Venta a crédito creada con cronograma de cuotas.')
            return redirect('credits:credit_sale_detail', pk=sale.pk)
    else:
        form = CreditSaleForm()
    return render(request, 'credits/credit_sale_form.html', {'form': form, 'title': 'Crear Venta a Crédito'})


@login_required
def credit_sale_detail(request, pk):
    sale = get_object_or_404(CreditSale, pk=pk)
    installments = sale.installments.order_by('number')
    return render(request, 'credits/credit_sale_detail.html', {
        'sale': sale,
        'installments': installments,
        'items': sale.items.all(),
    })


@login_required
@require_http_methods(['GET', 'POST'])
def payment_register(request, installment_id):
    installment = get_object_or_404(Installment, pk=installment_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.installment = installment
            payment.registered_by = request.user
            payment.save()
            messages.success(request, f'Pago de ${payment.amount} registrado correctamente.')
            return redirect('credits:credit_sale_detail', pk=installment.credit_sale.pk)
    else:
        form = PaymentForm(initial={'amount': installment.pending_amount, 'paid_at': None})
    return render(request, 'credits/payment_form.html', {'form': form, 'installment': installment})


@login_required
def installment_payments(request, installment_id):
    installment = get_object_or_404(Installment, pk=installment_id)
    payments = installment.payments.all()
    return render(request, 'credits/installment_payments.html', {
        'installment': installment,
        'payments': payments,
    })


class CreditConfigurationAPIView(APIView):
    """API para obtener la configuración de créditos"""

    def get(self, request):
        config = CreditConfiguration.get_config()
        serializer = CreditConfigurationSerializer(config)
        return Response(serializer.data)
