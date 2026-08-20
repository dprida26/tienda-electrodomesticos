# Plan para Mañana 📅

## ⏰ Orden de Tareas

### **MAÑANA - PARTE 1: Setup (30 min)**

```bash
# Terminal 1: Backend Django
cd "c:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\Tienda electrodomesticos"
docker-compose up

# Esperar a que diga: "Running on http://127.0.0.1:8000"

# Terminal 2: Frontend Next.js
cd "c:\Users\Administrador\Desktop\AMSA\Personal\Proyectos IA\tienda-web"
npm run dev

# Esperar a que diga: "Ready in XXs"
```

✅ Verificar en navegador:
- http://localhost:3000 (debe mostrar página con categorías)
- http://localhost:8000/admin/ (login con admin/admin123)
- http://localhost:8000/api/v1/categories/ (JSON con 8 categorías)

---

### **MAÑANA - PARTE 2: Agregar Productos de Prueba (30 min)**

1. Ir a: http://localhost:8000/admin/
2. Login: admin / admin123
3. Click en **"Productos"** → **"Agregar Producto"**

**Producto 1: Refrigerador**
```
Nombre: Refrigerador Samsung 500L
Categoría: Refrigerador
Marca: Samsung
Modelo: RS25R5011SR
Descripción: Refrigerador moderno con tecnología inverter
Precio: 1500000
Stock: 5
Stock Mínimo: 2
Activo: ✓
```

**Producto 2: Horno**
```
Nombre: Horno Electrolux 60L
Categoría: Horno
Marca: Electrolux
Modelo: OE8EL
Descripción: Horno eléctrico empotrable
Precio: 800000
Stock: 3
Stock Mínimo: 1
Activo: ✓
```

**Producto 3: Lavadora**
```
Nombre: Lavadora LG 10kg
Categoría: Lavadora
Marca: LG
Modelo: WF10WB6
Descripción: Lavadora automática frontal
Precio: 2000000
Stock: 2
Stock Mínimo: 1
Activo: ✓
```

Después de agregar, vuelve a: http://localhost:3000
Deberías ver los 3 productos en la página de inicio.

---

### **MAÑANA - PARTE 3: Panel Admin en Next.js (2-3 horas)**

**Crear estos archivos:**

1. **`tienda-web/app/admin/page.tsx`** - Dashboard admin
2. **`tienda-web/app/admin/categorias/page.tsx`** - Gestión categorías
3. **`tienda-web/app/admin/productos/page.tsx`** - Gestión productos
4. **`tienda-web/lib/admin-api.ts`** - Cliente API para POST/PUT/DELETE

**Funcionalidades:**

✅ **Panel Admin (http://localhost:3000/admin)**
- Tabla de categorías (nombre, orden, acciones)
- Botón "+ Nueva Categoría"
- Botón editar/eliminar para cada una

✅ **Panel Productos**
- Tabla de productos
- Botón "+ Nuevo Producto"
- Carga de imágenes

✅ **Formularios:**
- Modal/Form para agregar categoría
- Modal/Form para agregar producto
- Validaciones

---

## 📋 Checklist para Mañana

- [ ] Backend corriendo (`docker-compose up`)
- [ ] Frontend corriendo (`npm run dev`)
- [ ] Web pública visible (http://localhost:3000)
- [ ] Admin login funciona (http://localhost:8000/admin/)
- [ ] Agregados 3+ productos de prueba
- [ ] Productos visibles en web pública
- [ ] Panel admin en Next.js CREADO
  - [ ] Página de categorías
  - [ ] Crear categoría
  - [ ] Editar categoría
  - [ ] Eliminar categoría
  - [ ] Subir imágenes

---

## 🎯 Resultado Final Esperado

Cuando termines mañana, tendrás:

```
✅ Backend API funcional
✅ Web pública con productos
✅ Panel admin para gestionar:
   - Categorías
   - Productos
   - Imágenes
```

Todo en una sola aplicación Next.js.

---

## 💡 Tips para Mañana

1. **Si algo no carga:**
   - Revisar consola del navegador (F12 → Console)
   - Revisar terminal de Next.js
   - Si sigue fallando, revisar `DIAGNOSTICO.md`

2. **Si cambias código:**
   - Next.js recarga automático
   - Django también recarga
   - Solo reinicia si algo se "congela"

3. **Para agregar más productos rápido:**
   - Ir a http://localhost:8000/admin/inventory/product/
   - Click en "Agregar Producto"
   - Completa y guarda (repite)

4. **Commit frecuentemente:**
   ```bash
   cd tienda-web
   git add -A
   git commit -m "feat: descripción del cambio"
   ```

---

## 📞 Si Necesitas Ayuda

Revisa estos archivos en este orden:
1. `DIAGNOSTICO.md` - Problemas comunes
2. `INSTRUCCIONES_FASE2.md` - Guía completa
3. `API_DOCS.md` - Endpoints disponibles

---

**¡Que tengas un excelente día de trabajo mañana! 🚀**
