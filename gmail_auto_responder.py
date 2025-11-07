#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-responder inteligente de Gmail con OpenAI
Autor: Rafael M.
Versión: 1.6 (solo responde a correos recibidos después de iniciar el script)
"""

import os
import time
import base64
import logging
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv
import openai
from datetime import datetime

# -------------------------------
# CONFIGURACIÓN DE LOGGING
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("auto_reply_log.txt"),
        logging.StreamHandler()
    ]
)

# -------------------------------
# VARIABLES DE ENTORNO
# -------------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 900))
LABEL_NAME = "Respondido_por_bot"
LAST_TIMESTAMP_FILE = "last_timestamp.txt"
RESPONDED_IDS_FILE = "responded_ids.txt"

openai.api_key = OPENAI_API_KEY

# -------------------------------
# FUNCIONES AUXILIARES
# -------------------------------
def load_last_timestamp():
    if os.path.exists(LAST_TIMESTAMP_FILE):
        with open(LAST_TIMESTAMP_FILE, "r") as f:
            return int(f.read().strip())
    else:
        now = int(time.time())
        with open(LAST_TIMESTAMP_FILE, "w") as f:
            f.write(str(now))
        return now

def save_last_timestamp(ts):
    with open(LAST_TIMESTAMP_FILE, "w") as f:
        f.write(str(ts))

def load_responded_ids():
    if not os.path.exists(RESPONDED_IDS_FILE):
        return set()
    with open(RESPONDED_IDS_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f.readlines())

def save_responded_id(msg_id):
    with open(RESPONDED_IDS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{msg_id}\n")

# -------------------------------
# SERVICIO GMAIL
# -------------------------------
def get_gmail_service():
    SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            from google_auth_oauthlib.flow import InstalledAppFlow
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

# -------------------------------
# ETIQUETA
# -------------------------------
def get_or_create_label(service):
    labels = service.users().labels().list(userId="me").execute().get("labels", [])
    for label in labels:
        if label["name"] == LABEL_NAME:
            return label["id"]
    new_label = service.users().labels().create(userId="me", body={"name": LABEL_NAME}).execute()
    return new_label["id"]


# -------------------------------
# RESPUESTA AUTOMÁTICA SIN IA (modo seguro)
# -------------------------------
def generate_ai_reply(original_text):
    """
    Genera una respuesta automática sin usar IA.
    Se puede reactivar la IA simplemente cambiando USE_AI=True en .env
    cuando tengas una API Key válida.
    """
    use_ai = os.getenv("USE_AI", "False").lower() == "true"

    # IA desactivada → respuesta fija
    if not use_ai:
        logging.info("💤 IA desactivada, usando respuesta automática fija.")
        return (
            "Gracias por tu mensaje. He recibido tu correo y lo revisaré en breve.\n\n"
            "Este es un mensaje automático generado por mi asistente virtual.\n"
            "— Rafael M."
        )

    # (modo preparado para IA, por si la activas en el futuro)
    try:
        prompt = f"""Redacta una breve respuesta automática en español,
con tono profesional y amable, confirmando la recepción del mensaje.
Incluye una línea final que diga: "Este es un mensaje automático generado por mi asistente virtual."
Firma siempre con “— Rafael M.”.

Correo recibido:
{original_text}
"""
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente profesional que escribe respuestas automáticas educadas y concisas."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.6,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        logging.error(f"Error generando respuesta IA: {e}")
        return (
            "Gracias por tu mensaje. He recibido tu correo y lo revisaré en breve.\n\n"
            "Este es un mensaje automático generado por mi asistente virtual.\n"
            "— Rafael M."
        )

# -------------------------------
# RESPUESTA AUTOMÁTICA SIN IA (modo seguro)
# -------------------------------
def generate_ai_reply(original_text):
    """
    Genera una respuesta automática sin usar IA.
    Se puede activar IA en el futuro con USE_AI=True en .env
    """
    use_ai = os.getenv("USE_AI", "False").lower() == "true"

    if not use_ai:
        logging.info("💤 IA desactivada, usando respuesta automática fija.")
        return (
            "Gracias por tu mensaje. He recibido tu correo y lo revisaré en breve.\n\n"
            "Este es un mensaje automático generado por mi asistente virtual.\n"
            "— Rafael M."
        )

    # (Solo se usa si activas la IA más adelante)
    try:
        prompt = f"""Redacta una breve respuesta automática en español,
con tono profesional y amable, confirmando la recepción del mensaje.
Incluye una línea final que diga: "Este es un mensaje automático generado por mi asistente virtual."
Firma siempre con “— Rafael M.”.

Correo recibido:
{original_text}
"""
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente profesional que escribe respuestas automáticas educadas y concisas."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.6,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        logging.error(f"Error generando respuesta IA: {e}")
        return (
            "Gracias por tu mensaje. He recibido tu correo y lo revisaré en breve.\n\n"
            "Este es un mensaje automático generado por mi asistente virtual.\n"
            "— Rafael M."
        )

# -------------------------------
# ENVIAR RESPUESTA
# -------------------------------
def send_reply(service, to_email, subject, reply_text):
    try:
        message = MIMEText(reply_text)
        message["to"] = to_email
        message["subject"] = f"Re: {subject[:60]}"
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        service.users().messages().send(userId="me", body={"raw": raw}).execute()
        logging.info(f"📨 Respuesta enviada a {to_email}")
    except Exception as e:
        logging.error(f"Error enviando respuesta: {e}")

# -------------------------------
# PROCESAR NUEVOS EMAILS
# -------------------------------
def process_new_emails():
    service = get_gmail_service()
    label_id = get_or_create_label(service)
    responded_ids = load_responded_ids()
    last_ts = load_last_timestamp()

    # Buscar correos nuevos desde el último timestamp
    query = f"after:{last_ts} -label:{LABEL_NAME} in:inbox"
    results = service.users().messages().list(userId="me", q=query).execute()
    messages = results.get("messages", [])
    if not messages:
        logging.info("📭 No hay correos nuevos desde la última ejecución.")
        return

    # Obtener tu propio correo
    profile = service.users().getProfile(userId="me").execute()
    my_email = profile["emailAddress"]

    latest_ts = last_ts

    for msg_obj in messages:
        msg_id = msg_obj["id"]
        if msg_id in responded_ids:
            continue

        msg = service.users().messages().get(userId="me", id=msg_id).execute()
        headers = msg["payload"].get("headers", [])
        snippet = msg.get("snippet", "")
        sender = next((h["value"] for h in headers if h["name"].lower() == "from"), "")
        subject = next((h["value"] for h in headers if h["name"].lower() == "subject"), "Sin asunto")
        internal_date = int(msg.get("internalDate", 0)) // 1000

        # Actualizar último timestamp
        if internal_date > latest_ts:
            latest_ts = internal_date

        # Ignorar correos propios o automáticos
        if my_email.lower() in sender.lower() or "no-reply" in sender.lower():
            logging.info(f"⏭️ Ignorado correo propio o automático: {subject}")
            continue

        # Generar y enviar respuesta
        reply_text = generate_ai_reply(snippet)
        send_reply(service, sender, subject, reply_text)

        # Marcar como leído, etiquetar y registrar
        service.users().messages().modify(
            userId="me",
            id=msg_id,
            body={"removeLabelIds": ["UNREAD"], "addLabelIds": [label_id]},
        ).execute()
        save_responded_id(msg_id)
        logging.info(f"✅ Respondido: {subject} de {sender}")

    save_last_timestamp(latest_ts)

# -------------------------------
# LOOP PRINCIPAL
# -------------------------------
def main():
    logging.info("🤖 Auto-responder Gmail iniciado (solo correos nuevos desde ahora)")
    while True:
        try:
            process_new_emails()
        except Exception as e:
            logging.error(f"Error general: {e}")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
