import json
import sys

# Función para cargar configuraciones desde un archivo JSON
def load_config(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Archivo {filename} no encontrado. Se usarán configuraciones por defecto.")
        sys.exit(1)  # Salir del programa si no se puede cargar el archivo

# Función para guardar configuraciones en un archivo JSON
def save_config(filename, config):
    try:
        with open(filename, 'w') as file:
            json.dump(config, file, indent=4)
        print("Configuraciones guardadas exitosamente.\n")
    except Exception as e:
        print(f"Error al guardar el archivo {filename}: {e}")

# Función para modificar una configuración específica
def modify_config(config, key, new_value):
    if key in config:
        config[key] = new_value
        print(f"Configuración '{key}' modificada a '{new_value}'")
    else:
        print(f"Configuración '{key}' no encontrada.")
