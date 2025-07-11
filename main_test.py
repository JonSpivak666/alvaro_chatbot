from core.whatsapp import enviar_mensaje_whatsapp

def main():
    mensaje = "Hola, soy Álvaro Medina. ¿En qué puedo ayudarte hoy? 😊"
    respuesta = enviar_mensaje_whatsapp(mensaje)
    print("Respuesta de WhatsApp API:")
    print(respuesta)

if __name__ == "__main__":
    main()
