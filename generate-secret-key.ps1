# Script para generar SECRET_KEY seguro para Django en Render

Write-Host "`n🔐 Generador de SECRET_KEY para Django`n" -ForegroundColor Cyan

Write-Host "Generando SECRET_KEY seguro..." -ForegroundColor Yellow

try {
    $secretKey = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ SECRET_KEY Generado Exitosamente:`n" -ForegroundColor Green
        Write-Host $secretKey -ForegroundColor Cyan

        Write-Host "`n📋 Pasos a seguir:`n" -ForegroundColor Yellow
        Write-Host "1. Copia el valor anterior (Ctrl+C o selecciona y copia)"
        Write-Host "2. Ve a https://dashboard.render.com"
        Write-Host "3. Abre tu Web Service"
        Write-Host "4. Sección 'Environment'"
        Write-Host "5. Busca 'SECRET_KEY' y pega el valor"
        Write-Host "6. Haz clic en 'Save Changes' y 'Manual Deploy'`n"

        # Copiar al portapapeles si es posible
        try {
            $secretKey | Set-Clipboard
            Write-Host "✨ El SECRET_KEY ha sido copiado al portapapeles automáticamente!`n" -ForegroundColor Green
        } catch {
            Write-Host "(No se pudo copiar automáticamente, cópialo manualmente)" -ForegroundColor Gray
        }
    }
    else {
        Write-Host "`n❌ Error al generar SECRET_KEY" -ForegroundColor Red
        Write-Host "Asegúrate de que Python y Django están instalados" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "`n❌ Error: $_" -ForegroundColor Red
    Write-Host "`nAsegúrate de ejecutar este script desde la carpeta del proyecto" -ForegroundColor Yellow
}

Write-Host ""
