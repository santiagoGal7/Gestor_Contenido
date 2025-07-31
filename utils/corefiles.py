import json
import os

Data_Dir = "data"
File_coleccion = os.path.join(Data_Dir, "coleccion.json")

def asegurar_archivo_datos():
    if not os.path.exists(Data_Dir):
        os.makedirs(Data_Dir)
    if not os.path.exists(File_coleccion):
        with open(File_coleccion, 'w', encoding='utf-8') as f:
            json.dump([], f)

def leer_coleccion():
    asegurar_archivo_datos()
    try:
        with open(File_coleccion, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def escribir_coleccion(coleccion):
    asegurar_archivo_datos()
    try:
        with open(File_coleccion, 'w', encoding='utf-8') as f:
            json.dump(coleccion, f, indent=4, ensure_ascii=False)
        return True
    except IOError:
        return False