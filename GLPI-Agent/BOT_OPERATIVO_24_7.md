# 🤖 GLPI Bot 24/7 - ¡Operativo!

## ✅ Estado: ACTIVO EN TELEGRAM

El bot está **corriendo 24/7** y responde a consultas de tickets en Telegram.

---

## 📱 Cómo Usar el Bot en Telegram

Abre Telegram y busca el bot: **@glpi_soporte_amsa_bot**

### Comandos Disponibles

#### `/start`
Muestra el menú de ayuda y opciones disponibles.

```
/start
→ Muestra: Comandos disponibles y guía de uso
```

#### `/tickets`
Ver todos los tickets **activos** de @amsa.com.py del mes actual.

```
/tickets
→ Retorna: Lista completa de 21 tickets (en este momento)
   • Con: ID, Título, Solicitante, Fecha, Estado, Prioridad
```

#### `/resumen`
Ver estadísticas resumidas de tickets por prioridad.

```
/resumen
→ Retorna: Conteo de tickets por nivel de prioridad
   • MUY ALTA: X tickets
   • ALTA: X tickets
   • MEDIA: X tickets
   • BAJA: X tickets
```

#### `/ayuda`
Muestra esta lista de comandos.

```
/ayuda
→ Muestra: Menú de ayuda con comandos disponibles
```

---

## 💬 Preguntas Naturales (Sin Comandos)

El bot entiende palabras clave y responde automáticamente:

### Palabras que disparan `/tickets` automáticamente:
- "muéstrame los **tickets**"
- "qué **soporte** tengo"
- "hay algún **problema**"
- "dame **error**" 
- "info de **GLPI**"

### Palabras que disparan `/ayuda` automáticamente:
- "¿qué puedes hacer?"
- "ayuda"
- "help"
- "cómo funciona"

**Ejemplo:**
```
Tú: "Muéstrame los tickets pendientes"
Bot: [Envía lista de 21 tickets activos]
```

---

## ⚙️ Configuración del Servicio

### Bot Token
```
8622104359:AAFgXgJPb83Fcet0Rk_fHOo-PnFX0d5GuU8
```

### Grupo de Telegram
```
Chat ID: -5059022707 (Soporte GLPI AMSA)
```

### Conexión GLPI
```
URL: https://soporte.promed.com.py/apirest.php
Usuario: glpi
Dominio filtrado: @amsa.com.py
Categoría: Soporte Tecnico
```

---

## 🔧 Gestionar el Servicio

### Ver que el bot está corriendo
```powershell
Get-Process python | Where-Object { $_.CommandLine -like "*bot_24_7.py*" }
```

### Ver logs en tiempo real
```powershell
Get-Content "C:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\GLPI-Agent\logs\bot_24_7.log" -Wait -Tail 20
```

### Detener el bot
```powershell
Stop-Process -Name python -Force
# O específicamente:
Get-Process python | Where-Object { $_.CommandLine -like "*bot_24_7.py*" } | Stop-Process
```

### Reiniciar el bot
```powershell
# 1. Detener
Get-Process python | Where-Object { $_.CommandLine -like "*bot_24_7.py*" } | Stop-Process
# 2. Esperar 2 segundos
Start-Sleep -Seconds 2
# 3. Iniciar
cd "C:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\GLPI-Agent"
Start-Process python -ArgumentList "bot_24_7.py" -NoNewWindow
```

---

## 📊 Monitoreo Automático

### Ejecución al Iniciar PC
El bot se ejecuta **automáticamente** al iniciar Windows gracias a la tarea programada **GLPIBot24-7**.

Para ver/modificar:
1. Abre **Programador de Tareas** (`taskschd.msc`)
2. Busca: `GLPIBot24-7`
3. Click derecho → Propiedades

### Auto-Reinicio si Falla
El bot incluye un script de reinicio automático que:
- ✅ Detecta si el bot falla
- ✅ Intenta reiniciar hasta 5 veces
- ✅ Registra todos los intentos en `logs\bot_restart.log`
- ✅ Espera 5 segundos entre reintentos

---

## 📝 Archivos Importantes

```
C:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\GLPI-Agent\
├── bot_24_7.py                    ← Bot principal
├── run_bot_with_restart.ps1       ← Script de reinicio automático
├── install_bot_service_clean.ps1  ← Instalador de servicio
├── requirements.txt               ← Dependencias (python-telegram-bot)
├── .env                           ← Credenciales (no compartir)
└── logs/
    ├── bot_24_7.log              ← Logs del bot
    └── bot_restart.log           ← Logs de reinicio
```

---

## 🚀 Ejecución Manual

### En PowerShell (como Admin)
```powershell
cd "C:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\GLPI-Agent"

# Opción 1: Con reinicio automático
powershell -ExecutionPolicy Bypass -File run_bot_with_restart.ps1

# Opción 2: Bot directo (sin auto-reinicio)
python bot_24_7.py
```

### En CMD
```cmd
cd "C:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\GLPI-Agent"
python bot_24_7.py
```

---

## 🔍 Troubleshooting

### El bot no responde
1. Verifica que esté en marcha: `Get-Process python`
2. Revisa logs: `Get-Content logs\bot_24_7.log -Tail 30`
3. Reinicia: `Stop-Process -Name python; Start-Sleep 2; Start-Process python -ArgumentList "bot_24_7.py"`

### Error de token de Telegram
- Verifica que el token en `.env` sea correcto
- Prueba la conexión: `python test_bot_interactive.py`

### Error de conexión a GLPI
- Verifica credenciales en `.env`
- Comprueba que `https://soporte.promed.com.py` sea accesible
- Prueba con: `python main.py --test-glpi`

---

## 📞 Contacto y Soporte

Para reportar problemas o sugerencias:
1. Revisa los logs en `logs/bot_24_7.log`
2. Verifica que todas las credenciales estén correctas en `.env`
3. Ejecuta el test: `python test_bot_interactive.py`

---

## 🎯 Casos de Uso

### Caso 1: Ver tickets pendientes durante la mañana
```
Usuario: "Oye bot, dame los tickets pendientes"
Bot: [Envía 21 tickets de @amsa.com.py del mes actual]
```

### Caso 2: Verificar si hay emergencias
```
Usuario: "hay algún problema urgente"
Bot: [Busca automáticamente por palabra "problema" → envía /tickets]
```

### Caso 3: Estadísticas rápidas
```
Usuario: /resumen
Bot: [Muestra: 21 tickets totales: 0 MUY ALTA, 5 ALTA, 16 MEDIA, 0 BAJA]
```

---

**Versión:** 1.0  
**Último Update:** 2026-05-18 16:30  
**Estado:** ✅ Operativo 24/7
