from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import Product, StockMovement, ProductCategory
from .forms import ProductForm, StockMovementForm


@login_required
def product_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')

    products = Product.objects.select_related('category').all()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(brand__icontains=query))
    if category:
        products = products.filter(category_id=category)

    categories = [(c.id, c.name) for c in ProductCategory.objects.filter(is_active=True)]
    return render(request, 'inventory/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category,
    })


@login_required
@require_http_methods(['GET', 'POST'])
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado correctamente.')
            return redirect('inventory:product_list')
    else:
        form = ProductForm()

    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Crear Producto'})


@login_required
@require_http_methods(['GET', 'POST'])
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('inventory:product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'inventory/product_form.html', {'form': form, 'product': product, 'title': 'Editar Producto'})


@login_required
@require_http_methods(['GET', 'POST'])
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.is_active = False
        product.save()
        messages.success(request, 'Producto desactivado correctamente.')
        return redirect('inventory:product_list')

    return render(request, 'inventory/product_confirm_delete.html', {'product': product})


@login_required
def stock_movement_list(request):
    movements = StockMovement.objects.select_related('product', 'user').order_by('-created_at')
    product_filter = request.GET.get('product', '')
    if product_filter:
        movements = movements.filter(product_id=product_filter)

    products = Product.objects.filter(is_active=True)
    return render(request, 'inventory/stock_movement_list.html', {
        'movements': movements,
        'products': products,
        'selected_product': product_filter,
    })


@login_required
@require_http_methods(['GET', 'POST'])
def stock_movement_create(request):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.user = request.user
            movement.save()
            messages.success(request, 'Movimiento de stock registrado correctamente.')
            return redirect('inventory:stock_movement_list')
    else:
        form = StockMovementForm()

    return render(request, 'inventory/stock_movement_form.html', {'form': form})
