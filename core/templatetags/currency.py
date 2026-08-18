from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def guarani(value):
    """Formatea un número como moneda Guaraní con separadores de miles"""
    if value is None:
        return 'Gs. 0'

    try:
        # Convertir a Decimal si es necesario
        if isinstance(value, str):
            value = Decimal(value)
        else:
            value = Decimal(str(value))

        # Formatear con 2 decimales
        formatted = f"{value:,.2f}"

        # Reemplazar separadores (formato Paraguay: punto para miles, coma para decimales)
        # Django por defecto usa: 1,234.56 (inglés)
        # Paraguay usa: 1.234,56
        parts = formatted.split('.')
        if len(parts) == 3:  # Tiene miles y decimales
            thousands = parts[0] + '.' + parts[1]
            decimals = parts[2]
            return f"Gs. {thousands},{decimals}"
        elif len(parts) == 2:  # Solo decimales
            return f"Gs. {parts[0]},{parts[1]}"
        else:
            return f"Gs. {formatted}"
    except:
        return f"Gs. {value}"
