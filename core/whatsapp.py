import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Variables de entorno
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
WHATSAPP_TO_NUMBER = os.getenv("WHATSAPP_TO_NUMBER")

# Endpoint base de WhatsApp Cloud API
WHATSAPP_API_URL = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_ID}/messages"

# Función para enviar un mensaje de texto
def enviar_mensaje_whatsapp(texto: str) -> dict:
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    body = {
        "messaging_product": "whatsapp",
        "to": WHATSAPP_TO_NUMBER,
        "type": "text",
        "text": {
            "body": texto
        }
    }

    response = requests.post(WHATSAPP_API_URL, headers=headers, json=body)

    if response.status_code == 200:
        return {
            "status": "enviado",
            "detalle": response.json()
        }
    else:
        return {
            "status": "error",
            "codigo_http": response.status_code,
            "detalle": response.text
        }
