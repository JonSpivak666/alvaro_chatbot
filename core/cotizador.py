from datetime import datetime

def generar_resumen(nombre: str, correo: str, licencia: str, cantidad: int, total: float) -> str:
    """
    Genera un resumen legible y formal de la cotización para mostrar o enviar por correo.
    """

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    resumen = f"""
🧾 RESUMEN DE COTIZACIÓN — Álvaro Medina
Fecha: {fecha}

Cliente:
- Nombre: {nombre}
- Correo: {correo}

Detalle de la Solicitud:
- Licencia solicitada: {licencia}
- Cantidad: {cantidad}
- Precio total estimado: ${total:,.2f} USD

📩 En breve, un ejecutivo se pondrá en contacto contigo para continuar con el proceso.

Gracias por tu interés.
    """.strip()

    return resumen
