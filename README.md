# SUNFILM — Sitio web corporativo en producción

Aplicación web desarrollada con **Django** para un negocio real del rubro de **láminas para vidrios arquitectónicos** (control solar, seguridad, empavonados de privacidad, anti-graffiti y rotulación en vinilo). El sitio está **desplegado en producción** sobre un VPS con Nginx, Gunicorn, PostgreSQL y Cloudflare, e incluye un panel de administración que permite gestionar todo el contenido y las solicitudes de cotización sin tocar código.

Este repositorio documenta tanto el **desarrollo de la aplicación** como el **despliegue y aseguramiento (hardening)** de la infraestructura, con foco en buenas prácticas de seguridad.

> **Nota de privacidad:** los datos operativos del entorno de producción (dominio, IP, rutas de administración, valores de configuración) se gestionan mediante variables de entorno y no se incluyen en este repositorio.

---

## Tabla de contenidos

- [Stack tecnológico](#stack-tecnológico)
- [Arquitectura de despliegue](#arquitectura-de-despliegue)
- [Funcionalidades](#funcionalidades)
- [Seguridad implementada](#seguridad-implementada)
- [Optimización y rendimiento](#optimización-y-rendimiento)
- [SEO técnico](#seo-técnico)
- [Instalación local](#instalación-local)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Modelo de datos](#modelo-de-datos)
- [Autor](#autor)

---

## Stack tecnológico

**Backend**
- Python 3.12+ · Django 5.2 LTS
- PostgreSQL 16 (producción) · SQLite (desarrollo)
- Gunicorn (servidor WSGI)

**Frontend**
- Bootstrap 5.3 + Bootstrap Icons
- AOS (Animate On Scroll)
- Tema oscuro nativo, diseño responsive

**Infraestructura**
- Nginx (reverse proxy)
- Cloudflare (proxy, WAF, HTTPS)
- VPS Ubuntu 24.04 LTS
- systemd (gestión del servicio)

**Librerías clave**
- `Pillow` — procesamiento y optimización de imágenes
- `django-axes` + `django-ipware` — protección contra fuerza bruta
- `python-dotenv` — gestión de configuración por entorno
- `psycopg2-binary` — conector PostgreSQL

---

## Arquitectura de despliegue

```
                    Internet
                       │
                       ▼
              ┌─────────────────┐
              │   Cloudflare    │  proxy · WAF · HTTPS (edge)
              └─────────────────┘
                       │  HTTPS (certificado de origen)
                       ▼
              ┌─────────────────┐
              │      Nginx      │  reverse proxy · archivos estáticos
              └─────────────────┘
                       │  socket Unix
                       ▼
              ┌─────────────────┐
              │    Gunicorn     │  servidor WSGI (systemd)
              └─────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │     Django      │  aplicación
              └─────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   PostgreSQL    │  base de datos
              └─────────────────┘
```

El tráfico entra por Cloudflare (que actúa como CDN, WAF y termina TLS en el borde), viaja cifrado hasta Nginx mediante un certificado de origen, y este redirige a la aplicación Django servida por Gunicorn. El firewall del servidor solo acepta tráfico web proveniente de los rangos de Cloudflare.

---

## Funcionalidades

- **Catálogo de servicios** organizado por categorías, con filtro dinámico y página de detalle con beneficios y llamado a la acción.
- **Galería de trabajos** con grilla filtrable, lightbox modal y carga diferida de imágenes.
- **Blog / Tips** con categorías propias, buscador, estados borrador/publicado y publicación programada.
- **Solicitudes de cotización** con validación, protección anti-spam mediante campo *honeypot* y gestión de estados tipo CRM (Nuevo → Contactado → Cotizado → Cerrado) desde el admin.
- **Panel de administración** personalizado con miniaturas, edición en línea y acceso directo a WhatsApp por cotización.
- **Diseño responsive** con animaciones sutiles al hacer scroll.

---

## Seguridad implementada

El proyecto aplica defensa en capas, tanto a nivel de aplicación como de infraestructura:

### Infraestructura
- **Acceso SSH endurecido:** autenticación exclusiva por clave (ed25519), acceso de root deshabilitado.
- **Firewall restrictivo (deny by default):** solo se exponen los puertos estrictamente necesarios; el tráfico web se acepta únicamente desde los rangos de red del proxy (Cloudflare), evitando accesos directos al origen.
- **Protección perimetral con Cloudflare:** WAF, mitigación de bots y terminación TLS en el borde.
- **HTTPS de extremo a extremo:** certificado de origen entre el proxy y el servidor (modo *Full strict*).
- **Bloqueo automatizado de IPs:** `fail2ban` sobre los servicios expuestos.

### Aplicación
- **Gestión de secretos por entorno:** `SECRET_KEY`, credenciales de base de datos y demás configuración sensible se leen de variables de entorno; el repositorio no contiene credenciales.
- **Protección contra fuerza bruta:** `django-axes` limita los intentos de login fallidos, con detección de la IP real del cliente detrás del proxy.
- **Ruta de administración ofuscada:** el panel admin se sirve en una ruta configurable por entorno, en lugar de la predeterminada.
- **Cabeceras de seguridad** y configuración de cookies seguras en producción.
- **Filtro anti-spam sin fricción:** campo *honeypot* en el formulario público, sin necesidad de CAPTCHA.

> Las técnicas anteriores se documentan a nivel conceptual. Los valores concretos (rutas, IPs, credenciales) viven fuera del control de versiones.

---

## Optimización y rendimiento

- **Optimización automática de imágenes:** al subir cualquier imagen desde el admin, se redimensiona y comprime automáticamente con Pillow (reducciones típicas superiores al 90 % de peso), sin intervención manual.
- **Archivos estáticos con hash (cache busting):** `ManifestStaticFilesStorage` en producción para invalidar caché de forma fiable al desplegar cambios.
- **Carga diferida (lazy loading)** de imágenes de la galería.
- **CDN de Cloudflare** para servir contenido estático desde ubicaciones cercanas al usuario.

---

## SEO técnico

- **Sitemap XML** generado dinámicamente con `django.contrib.sitemaps` (páginas fijas, servicios y artículos).
- **robots.txt** que referencia el sitemap.
- **Registro en Google Search Console** con sitemap enviado.
- **URLs semánticas** con slug, meta descriptions por página, texto alternativo en imágenes y etiquetas Open Graph en artículos.

---

## Instalación local

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

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear un archivo `.env` en la raíz a partir del ejemplo:

```bash
cp .env.example .env
```

En desarrollo, sin `.env`, la aplicación usa valores por defecto seguros (DEBUG activo, SQLite). En producción, el `.env` define `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, las credenciales de PostgreSQL y la ruta del admin.

### 5. Migrar y crear superusuario

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Levantar el servidor

```bash
python manage.py runserver
```

Abrir **http://127.0.0.1:8000/**

---

## Estructura del proyecto

```
sunfilm/
├── config/                 # Configuración del proyecto
│   ├── settings.py         # Ajustes (variables de entorno)
│   ├── urls.py             # URLs raíz + sitemap + robots
│   └── wsgi.py
├── core/                   # Portada, nosotros, cotizaciones
│   ├── models.py           # Modelo Cotizacion
│   ├── forms.py            # Formulario con honeypot
│   ├── utils.py            # Optimización de imágenes
│   ├── sitemaps.py         # Definición del sitemap
│   └── views.py            # home, nosotros, cotizar, robots.txt
├── servicios/              # Catálogo de servicios
│   ├── models.py           # Categoria, Servicio
│   └── views.py            # lista, detalle
├── galeria/                # Galería de trabajos
│   └── models.py           # Trabajo
├── blog/                   # Consejos y tips
│   ├── models.py           # CategoriaPost, Post
│   └── views.py            # lista con buscador, detalle
├── templates/              # Plantillas globales
│   ├── base.html
│   └── partials/           # navbar, footer, whatsapp
├── static/css/             # Estilos
├── manage.py
├── requirements.txt
└── README.md
```

Patrón **MTV** (Model-Template-View), una app por dominio de negocio. Cada app encapsula sus modelos, vistas, URLs, admin y plantillas.

---

## Modelo de datos

| App | Modelo | Descripción |
|---|---|---|
| `servicios` | `Categoria` | Agrupa servicios por tipo |
| `servicios` | `Servicio` | Servicio con descripción, beneficios, imagen y flag de destacado |
| `galeria` | `Trabajo` | Foto de trabajo realizado, vinculada a un servicio |
| `blog` | `CategoriaPost` | Categorías de artículos |
| `blog` | `Post` | Artículo con estado borrador/publicado y CTA a un servicio |
| `core` | `Cotizacion` | Solicitud del cliente con seguimiento de estado tipo CRM |

**Relaciones:** `Servicio` → `Categoria` (PROTECT) · `Trabajo` → `Servicio` (SET_NULL) · `Post` → `CategoriaPost` / `Servicio` (SET_NULL) · `Cotizacion` → `Servicio` (SET_NULL)

Las imágenes de todos los modelos pasan por optimización automática al guardarse (ver `core/utils.py`).

---

## Autor

Desarrollado por **Hans Soto González**
Estudiante de Ingeniería en Ciberseguridad · orientado a SOC / Blue Team

[github.com/hanssoto-cyber](https://github.com/hanssoto-cyber)

---

*Proyecto real en producción. El código se comparte con fines de portafolio; la configuración sensible del entorno de producción no se incluye en el repositorio.*