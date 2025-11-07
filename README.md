🤖 Gmail Auto-Responder — Automatiza tus respuestas con Python y Gmail API

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Gmail API](https://img.shields.io/badge/Gmail%20API-Enabled-green)
![Systemd](https://img.shields.io/badge/Systemd-Service-orange)
![OpenAI](https://img.shields.io/badge/OpenAI-Optional-blueviolet)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📬 Descripción general

**Gmail Auto-Responder** es un proyecto desarrollado por **Rafael M.** que permite responder automáticamente a correos nuevos en tu cuenta de Gmail.  
Está diseñado para ejecutarse **en segundo plano** (incluso después de reiniciar el sistema) mediante un servicio **systemd**.  

Además, ofrece una opción de **respuesta inteligente con IA (OpenAI)**, que se puede activar o desactivar fácilmente mediante el archivo `.env`.  

---

## 🧠 Características principales

- 📩 Responde automáticamente a nuevos correos recibidos.  
- 🧠 Respuestas naturales generadas por IA (opcional con OpenAI API).  
- 🔒 Evita bucles o respuestas duplicadas a los mismos mensajes.  
- ⚙️ Se ejecuta en segundo plano como servicio **systemd**.  
- 🧾 Guarda logs detallados con cada acción realizada.  
- 🧰 Configuración sencilla mediante archivo `.env`.  
- 🕒 Intervalo de verificación configurable (por defecto cada **15 minutos**).  

---

## 📋 Requisitos previos

- 🐍 **Python 3.10+**
- 📧 **Cuenta de Gmail** con acceso IMAP habilitado  
- 🔑 **Credenciales OAuth 2.0** desde [Google Cloud Console](https://console.cloud.google.com/)
- 🧩 **API de Gmail** activada  
- 🧠 *(Opcional)* **Clave API de OpenAI** para respuestas inteligentes  

---

## ⚙️ Instalación paso a paso

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/rafaelmperez/gmail-auto-responder.git
cd gmail-auto-responder
````

### 2️⃣ Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar variables de entorno

Copia el archivo de ejemplo y edítalo:

```bash
cp .env.example .env
```

Edita las siguientes variables en `.env`:

```
OPENAI_API_KEY=
USE_AI=False
CHECK_INTERVAL=900
```

> 🧩 Si no tienes clave de OpenAI, simplemente deja `USE_AI=False`.

### 5️⃣ Añadir credenciales de Google

Descarga tu `credentials.json` desde Google Cloud Console (OAuth Client)
y colócalo en la carpeta principal del proyecto:

```
~/gmail-auto-responder/credentials.json
```

El script generará automáticamente `token.json` la primera vez que se ejecute.

---

## 🚀 Ejecución manual

```bash
source venv/bin/activate
python3 gmail_auto_responder.py
```

---

## 🧩 Ejecución automática con Systemd

Permite que el bot se inicie automáticamente con tu sistema Linux.

### 1️⃣ Copiar el servicio

```bash
sudo cp auto_responder.service /etc/systemd/system/
```

### 2️⃣ Recargar e iniciar

```bash
sudo systemctl daemon-reload
sudo systemctl enable gmail-auto-responder.service
sudo systemctl start gmail-auto-responder.service
```

### 3️⃣ Verificar estado

```bash
systemctl status gmail-auto-responder.service
```

### 4️⃣ Ver logs en tiempo real

```bash
tail -f ~/gmail-auto-responder/auto_responder.log
```

---

## 🔒 Seguridad

* **Nunca subas tus credenciales ni claves API a GitHub.**

* Añade estos archivos a tu `.gitignore`:

  ```
  venv/
  .env
  credentials.json
  token.json
  auto_responder.log
  last_timestamp.txt
  responded_ids.txt
  ```

* Tus claves se almacenan solo de forma **local y privada**.

* El sistema evita responder a correos automáticos o duplicados.

---

## 🧠 Ejemplo de respuesta automática

```text
Este es un mensaje automático de confirmación.
He recibido tu correo y te responderé en cuanto sea posible.
— Rafael M.
```

*(Modo IA activado:)*

```text
¡Gracias por tu mensaje! 😊  
He recibido tu correo y pronto tendrás una respuesta más detallada.  
— Rafael M. (IA Auto-Responder)
```

---

## 🧰 Posibles mejoras futuras

* Panel web con Flask para visualizar logs y estadísticas.
* Integración con Telegram o Discord para notificaciones.
* Soporte IMAP/SMTP sin dependencia de la API de Gmail.
* Implementación de IA local sin conexión a OpenAI.

---

## 📁 Estructura del proyecto

```
gmail-auto-responder/
├── gmail_auto_responder.py
├── start_auto_responder.sh
├── .env.example
├── requirements.txt
├── auto_responder.service
├── README.md
└── logs/
    └── auto_responder.log
```

---

## ⚙️ Dependencias principales

```text
google-auth
google-auth-oauthlib
google-api-python-client
python-dotenv
psutil
openai
logging
```

---

## 🧑‍💻 Autor

**Rafael M.**
💼 Desarrollador Python y entusiasta de la automatización.
📧 Contacto: [iloveprivacy_us@proton.me](mailto:iloveprivacy_us@proton.me)

---

## 📜 Licencia

Este proyecto está licenciado bajo la **MIT License**.
Consulta el archivo [LICENSE](LICENSE) para más información.

---

> “Automatiza tu bandeja de entrada con inteligencia.
> Un proyecto real de integración entre Python, Gmail API y Systemd.”
> — *Rafael M.*

```

---

¿Quieres que te genere también los archivos complementarios `.env.example`, `requirements.txt` y `auto_responder.service` con contenido profesional y seguro para subir al repo limpio?  
Así completas tu proyecto con toda la estructura ideal para publicar.
```
