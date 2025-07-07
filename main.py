from fastapi import FastAPI, Request
from pydantic import BaseModel
from core.gemini_client import responder_con_gemini
from core.licencias_parser import obtener_precio
from core.cotizador import generar_resumen
from core.database import guardar_cotizacion
from emailing.mailer import enviar_correos
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
CORREO_EJECUTIVO = os.getenv("CORREO_EJECUTIVO", "ventas.ejemplo@empresa.com")

# Modelo de entrada para el mensaje
class MensajeUsuario(BaseModel):
    nombre: str
    correo: str
    mensaje: str

@app.post("/webhook")
async def procesar_mensaje(datos: MensajeUsuario):
    nombre = datos.nombre
    correo = datos.correo
    mensaje = datos.mensaje.strip().lower()

    if any(palabra in mensaje for palabra in ["cotiza", "licencia", "precio", "presupuesto"]):
        # Supone que el usuario ya te mandó algo como: "Cotiza licencia X, 3 unidades"
        try:
            partes = mensaje.split()
            licencia = partes[-2]  # penúltimo elemento
            cantidad = int(partes[-1])  # último elemento

            precio_unitario = obtener_precio(licencia)
            if precio_unitario is None:
                return {
                    "respuesta": f"No encontré la licencia '{licencia}'. Un ejecutivo se comunicará contigo pronto al correo {correo}."
                }

            total = precio_unitario * cantidad
            resumen = generar_resumen(nombre, correo, licencia, cantidad, total)
            guardar_cotizacion(nombre, correo, licencia, cantidad, total)
            enviar_correos(correo_cliente=correo, correo_ejecutivo=CORREO_EJECUTIVO, resumen=resumen)

            return {"respuesta": resumen}

        except Exception as e:
            return {
                "respuesta": f"Hubo un error procesando tu solicitud. Por favor revisa el formato. Detalles: {e}"
            }

    else:
        respuesta = responder_con_gemini(mensaje)
        return {"respuesta": respuesta}


