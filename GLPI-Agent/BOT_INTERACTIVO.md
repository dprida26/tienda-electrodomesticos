# GLPI Telegram Bot - Modo Interactivo

## 📱 Descripción

Bot de Telegram que responde a **comandos bajo demanda** en lugar de ejecutarse en horarios específicos.

El bot está siempre escuchando en Telegram y genera reportes cuando **tú lo solicitas**.

---

## 🎯 Características

✅ **Responde a comandos**: El bot reacciona cuando le escribes en Telegram  
✅ **Bajo demanda**: Solo genera reportes cuando lo solicitas  
✅ **Sin horarios fijos**: No necesitas configurar scheduler  
✅ **Múltiples comandos**: /reporte, /help, /status, /info  
✅ **Feedback inmediato**: "Procesando..." mientras obtiene los datos  
✅ **Manejo de errores**: Recuperación automática ante fallos  

---

## 🚀 Cómo Usar

### 1. Iniciar el Bot Interactivo

```bash
cd "C:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\GLPI-Agent"
python telegram_bot_interactive.py
```

**Salida esperada:**
```
╔══════════════════════════════════════╗
║   🤖 GLPI AGENT — Telegram Bot      ║
║     MODO INTERACTIVO                ║
╚══════════════════════════════════════╝

2026-05-12 10:50:00 │ INFO    │ 📡 Iniciando bot en modo interactivo...
2026-05-12 10:50:00 │ INFO    │ ⏳ Esperando comandos en Telegram...
2026-05-12 10:50:00 │ INFO    │ 💡 Usa /reporte, /help, /status o /info
```

### 2. Enviar Comandos en Telegram

Abre tu grupo **"Soporte GLPI AMSA"** y escribe uno de estos comandos:

#### **Obtener Reporte**
```
/reporte
```
o también puedes usar:
```
/report
/tickets
!reporte
```

**Respuesta del bot:**
```
⏳ Procesando solicitud...

Obteniendo tickets de GLPI...

[Después de ~15 segundos...]

📊 RESUMEN GLPI — 12/05/2026 10:50
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Tickets activos: 20

🟡 PRIORIDAD MEDIA (20 tickets)
──────────────────────────────
  📌 #8388 — Problemas en consumo pac...
  📌 #8403 — EVOLUCION DE ENFERMERIA...
  ... (más tickets)
```

#### **Ver Ayuda**
```
/help
```

**Respuesta:**
```
🤖 GLPI Agent Bot - Comandos Disponibles

/reporte - Obtener reporte de tickets
/report - (Alias de /reporte)
/tickets - (Alias de /reporte)
!reporte - (Alias de /reporte)

/help - Mostrar esta ayuda
/status - Estado del sistema
/info - Información del bot
```

#### **Ver Estado del Sistema**
```
/status
```

**Respuesta:**
```
✅ Sistema Operativo

GLPI API: ✓ Conectado
Telegram Bot: ✓ Activo
Filtros: ✓ Configurados
  • Email: @amsa.com.py
  • Mes: Mayo 2026
  • Categoría: Soporte Tecnico

Estado: 🟢 En línea
```

#### **Ver Información**
```
/info
```

---

## 💻 Instalación para Ejecución Continua

### Opción A: Como Servicio de Windows (Recomendado)

Crear un archivo `start_bot_interactive.bat`:

```batch
@echo off
REM Inicia el bot interactivo en la carpeta correcta

cd /d "C:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\GLPI-Agent"
python telegram_bot_interactive.py

REM Si el bot falla, esperar 10 segundos e intentar de nuevo
timeout /t 10
goto start
```

Luego crear una tarea programada en Windows:

1. Abre "Tareas Programadas"
2. Crea una tarea nueva
3. Asigna: `start_bot_interactive.bat`
4. Configura: Iniciar al encender la PC
5. Marca: "Ejecutar aunque el usuario no esté conectado"

### Opción B: Con nssm (Conversión a Servicio Windows)

```bash
# Descargar nssm: https://nssm.cc/download
# Luego:

nssm install GLPIBot "python" "telegram_bot_interactive.py"
nssm start GLPIBot
```

### Opción C: Ejecutar en tmux/screen (Linux/WSL)

```bash
tmux new-session -d -s glpi-bot "python telegram_bot_interactive.py"
```

---

## 📊 Arquitectura del Bot

```
┌─────────────────────────────────────┐
│  Usuario en Telegram                │
│  Escribe: /reporte                  │
└──────────────┬──────────────────────┘
               │
               ▼
        ┌──────────────────┐
        │ Telegram API     │
        │ getUpdates()     │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Bot Interactivo  │
        │ Lee comandos     │
        └────────┬─────────┘
                 │
          ┌──────┴──────┐
          │             │
    /reporte?      Otros comandos?
          │             │
          ▼             ▼
    ┌─────────────┐  ┌──────────────┐
    │ GLPI API    │  │ Enviar estado│
    │ Obtener     │  │ o ayuda      │
    │ tickets     │  └──────────────┘
    └──────┬──────┘
           │
           ▼
    ┌──────────────┐
    │ Generar      │
    │ Reporte      │
    └──────┬──────┘
           │
           ▼
    ┌──────────────┐
    │ Enviar a     │
    │ Telegram     │
    └──────────────┘
```

---

## 🔧 Configuración Requerida

El bot usa la misma configuración del `.env`:

```env
GLPI_URL=https://soporte.promed.com.py/apirest.php
APP_TOKEN=SNpRD2C82cAo8d7BTmKgcKSuuiWsnuRsAVNVVo6r
GLPI_USER=glpi
GLPI_PASSWORD=4s3YU4KNVgrJWyt
EMAIL_DOMAIN=@amsa.com.py
CATEGORY_NAME=Soporte Tecnico
TELEGRAM_BOT_TOKEN=8622104359:AAFgXgJPb83Fcet0Rk_fHOo-PnFX0d5GuU8
TELEGRAM_CHAT_ID=-5059022707
```

---

## 📋 Comandos Disponibles

| Comando | Alias | Función |
|---------|-------|---------|
| `/reporte` | `/report`, `/tickets`, `!reporte` | Obtener reporte de tickets |
| `/help` | `/ayuda`, `!help` | Mostrar ayuda |
| `/status` | `!status` | Estado del sistema |
| `/info` | `!info` | Información del bot |

---

## 🔍 Logs

Los logs se guardan en `logs/bot_interactive.log`:

```bash
# Ver últimas líneas
type logs\bot_interactive.log | tail -20

# Buscar errores
findstr "ERROR" logs\bot_interactive.log

# Ver línea específica
findstr "2026-05-12 10:50" logs\bot_interactive.log
```

---

## ⚙️ Cómo Funciona

### Polling (Long Polling)

El bot usa **Telegram getUpdates API** con timeout de 30 segundos:

1. Bot conecta a Telegram
2. Pregunta: "¿Hay mensajes nuevos?"
3. Si hay mensajes, procesa comandos
4. Si no hay, espera 1 segundo y vuelve a preguntar
5. Repite indefinidamente

**Ventajas:**
- ✅ No requiere webhook
- ✅ Funciona sin abrir puertos
- ✅ Simple de configurar
- ✅ Perfecto para máquinas locales

**Desventajas:**
- ⚠️ Ligeramente más lento que webhooks (30 seg max)
- ⚠️ Consume más ancho de banda

---

## 🛡️ Manejo de Errores

El bot se recupera automáticamente de:
- ✅ Desconexiones de GLPI
- ✅ Errores de Telegram API
- ✅ Timeouts de red
- ✅ Mensajes malformados

Después de 5 errores consecutivos, el bot se detiene para evitar loops infinitos.

---

## 📈 Rendimiento

- **Respuesta a comando**: ~15 segundos (tiempo de GLPI)
- **Consumo de memoria**: ~100 MB
- **Consumo de CPU**: Mínimo (esperando updates)
- **Consumo de red**: Mínimo (30 seg long polling)

---

## 🚀 Comparación: Scheduler vs Interactivo

| Aspecto | Scheduler | Interactivo |
|---------|-----------|------------|
| Horarios | Fijos (08:00, 17:00) | Bajo demanda |
| Reportes | Automáticos | Manual |
| Latencia | Máximo 1 hora | ~15 segundos |
| Uso de recursos | Bajo | Muy bajo |
| Flexibilidad | Media | Alta |
| Ideal para | Equipos grandes | Equipos dinámicos |

---

## 💡 Casos de Uso

### ✅ Usa Interactivo si:
- Necesitas reportes bajo demanda
- No sabes cuándo necesitarás información
- Quieres evitar reportes innecesarios
- Prefieres controlar cuándo obtener datos

### ✅ Usa Scheduler si:
- Necesitas reportes automáticos diarios
- El equipo necesita información rutinaria
- Quieres reducir carga manual

### 💪 Usa Ambos si:
- Necesitas reportes automáticos + acceso bajo demanda
- Ejecuta scheduler durante el día y bot interactivo 24/7

---

## 🆘 Troubleshooting

### "El bot no responde"
```bash
# Verificar que está ejecutándose
python telegram_bot_interactive.py

# Ver logs
type logs\bot_interactive.log | tail -50
```

### "Error: getUpdates failed"
```
❌ Verificar que TELEGRAM_BOT_TOKEN es correcto
✅ Solución: python main.py --test-tg
```

### "No se genera reporte"
```
❌ Verificar credenciales GLPI
✅ Solución: python main.py --test-glpi
```

---

## 📞 Ventajas del Modo Interactivo

1. **Control Total**: Tú decides cuándo obtener reportes
2. **Económico**: No consume recursos sin necesidad
3. **Flexible**: Cero configuración de horarios
4. **Intuitivo**: Comandos simples y fáciles de recordar
5. **Responsivo**: Respuesta inmediata a comandos

---

## Conclusión

El **Bot Interactivo** es perfecto para equipos que necesitan reportes **bajo demanda** sin depender de horarios fijos.

**Para empezar ahora mismo:**

```bash
python telegram_bot_interactive.py
```

¡Luego escribe `/reporte` en Telegram! 🚀
