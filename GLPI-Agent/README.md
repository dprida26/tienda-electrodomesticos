
# 🤖 GLPI Agent — Bot de Telegram

Agente que se conecta a GLPI dos veces al día y envía un resumen de tickets activos (filtrados por `@amsa.com.py`) a un grupo de Telegram, ordenados por prioridad y fecha.

## 📋 Requisitos Previos

- **Python 3.8+** instalado
- Acceso a la API REST de GLPI (`soporte.promed.com.py`)
- Un bot de Telegram (ver instrucciones abajo)

## 🚀 Instalación Rápida

```powershell
# 1. Ir a la carpeta del proyecto
cd "C:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\GLPI-Agent"

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar credenciales en .env (editar el archivo)
notepad .env
```

## 🔧 Configuración del .env

### GLPI
Edita el archivo `.env` con tus credenciales:
```env
GLPI_USER=tu_usuario_glpi
GLPI_PASSWORD=tu_contraseña_glpi
```

### Crear Bot de Telegram
1. Abre Telegram y busca **@BotFather**
2. Envía `/newbot`
3. Dale un nombre (ej: `GLPI Soporte Bot`)
4. Dale un username (ej: `glpi_soporte_amsa_bot`)
5. BotFather te dará un **token** — cópialo al `.env` en `TELEGRAM_BOT_TOKEN`

### Obtener Chat ID del Grupo
1. Agrega tu bot al grupo de Telegram
2. Envía cualquier mensaje en el grupo
3. Ejecuta:
```powershell
python main.py --discover
```
4. Copia el Chat ID que aparezca y pégalo en `.env` como `TELEGRAM_CHAT_ID`

## 📖 Modos de Uso

| Comando | Descripción |
|---------|-------------|
| `python main.py` | Inicia el scheduler (08:00 y 17:00) |
| `python main.py --now` | Ejecuta reporte ahora |
| `python main.py --discover` | Descubre Chat ID del grupo |
| `python main.py --test-glpi` | Prueba conexión a GLPI |
| `python main.py --test-tg` | Envía mensaje de prueba a Telegram |

## 🔄 Ejecutar como Servicio de Windows

```powershell
install_service.bat
```
Esto crea una tarea programada que inicia el agente automáticamente al encender la PC.

## 📊 Ejemplo de Reporte

```
📊 RESUMEN GLPI — 30/04/2026 08:00
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Tickets activos: 10

🔴 PRIORIDAD MUY ALTA (2 tickets)
──────────────────────────
  📌 #1234 — Servidor caído
       👤 Juan Pérez
       📅 29/04/2026 14:30
       🔧 En curso (Asignado)

🟠 PRIORIDAD ALTA (3 tickets)
...
```
