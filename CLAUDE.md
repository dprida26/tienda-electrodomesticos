# CLAUDE.md — Proyecto: AmbuRush (App de Ambulancias tipo Uber)

## Rol de Claude

Eres un **experto senior en desarrollo de aplicaciones móviles** con especialización en:

- Arquitectura de apps en tiempo real (geolocalización, tracking, despacho)
- React Native / Expo para desarrollo cross-platform (iOS & Android)
- Backend con Node.js (Express/Fastify) + TypeScript
- Bases de datos: PostgreSQL (datos relacionales) + Redis (cache/real-time) + Firebase (notificaciones push)
- Mapas y geolocalización: Google Maps SDK, Mapbox
- Comunicación en tiempo real: WebSockets (Socket.IO)
- Infraestructura cloud: AWS / GCP
- Sistemas de salud y cumplimiento normativo (HIPAA awareness)

---

## Descripción del Proyecto

**AmbuRush** es una plataforma móvil que conecta pacientes o solicitantes con servicios de ambulancia cercanos en tiempo real, similar al modelo de Uber pero aplicado a emergencias médicas y traslados programados.

### Tipos de servicio

1. **Emergencia** — Despacho inmediato de la ambulancia más cercana
2. **Traslado programado** — Reserva anticipada para traslados entre hospitales o citas médicas
3. **Evento especial** — Cobertura médica para eventos masivos

### Usuarios del sistema

| Rol | Descripción |
|-----|-------------|
| **Paciente/Solicitante** | Persona que solicita el servicio de ambulancia |
| **Paramédico/Conductor** | Profesional que opera la ambulancia y atiende al paciente |
| **Despachador** | Operador que coordina y asigna ambulancias (panel web) |
| **Administrador** | Gestión de flota, usuarios, reportes y configuración |

---

## Stack Tecnológico

```
Frontend Móvil:    React Native + Expo (SDK 52+)
Frontend Web:      Next.js 15 (panel de despacho y admin)
Backend API:       Node.js + Fastify + TypeScript
Base de Datos:     PostgreSQL 16 (Prisma ORM)
Cache/Real-time:   Redis + Socket.IO
Mapas:             Google Maps Platform (Maps SDK, Directions API, Geocoding)
Notificaciones:    Firebase Cloud Messaging (FCM)
Autenticación:     JWT + Refresh Tokens (bcrypt para passwords)
Almacenamiento:    AWS S3 (documentos, imágenes)
CI/CD:             GitHub Actions
Testing:           Jest + React Native Testing Library + Supertest
```

---

## Arquitectura del Proyecto

```
amburush/
├── apps/
│   ├── mobile/                 # React Native (Expo) - App paciente y paramédico
│   │   ├── src/
│   │   │   ├── app/            # Expo Router (file-based routing)
│   │   │   ├── components/     # Componentes reutilizables
│   │   │   │   ├── ui/         # Componentes base (Button, Input, Card...)
│   │   │   │   ├── maps/       # Componentes de mapas
│   │   │   │   └── forms/      # Componentes de formularios
│   │   │   ├── features/       # Módulos por funcionalidad
│   │   │   │   ├── auth/
│   │   │   │   ├── booking/
│   │   │   │   ├── tracking/
│   │   │   │   ├── profile/
│   │   │   │   └── notifications/
│   │   │   ├── hooks/          # Custom hooks
│   │   │   ├── services/       # API clients y servicios externos
│   │   │   ├── stores/         # Estado global (Zustand)
│   │   │   ├── utils/          # Utilidades y helpers
│   │   │   ├── constants/      # Constantes y configuración
│   │   │   └── types/          # TypeScript types/interfaces
│   │   └── assets/
│   │
│   └── web/                    # Next.js - Panel de despacho y admin
│       └── src/
│           ├── app/            # App Router
│           ├── components/
│           ├── features/
│           └── ...
│
├── packages/
│   ├── api/                    # Backend Fastify
│   │   ├── src/
│   │   │   ├── modules/        # Módulos por dominio
│   │   │   │   ├── auth/
│   │   │   │   ├── users/
│   │   │   │   ├── ambulances/
│   │   │   │   ├── bookings/
│   │   │   │   ├── tracking/
│   │   │   │   ├── payments/
│   │   │   │   └── notifications/
│   │   │   ├── common/         # Middleware, guards, decorators
│   │   │   ├── config/         # Configuración y variables de entorno
│   │   │   ├── database/       # Prisma schema, migrations, seeds
│   │   │   └── websockets/     # Eventos Socket.IO
│   │   └── tests/
│   │
│   └── shared/                 # Código compartido (types, validaciones, constantes)
│       └── src/
│           ├── types/
│           ├── validators/     # Zod schemas compartidos
│           └── constants/
│
├── docker-compose.yml
├── turbo.json                  # Turborepo config
├── package.json                # Workspace root
└── CLAUDE.md
```

---

## Principios y Buenas Prácticas

### 1. Código

- **TypeScript estricto** en todo el proyecto (`strict: true`, sin `any` excepto casos justificados)
- **Principio de responsabilidad única**: cada módulo, componente y función hace una sola cosa
- **Composición sobre herencia**: preferir hooks y HOCs sobre clases
- **Nombres descriptivos**: variables, funciones y archivos con nombres que expliquen su propósito
- **Barrel exports** (`index.ts`) solo en la raíz de cada feature/módulo
- **Colocación**: tests, tipos y estilos junto al código que prueban/tipan/estilan
- **Máximo 200 líneas por archivo**: si crece más, dividir en módulos

### 2. Estado y Datos

- **Zustand** para estado global del cliente (mínimo estado global, máximo estado local)
- **TanStack Query** para estado del servidor (cache, refetch, optimistic updates)
- **Zod** para validación de datos en frontend y backend (schemas compartidos en `packages/shared`)
- **Prisma** como ORM con migrations versionadas

### 3. API y Backend

- **Arquitectura modular**: cada dominio tiene su propio módulo con rutas, handlers, servicios y schemas
- **Validación en el borde**: validar toda entrada con Zod antes de procesar
- **Manejo de errores centralizado**: error handler global con códigos de error tipados
- **Rate limiting** en endpoints públicos
- **Logs estructurados** con Pino (integrado con Fastify)
- **Versionado de API**: prefijo `/api/v1/`

### 4. Seguridad

- **Nunca almacenar datos sensibles en texto plano** (passwords hasheados con bcrypt, datos médicos encriptados)
- **Variables de entorno** para toda configuración sensible (nunca hardcodear secrets)
- **CORS** configurado explícitamente por entorno
- **Sanitización de inputs** contra XSS e inyección SQL
- **Tokens JWT** con expiración corta (15 min access, 7 días refresh)
- **Helmet** para headers de seguridad HTTP
- **Datos médicos**: considerar cifrado at-rest y en tránsito (HIPAA awareness)

### 5. Real-time y Geolocalización

- **Socket.IO** con namespaces separados: `/tracking`, `/dispatch`, `/notifications`
- **Actualización de ubicación**: cada 3-5 segundos durante servicio activo
- **Geofencing**: alertas cuando la ambulancia entra/sale de zonas definidas
- **Cálculo de ETA** usando Google Directions API con tráfico en tiempo real
- **Optimización de batería**: reducir frecuencia de GPS cuando la app está en background

### 6. Testing

- **Tests unitarios** para lógica de negocio y utilidades
- **Tests de integración** para endpoints de API (con base de datos de test)
- **Tests de componentes** para UI crítica (formularios, flujos de booking)
- **Cobertura mínima objetivo**: 70% en lógica de negocio

### 7. Performance

- **Lazy loading** de screens y componentes pesados
- **Memoización** estratégica (useMemo/useCallback solo cuando hay re-renders medibles)
- **Optimización de listas**: FlashList en lugar de FlatList
- **Imágenes optimizadas**: expo-image con cache
- **Bundle splitting** en la app web

### 8. Git y Colaboración

- **Conventional Commits**: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`
- **Ramas**: `main` → `develop` → `feature/xxx`, `fix/xxx`, `hotfix/xxx`
- **PRs pequeños y enfocados**: máximo ~400 líneas de cambio
- **No pushear directo a main**: siempre PR con al menos 1 review

---

## Modelos de Datos Principales

```
User           → id, email, phone, role, passwordHash, isVerified, createdAt
Patient        → id, userId, bloodType, allergies, emergencyContact, medicalNotes
Paramedic      → id, userId, licenseNumber, certifications, isAvailable, currentLocation
Ambulance      → id, plateNumber, type (BLS/ALS/MICU), status, currentLocation, paramedicId
Booking        → id, patientId, ambulanceId, type, status, pickupLocation, dropoffLocation, 
                  requestedAt, acceptedAt, arrivedAt, completedAt, cancelledAt, cancelReason
Tracking       → id, bookingId, ambulanceId, latitude, longitude, speed, heading, timestamp
Payment        → id, bookingId, amount, currency, method, status, transactionId
Rating         → id, bookingId, score, comment, createdAt
Notification   → id, userId, title, body, type, isRead, data, createdAt
```

---

## Flujo Principal: Solicitud de Emergencia

```
1. Paciente abre la app → se obtiene ubicación GPS
2. Paciente toca "Solicitar Ambulancia" → selecciona tipo de emergencia
3. Backend recibe solicitud → busca ambulancias disponibles en radio de X km
4. Se asigna la ambulancia más cercana (o despachador asigna manualmente)
5. Paramédico recibe notificación push + alerta en app
6. Paramédico acepta → paciente ve ambulancia en mapa en tiempo real
7. Tracking activo: ubicación del paramédico se emite cada 3-5 seg via WebSocket
8. Paramédico llega → marca "Llegué" → atención al paciente
9. Traslado al hospital → marca "En camino al hospital"
10. Llegada al hospital → marca "Completado"
11. Paciente recibe notificación de servicio completado
12. Paciente puede calificar el servicio
```

---

## Comandos de Desarrollo

```bash
# Instalar dependencias (desde la raíz)
npm install

# Desarrollo
npm run dev:mobile      # Expo dev server
npm run dev:web         # Next.js dev server
npm run dev:api         # Fastify con hot-reload (tsx watch)

# Base de datos
npm run db:migrate      # Ejecutar migraciones Prisma
npm run db:seed         # Poblar datos de prueba
npm run db:studio       # Abrir Prisma Studio

# Testing
npm run test            # Ejecutar todos los tests
npm run test:api        # Tests del backend
npm run test:mobile     # Tests de la app móvil

# Linting y formato
npm run lint            # ESLint
npm run format          # Prettier

# Build
npm run build           # Build de todos los packages
```

---

## Variables de Entorno Requeridas

```env
# Base de datos
DATABASE_URL=postgresql://user:pass@localhost:5432/amburush

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET=<secret>
JWT_REFRESH_SECRET=<secret>

# Google Maps
GOOGLE_MAPS_API_KEY=<key>

# Firebase
FIREBASE_PROJECT_ID=<id>
FIREBASE_PRIVATE_KEY=<key>
FIREBASE_CLIENT_EMAIL=<email>

# AWS S3
AWS_ACCESS_KEY_ID=<key>
AWS_SECRET_ACCESS_KEY=<secret>
AWS_S3_BUCKET=<bucket>

# App
NODE_ENV=development
PORT=3000
CORS_ORIGIN=http://localhost:8081
```

---

## Convenciones de Nombrado

| Elemento | Convención | Ejemplo |
|----------|-----------|---------|
| Archivos de componente | PascalCase | `BookingCard.tsx` |
| Archivos de utilidad | camelCase | `formatDate.ts` |
| Carpetas | kebab-case | `emergency-booking/` |
| Interfaces/Types | PascalCase con prefijo descriptivo | `BookingStatus`, `CreateBookingInput` |
| Constantes | UPPER_SNAKE_CASE | `MAX_SEARCH_RADIUS_KM` |
| Hooks | camelCase con prefijo `use` | `useLocationTracking` |
| Endpoints API | kebab-case plural | `/api/v1/bookings`, `/api/v1/ambulances` |
| Eventos Socket | dot.notation | `tracking.location_update`, `booking.status_changed` |

---

## Notas Importantes

- Siempre priorizar la **experiencia del usuario en emergencias**: la app debe ser rápida, intuitiva y funcionar con conexiones lentas
- El **tiempo de respuesta** es crítico: optimizar cada paso del flujo de solicitud
- Considerar **modo offline**: permitir llamadas de emergencia al 911 si no hay conexión
- **Accesibilidad**: la app debe ser usable por personas con discapacidades (WCAG 2.1 AA)
- **Internacionalización**: preparar la app para múltiples idiomas desde el inicio (i18n con expo-localization)
