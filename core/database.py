import os
import pandas as pd
from datetime import datetime

# Ruta al archivo local de cotizaciones
BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, '..', 'data', 'cotizaciones_clientes.csv')

def guardar_cotizacion(nombre: str, correo: str, licencia: str, cantidad: int, total: float):
    """
    Registra la cotización en un archivo CSV (base de datos local).
    """
    nueva_fila = {
        "nombre": nombre,
        "correo": correo,
        "licencia": licencia,
        "cantidad": cantidad,
        "total": round(total, 2),
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        # Si el archivo ya existe, cargarlo y agregar
        if os.path.exists(CSV_PATH):
            df = pd.read_csv(CSV_PATH)
            df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
        else:
            df = pd.DataFrame([nueva_fila])

        df.to_csv(CSV_PATH, index=False)

    except Exception as e:
        print(f"[ERROR] No se pudo guardar la cotización: {e}")
