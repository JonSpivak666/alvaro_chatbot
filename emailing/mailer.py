import os
import yagmail
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")

def enviar_correos(correo_cliente: str, correo_ejecutivo: str, resumen: str):
    """
    Envía el resumen de cotización al cliente y al ejecutivo.
    """
    try:
        # Conexión segura al servidor de Gmail
        yag = yagmail.SMTP(user=GMAIL_USER, password=GMAIL_PASS)

        asunto = "Resumen de cotización | Álvaro Medina"
        cuerpo = resumen

        # Enviar al cliente
        yag.send(to=correo_cliente, subject=asunto, contents=cuerpo)

        # Enviar copia al ejecutivo
        yag.send(to=correo_ejecutivo, subject=f"Copia interna — {asunto}", contents=cuerpo)

        print("📤 Correos enviados con éxito.")

    except Exception as e:
        print(f"[ERROR] No se pudo enviar el correo: {e}")
