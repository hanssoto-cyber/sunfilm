# SUNFILM — Sitio web corporativo

Sitio web para **SUNFILM**, empresa de instalación de láminas para vidrios: polarizado automotriz, control solar, láminas de seguridad, decorativas, empavonados y anti grafiti.

El sitio permite al administrador gestionar servicios, galería de trabajos y artículos desde el panel de Django, y recibir solicitudes de cotización de clientes que quedan registradas en la base de datos.

---

## Tecnologías

| Componente | Versión / Detalle |
|---|---|
| Python | 3.14 |
| Django | 5.2 LTS |
| Base de datos | SQLite 3 (desarrollo) |
| Frontend | Bootstrap 5.3 (CDN) + Bootstrap Icons |
| Imágenes | Pillow |
| Patrón | MTV (Model-Template-View), una app por dominio |

---

## Funcionalidades

- **Catálogo de servicios** organizado por categorías (Automotriz, Arquitectónico, Seguridad) con filtro dinámico y página de detalle.
- **Galería de trabajos** con grilla filtrable, lightbox modal y paginación.
- **Blog / Tips** con categorías propias, buscador, estados borrador/publicado y publicación programada.
- **Solicitudes de cotización** con validación de datos, protección anti-spam por honeypot y gestión de estados tipo CRM desde el admin.
- **Panel de administración** personalizado con miniaturas, edición en línea y links directos a WhatsApp.
- **SEO**: URLs con slug, meta descriptions por página, texto alternativo en imágenes y etiquetas Open Graph en artículos.
- **Diseño responsive** con tema oscuro nativo de Bootstrap 5.

---

## Requisitos previos

- Python 3.14 o superior
- Git
- pip

---

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/hanssoto-cyber/sunfilm.git
cd sunfilm
```

### 2. Crear y activar el entorno virtual

**Windows (Git Bash):**
```bash
python -m venv venv
source venv/Scripts/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

El prompt debe mostrar `(venv)` al inicio.

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones

```bash
python manage.py migrate
```

### 5. Cargar datos iniciales

```bash
python manage.py loaddata servicios_iniciales
python manage.py loaddata blog_inicial
```

Esto carga 3 categorías, 8 servicios y 3 artículos de ejemplo.

### 6. Crear un superusuario

```bash
python manage.py createsuperuser
```

### 7. Levantar el servidor

```bash
python manage.py runserver
```

Abrir en el navegador: **http://127.0.0.1:8000/**

---

## Rutas del proyecto

### Sitio público

| Ruta | Nombre | Descripción |
|---|---|---|
| `/` | `core:home` | Portada: hero, categorías, servicios destacados, trabajos recientes |
| `/nosotros/` | `core:nosotros` | Información de la empresa |
| `/cotizar/` | `core:cotizar` | Formulario de solicitud de cotización |
| `/cotizar/?servicio=<id>` | `core:cotizar` | Formulario con servicio preseleccionado |
| `/servicios/` | `servicios:lista` | Catálogo completo de servicios |
| `/servicios/?categoria=<slug>` | `servicios:lista` | Catálogo filtrado por categoría |
| `/servicios/<slug>/` | `servicios:detalle` | Detalle del servicio con beneficios y CTA |
| `/galeria/` | `galeria:lista` | Galería de trabajos realizados |
| `/galeria/?categoria=<slug>` | `galeria:lista` | Galería filtrada por categoría |
| `/tips/` | `blog:lista` | Listado de artículos |
| `/tips/?categoria=<slug>` | `blog:lista` | Artículos filtrados por categoría |
| `/tips/?q=<término>` | `blog:lista` | Búsqueda de artículos |
| `/tips/<slug>/` | `blog:detalle` | Artículo completo |

### Administración

| Ruta | Descripción |
|---|---|
| `/admin/` | Panel de administración de Django |
| `/admin/servicios/categoria/` | Gestión de categorías de servicios |
| `/admin/servicios/servicio/` | Gestión de servicios |
| `/admin/galeria/trabajo/` | Gestión de la galería de trabajos |
| `/admin/blog/post/` | Gestión de artículos |
| `/admin/blog/categoriapost/` | Gestión de categorías del blog |
| `/admin/core/cotizacion/` | Solicitudes de cotización recibidas |

---

## Usuario de prueba

| Campo | Valor |
|---|---|
| Usuario | `admin` |
| Contraseña | `sunfilm2026` |
| URL | http://127.0.0.1:8000/admin/ |

> Estas credenciales son únicamente para evaluación en entorno local. En producción se utiliza un usuario distinto con contraseña segura.

---

## Estructura del proyecto

```
sunfilm/
├── config/                    # Configuración del proyecto
│   ├── settings.py            # Ajustes generales
│   ├── urls.py                # URLs raíz
│   └── wsgi.py
├── core/                      # Portada, nosotros y cotizaciones
│   ├── models.py              # Modelo Cotizacion
│   ├── forms.py               # CotizacionForm con honeypot
│   ├── views.py               # home, nosotros, cotizar
│   ├── urls.py
│   ├── admin.py
│   └── templates/core/
├── servicios/                 # Catálogo de servicios
│   ├── models.py              # Modelos Categoria y Servicio
│   ├── views.py               # lista, detalle
│   ├── urls.py
│   ├── admin.py
│   ├── fixtures/
│   └── templates/servicios/
├── galeria/                   # Galería de trabajos
│   ├── models.py              # Modelo Trabajo
│   ├── views.py               # lista con paginación
│   ├── urls.py
│   ├── admin.py
│   └── templates/galeria/
├── blog/                      # Consejos y tips
│   ├── models.py              # Modelos Post y CategoriaPost
│   ├── views.py               # lista con buscador, detalle
│   ├── urls.py
│   ├── admin.py
│   ├── fixtures/
│   └── templates/blog/
├── templates/                 # Plantillas globales
│   ├── base.html              # Plantilla base (herencia)
│   └── partials/
│       ├── navbar.html
│       ├── footer.html
│       └── whatsapp.html
├── static/                    # Archivos estáticos
│   ├── css/style.css
│   └── img/logo.png
├── media/                     # Archivos subidos (no versionado)
├── evidencia/                 # Capturas de pantalla
├── manage.py
├── requirements.txt
└── README.md
```

---

## Modelo de datos

| App | Modelo | Descripción |
|---|---|---|
| `servicios` | `Categoria` | Agrupa servicios (Automotriz, Arquitectónico, Seguridad) |
| `servicios` | `Servicio` | Servicio con descripción, beneficios, imagen y destacado |
| `galeria` | `Trabajo` | Foto de trabajo realizado, vinculada a un servicio |
| `blog` | `CategoriaPost` | Categorías de artículos |
| `blog` | `Post` | Artículo con estado borrador/publicado y CTA a un servicio |
| `core` | `Cotizacion` | Solicitud del cliente con seguimiento de estado |

**Relaciones:** `Servicio` → `Categoria` (PROTECT) · `Trabajo` → `Servicio` (SET_NULL) · `Post` → `CategoriaPost`, `Servicio` (SET_NULL) · `Cotizacion` → `Servicio` (SET_NULL)

---

## Panel de administración

El administrador del sitio puede, sin tocar código:

- Crear, editar y desactivar servicios; marcarlos como destacados para la portada.
- Subir fotos de trabajos con vista previa y organizarlas por servicio.
- Escribir artículos, guardarlos como borrador y programar su publicación.
- Revisar las cotizaciones recibidas, cambiar su estado (Nuevo → Contactado → Cotizado → Cerrado) y responder por WhatsApp con un clic desde el listado.

---

## Evidencias

Las capturas de pantalla se encuentran en la carpeta `evidencia/`:

| Archivo | Contenido |
|---|---|
| `01-home.png` | Portada del sitio |
| `02-servicios-lista.png` | Catálogo de servicios con filtros |
| `03-servicio-detalle.png` | Detalle de un servicio |
| `04-galeria.png` | Galería de trabajos |
| `05-galeria-modal.png` | Lightbox de la galería |
| `06-blog-lista.png` | Listado de artículos |
| `07-blog-detalle.png` | Artículo completo |
| `08-cotizar-form.png` | Formulario de cotización |
| `09-cotizar-exito.png` | Confirmación de envío |
| `10-admin-cotizaciones.png` | Cotizaciones recibidas en el admin |
| `11-admin-galeria.png` | Admin de galería con miniaturas |
| `12-responsive-movil.png` | Vista en dispositivo móvil |

---

## Notas de desarrollo

- Los archivos subidos (`media/`), el entorno virtual (`venv/`) y la base de datos local (`db.sqlite3`) no se versionan.
- Las fixtures incluyen contenido de ejemplo editable desde el admin.
- El formulario de cotización usa un campo honeypot oculto como filtro anti-spam, sin requerir CAPTCHA.
- La búsqueda del blog utiliza `icontains` sobre SQLite; para un volumen mayor de artículos se recomienda migrar a búsqueda full-text de PostgreSQL.

---

## Contacto de la empresa

- **Teléfono / WhatsApp:** +56 9 5097 8799
- **Facebook:** [SUNFILM](https://www.facebook.com/share/1Cjvu26wjS/)

---

## Autor

Desarrollado por **Hans Soto** — [github.com/hanssoto-cyber](https://github.com/hanssoto-cyber)