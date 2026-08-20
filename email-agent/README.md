# Email Agent - Informe Diario de Correo (Gmail)

Agente que se conecta a tu cuenta personal de Gmail, lee los correos del día y genera un informe PDF en la carpeta `Informes de Correo` del escritorio.

---

## Requisitos previos

- **Node.js** 18+
- Cuenta personal de **Gmail**

---

## Paso 1: Crear proyecto en Google Cloud Console

1. Ir a [console.cloud.google.com](https://console.cloud.google.com)
2. Clic en el selector de proyectos (arriba) → **"New Project"**
   - Nombre: `Email Agent`
   - Clic en **Create**
3. Seleccionar el proyecto recién creado

### Habilitar Gmail API

1. Ir a **APIs & Services** → **Library**
2. Buscar **"Gmail API"**
3. Clic en **Enable**

### Configurar pantalla de consentimiento

1. Ir a **APIs & Services** → **OAuth consent screen**
2. Seleccionar **External** → **Create**
3. Completar:
   - App name: `Email Agent`
   - User support email: tu email
   - Developer contact: tu email
4. Clic en **Save and Continue**
5. En **Scopes**: clic en **Add or Remove Scopes**
   - Buscar y marcar: `https://www.googleapis.com/auth/gmail.readonly`
   - Clic en **Update** → **Save and Continue**
6. En **Test users**: clic en **Add Users**
   - Agregar tu email de Gmail
   - Clic en **Save and Continue**

### Crear credenciales OAuth 2.0

1. Ir a **APIs & Services** → **Credentials**
2. Clic en **Create Credentials** → **OAuth client ID**
3. Configurar:
   - Application type: **Web application**
   - Name: `Email Agent`
   - Authorized redirect URIs: agregar `http://localhost:3456/callback`
4. Clic en **Create**
5. Copiar **Client ID** y **Client Secret**

---

## Paso 2: Instalar y configurar

```bash
cd email-agent
npm install
```

Editar el archivo `.env` con tus credenciales:

```env
GOOGLE_CLIENT_ID=123456789-xxxxxxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxxxxxxx
GOOGLE_REFRESH_TOKEN=
OUTPUT_DIR=C:\Users\Administrador\Desktop\Informes de Correo
```

---

## Paso 3: Autenticarse con Gmail

```bash
npm run auth
```

Esto va a:
1. Abrir tu navegador para iniciar sesión con Google
2. Pedirte autorización de lectura de correo
3. Mostrarte un `GOOGLE_REFRESH_TOKEN` en la terminal

**Copiá ese token y pegálo en tu `.env`.**

---

## Paso 4: Generar informe

```bash
npm run dev
```

El PDF se guardará en `C:\Users\Administrador\Desktop\Informes de Correo\Informe_Correo_YYYY-MM-DD.pdf`

---

## Paso 5: Programar ejecución diaria

### Opción A: Programador de tareas de Windows (manual)

1. Primero compilar: `npm run build`
2. Abrir **Programador de tareas** (Task Scheduler)
3. **Crear tarea básica**:
   - Nombre: `Email Agent - Informe Diario`
   - Desencadenador: **Diariamente** a la hora deseada (ej: 18:00)
   - Acción: **Iniciar un programa**
     - Programa: `node`
     - Argumentos: `dist/index.js`
     - Iniciar en: `C:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\email-agent`

### Opción B: Comando PowerShell (rápido)

Abrir PowerShell como administrador:

```powershell
$action = New-ScheduledTaskAction `
  -Execute "node" `
  -Argument "dist/index.js" `
  -WorkingDirectory "C:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\email-agent"

$trigger = New-ScheduledTaskTrigger -Daily -At 6:00PM

Register-ScheduledTask `
  -TaskName "EmailAgent-InformeDiario" `
  -Action $action `
  -Trigger $trigger `
  -Description "Genera informe PDF diario de correos de Gmail" `
  -RunLevel Highest
```

---

## Estructura del proyecto

```
email-agent/
├── src/
│   ├── index.ts           # Punto de entrada principal
│   ├── config.ts          # Configuración y variables de entorno
│   ├── email.ts           # Conexión a Gmail API
│   ├── pdf-generator.ts   # Generador de informes PDF
│   └── auth-setup.ts      # Script de autenticación OAuth 2.0
├── .env                   # Variables de entorno (NO compartir)
├── .env.example           # Plantilla de variables
├── .gitignore
├── package.json
├── tsconfig.json
└── README.md
```
