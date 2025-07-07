import os
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Configurar cliente Gemini
genai.configure(api_key=API_KEY)
modelo = genai.GenerativeModel("gemini-pro")


def responder_con_gemini(pregunta: str) -> str:
    """
    Envía la pregunta a Gemini y devuelve la respuesta.
    """
    try:
        respuesta = modelo.generate_content(pregunta)
        return respuesta.text.strip()

    except Exception as e:
        print(f"[ERROR] Gemini API falló: {e}")
        return "Lo siento, no pude procesar tu solicitud en este momento. Por favor intenta más tarde."
