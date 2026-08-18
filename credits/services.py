from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from .models import CreditSale, Installment


def generate_installment_schedule(credit_sale):
    """
    Genera el cronograma de cuotas para una venta a crédito.
    Divide el monto total en N cuotas iguales, ajustando centavos en la última cuota.
    """
    Installment.objects.filter(credit_sale=credit_sale).delete()

    installments_count = credit_sale.installments_count
    amount_per_installment = credit_sale.total_amount / Decimal(installments_count)
    base_amount = amount_per_installment.quantize(Decimal('0.01'))

    installments = []
    for i in range(1, installments_count + 1):
        due_date = credit_sale.start_date + timedelta(days=30 * i)

        if i == installments_count:
            amount = credit_sale.total_amount - (base_amount * (installments_count - 1))
        else:
            amount = base_amount

        installment = Installment(
            credit_sale=credit_sale,
            number=i,
            due_date=due_date,
            amount=amount,
            status='PENDING'
        )
        installments.append(installment)

    Installment.objects.bulk_create(installments)
    return installments
