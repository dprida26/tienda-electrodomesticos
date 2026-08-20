# 🔧 Habilitar el Bot para Recibir Mensajes del Grupo

## ⚠️ PROBLEMA ACTUAL
El bot está corriendo pero **no recibe mensajes del grupo** porque Telegram por defecto no permite que bots vean mensajes de grupo sin mencionar.

## ✅ SOLUCIÓN: Cambiar Configuración de Privacidad en BotFather

### Paso 1: Abre Telegram y busca **@BotFather**

### Paso 2: Envía `/mybots`
Aparecerá una lista de tus bots.

### Paso 3: Selecciona **GLPI Soporte Bot**
(El bot que creaste para este proyecto)

### Paso 4: Busca y toca **"Bot Settings"**

### Paso 5: Selecciona **"Group Privacy"**

### Paso 6: Toca **"Turn OFF"**
(Esto permite que el bot vea todos los mensajes del grupo, no solo los que lo mencionan)

### Paso 7: BotFather te mostrará:
```
Group Privacy is OFF.
Your bot will receive all messages in groups (not just those addressing the bot).
```

## ✅ LISTO
Ahora el bot debería recibir y responder a todos los mensajes del grupo.

---

## 🧪 PRUEBA RÁPIDA

1. Ve al grupo "Soporte GLPI AMSA"
2. Escribe: `hola`
3. El bot debería responder en segundos

---

## 📝 ALTERNATIVA: Si Prefieres Que Solo Responda a Comandos

Si NO quieres que el bot lea todos los mensajes (para ahorrar ancho de banda), puedes:
- Dejar "Group Privacy" **ON** (por defecto)
- Los usuarios escriben **comandos**: `/tickets`, `/ayuda`, `/resumen`
- O mencionan el bot: `@glpi_soporte_amsa_bot muéstrame los tickets`

---

## ❓ ¿Cuál Prefieres?

### OPCIÓN A: Grupo Privacy OFF
- ✅ Bot responde a todo
- ✅ Más interactivo
- ⚠️ Usa más recursos
- ⚠️ Responde a mensajes que no van dirigidos a él

### OPCIÓN B: Grupo Privacy ON (actual)
- ✅ Más eficiente
- ✅ Solo responde a comandos
- ❌ No responde a preguntas casuales
- ✅ Usuarios escriben: `/tickets` o `@bot_name pregunta`

**RECOMENDACIÓN:** OPCIÓN A (Group Privacy OFF) para mejor experiencia del usuario.

---

## 📞 Soporte
Si después de cambiar la privacidad el bot sigue sin responder:
1. Verifica los logs: `Get-Content logs\bot_24_7.log -Tail 30`
2. Reinicia el bot: `Stop-Process -Name python; python bot_24_7.py`
3. Espera 2-3 segundos y escribe en el grupo nuevamente
