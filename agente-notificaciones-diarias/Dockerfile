FROM node:20-alpine

WORKDIR /app

# Copiar package files
COPY package*.json ./

# Instalar dependencias
RUN npm ci

# Copiar código fuente
COPY src ./src
COPY tsconfig.json ./

# Compilar TypeScript
RUN npm run build

# Crear directorio de reportes
RUN mkdir -p reports

# Exponer puerto (opcional si agregas API)
EXPOSE 3000

# Ejecutar la aplicación
CMD ["npm", "start"]
