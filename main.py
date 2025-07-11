from fastapi import FastAPI
from pydantic import BaseModel
from core.gemini_client import responder_con_gemini
from core.licencias_parser import obtener_precio
from core.cotizador import generar_resumen
from core.database import guardar_cotizacion
from emailing.mailer import enviar_correos
from core.whatsapp import enviar_mensaje_whatsapp
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
CORREO_EJECUTIVO = os.getenv("CORREO_EJECUTIVO", "ventas.ejemplo@empresa.com")


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
        try:
            partes = mensaje.split()
            licencia = partes[-2]  # penúltimo elemento
            cantidad = int(partes[-1])  # último elemento

            precio_unitario = obtener_precio(licencia)
            if precio_unitario is None:
                texto_fallo = (
                    f"No encontré la licencia '{licencia}'. "
                    f"Un ejecutivo se comunicará contigo pronto al correo {correo}."
                )
                enviar_mensaje_whatsapp(correo, texto_fallo)
                return {"respuesta": texto_fallo}

            total = precio_unitario * cantidad
            resumen = generar_resumen(nombre, correo, licencia, cantidad, total)
            guardar_cotizacion(nombre, correo, licencia, cantidad, total)
            enviar_correos(
                correo_cliente=correo,
                correo_ejecutivo=CORREO_EJECUTIVO,
                resumen=resumen
            )
            enviar_mensaje_whatsapp(correo, resumen)

            return {"respuesta": resumen}

        except Exception as e:
            error_msg = f"Hubo un error procesando tu solicitud. Detalles: {e}"
            enviar_mensaje_whatsapp(correo, error_msg)
            return {"respuesta": error_msg}

    else:
        respuesta = responder_con_gemini(mensaje)
        enviar_mensaje_whatsapp(correo, respuesta)
        return {"respuesta": respuesta}


