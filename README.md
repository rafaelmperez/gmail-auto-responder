# 🤖 Gmail Auto-Responder — Automatiza tus respuestas con Python y Gmail API

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Gmail API](https://img.shields.io/badge/Gmail%20API-Enabled-green)
![Systemd](https://img.shields.io/badge/systemd-Service-orange)
![OpenAI](https://img.shields.io/badge/OpenAI-Optional-blueviolet)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📬 Descripción general

**Gmail Auto-Responder** es un proyecto desarrollado por **Rafael M.** que permite responder automáticamente a correos nuevos en tu bandeja de entrada de Gmail.  
Está diseñado para ejecutarse en segundo plano, incluso tras reiniciar el equipo, gracias a su integración con **systemd**.  

Incluye una función opcional de **respuesta inteligente con IA (OpenAI)**, que se puede activar o desactivar fácilmente.

---

## 🧠 Características principales

- 📩 Responde automáticamente a correos nuevos recibidos en Gmail.  
- 🧠 Respuestas inteligentes mediante IA (OpenAI) — *opcional*.  
- 🔒 Evita respuestas duplicadas o bucles automáticos.  
- ⚙️ Corre en segundo plano como servicio `systemd`.  
- 🧾 Guarda un log detallado de cada acción.  
- 🧰 Configuración sencilla con archivo `.env`.  
- 🕒 Intervalo de verificación configurable (por defecto cada 15 minutos).  

---

## 📋 Requisitos previos

- Python **3.10** o superior  
- Una cuenta de **Gmail**  
- Credenciales **OAuth 2.0** generadas en [Google Cloud Console](https://console.cloud.google.com/)  
- Acceso a la API de Gmail habilitado  
- (Opcional) Clave API de **OpenAI** si deseas activar la IA  

---

## ⚙️ Instalación

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/gmail-auto-responder.git
cd gmail-auto-responder
