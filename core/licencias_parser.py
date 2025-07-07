import os
import pandas as pd

# Ruta a los archivos Excel
DATA_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data')

ARCHIVOS = [
    "Lista Academico.xlsx",
    "Lista Comercial.xlsx",
    "Lista Gobierno.xlsx"
]

def obtener_precio(nombre_licencia: str):
    """
    Busca el precio estimado de una licencia en los tres archivos.
    Retorna el precio como float si lo encuentra, o None si no existe.
    """
    nombre_licencia = nombre_licencia.strip().lower()

    for archivo in ARCHIVOS:
        ruta = os.path.join(DATA_FOLDER, archivo)

        try:
            df = pd.read_excel(ruta)

            for _, row in df.iterrows():
                if 'licencia' in row and 'precio' in row:
                    nombre = str(row['licencia']).strip().lower()
                    if nombre_licencia == nombre:
                        return float(row['precio'])

        except Exception as e:
            print(f"Error leyendo {archivo}: {e}")

    return None
