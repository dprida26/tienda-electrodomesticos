# 📑 Índice de Documentación

Bienvenido al **Agente de Notificaciones Diarias**. Este índice te guía por toda la documentación del proyecto.

## 🚀 Primeros Pasos

**¿Eres nuevo aquí?** Comienza por uno de estos:

1. **[⚡ QUICKSTART.md](QUICKSTART.md)** — Empieza en 5 minutos
   - Instalación rápida
   - Configuración mínima
   - Ejecuta tu primer reporte

2. **[📋 SETUP.md](SETUP.md)** — Guía detallada paso a paso
   - Instrucciones completas de instalación
   - Configuración de Google OAuth2
   - Configuración de LinkedIn API
   - Solución de problemas

3. **[📖 README.md](README.md)** — Documentación principal
   - Descripción del proyecto
   - Características
   - Variables de entorno
   - Troubleshooting

## 📚 Documentación Técnica

### Comprensión del Proyecto

- **[📁 PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** — Estructura completa
  - Árbol de directorios
  - Relación entre módulos
  - Flujo de ejecución
  - Dependencias

- **[🎓 PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** — Resumen técnico
  - Descripción general
  - Características principales
  - Stack tecnológico
  - Diagramas de flujo
  - Seguridad

### Uso y Extensión

- **[🔧 EXTENSION.md](EXTENSION.md)** — Cómo extender el proyecto
  - Agregar nuevos servicios
  - Integración con Slack
  - Envío de reportes por email
  - Web scraping LinkedIn
  - Testing
  - CI/CD

## 📂 Archivos Importantes

| Archivo | Propósito |
|---------|-----------|
| `package.json` | Dependencias y scripts del proyecto |
| `tsconfig.json` | Configuración de TypeScript |
| `.env.example` | Plantilla de variables de entorno |
| `Dockerfile` | Configuración para Docker |
| `docker-compose.yml` | Orquestación con Docker Compose |
| `.gitignore` | Archivos a ignorar en Git |

## 🔑 Configuración

### Variables de Entorno Requeridas

Crea un archivo `.env` con las siguientes variables:

```env
# Gmail OAuth2
GMAIL_CLIENT_ID=
GMAIL_CLIENT_SECRET=
GMAIL_REDIRECT_URI=http://localhost:3000/oauth/callback
GMAIL_USER_EMAIL=

# LinkedIn API
LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=
LINKEDIN_ACCESS_TOKEN=

# Configuración general
SCHEDULE_TIME=08:00
REPORT_OUTPUT_DIR=./reports
NODE_ENV=development
```

**Instrucciones detalladas**: Ver [SETUP.md](SETUP.md)

## 🔨 Comandos Principales

```bash
# Instalación
npm install

# Desarrollo (con reporte de prueba)
npm run dev

# Compilación
npm run build

# Ejecutar en producción
npm start

# Testing
npm run test

# Linting
npm run lint

# Formateo
npm run format
```

## 📊 Estructura de Carpetas

```
agente-notificaciones-diarias/
├── src/                    # Código fuente TypeScript
│   ├── agent/             # Lógica principal
│   ├── config/            # Configuración
│   ├── services/          # Servicios (Gmail, LinkedIn, Reports)
│   ├── scheduler/         # Tareas programadas
│   ├── types/             # Interfaces TypeScript
│   ├── utils/             # Utilidades
│   └── index.ts           # Punto de entrada
├── reports/               # PDFs generados
├── dist/                  # Código compilado (después de build)
└── [Archivos de config]   # .env, package.json, etc.
```

**Detalle completo**: Ver [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

## 🎯 Guía de Navegación por Caso de Uso

### "Quiero empezar ahora mismo"
1. [QUICKSTART.md](QUICKSTART.md) (5 minutos)

### "Necesito ayuda con la instalación"
1. [SETUP.md](SETUP.md)
2. Luego [QUICKSTART.md](QUICKSTART.md)

### "Quiero entender cómo funciona"
1. [README.md](README.md) — Características generales
2. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) — Detalles técnicos
3. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) — Estructura interna

### "Quiero extender/modificar el agente"
1. [README.md](README.md) — Visión general
2. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) — Cómo está organizado
3. [EXTENSION.md](EXTENSION.md) — Cómo agregar funcionalidades
4. Revisar el código en `src/`

### "Tengo un error, ¿cómo lo soluciono?"
1. [README.md](README.md) → Sección "Troubleshooting"
2. [SETUP.md](SETUP.md) → Sección "Solución de Problemas"
3. Revisar logs en la terminal

### "Quiero usar Docker"
1. Revisa [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) → Sección "Docker"
2. Usa `docker-compose up -d` (necesitas `.env` primero)

## 🌟 Características Principales

✅ **Gmail Integration**
- Lectura automática de correos
- OAuth2 authentication
- Filtrado por fecha

✅ **LinkedIn Integration**
- Captura de notificaciones
- Registro de actividad

✅ **Reportes PDF**
- Documento estructurado
- Dos secciones (Correos y LinkedIn)
- Generación automática

✅ **Automatización**
- Ejecución diaria
- Programación flexible
- Proceso siempre activo

## 🔐 Seguridad

- OAuth2 para Google (sin almacenar contraseñas)
- Tokens locales (no en repositorio)
- Validación de entrada con Zod
- Variables de entorno sensibles

Más detalles: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) → Sección "Seguridad"

## 📞 Preguntas Frecuentes

**P: ¿Cómo obtengo las credenciales de Google?**  
R: [SETUP.md](SETUP.md) → Paso 3

**P: ¿Cómo obtengo el token de LinkedIn?**  
R: [SETUP.md](SETUP.md) → Paso 4

**P: ¿Dónde se guardan los reportes?**  
R: En la carpeta `./reports/` (configurable)

**P: ¿Puedo cambiar la hora de ejecución?**  
R: Sí, cambia `SCHEDULE_TIME` en `.env`

**P: ¿Cómo envío reportes por email?**  
R: Ver [EXTENSION.md](EXTENSION.md) → "Enviar Reporte por Email"

**P: ¿Puedo integrar esto con Slack/Teams?**  
R: Sí, ver [EXTENSION.md](EXTENSION.md) → "Agregar Slack/Teams"

## 🚀 Próximas Mejoras

- [ ] Dashboard web interactivo
- [ ] Envío automático por email
- [ ] Integración con Slack/Teams
- [ ] Web scraping para LinkedIn
- [ ] Base de datos histórica
- [ ] API REST para generación manual
- [ ] Notificaciones push

Ver más en: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) → "Próximas Mejoras"

## 📈 Escalabilidad

El proyecto está diseñado para ser extensible:
- Arquitectura modular
- Servicios independientes
- Fácil agregar nuevas integraciones

Ejemplos: [EXTENSION.md](EXTENSION.md)

## 🐳 Deployment

### Local
```bash
npm install && npm run build && npm start
```

### Docker
```bash
docker-compose up -d
```

### Cloud (AWS, GCP, Azure)
Ver ejemplos en [EXTENSION.md](EXTENSION.md)

## 📝 Licencia

MIT - Libre para usar, modificar y distribuir

## 👤 Autor

Creado abril 2026  
Versión: 1.0.0

---

## 🗺️ Mapa de Lectura Recomendado

```
START → QUICKSTART.md (5 min)
   ↓
¿Funcionó? 
   ├─→ SÍ → Disfruta tu agente ✅
   └─→ NO → SETUP.md (troubleshooting)
         ↓
      ¿Arreglado?
         ├─→ SÍ → Disfruta tu agente ✅
         └─→ NO → README.md + PROJECT_SUMMARY.md
              ↓
           Explorar SOURCE CODE → src/
```

---

**Última actualización**: Abril 2026

¿Necesitas ayuda? Empieza por [QUICKSTART.md](QUICKSTART.md) o [SETUP.md](SETUP.md).
