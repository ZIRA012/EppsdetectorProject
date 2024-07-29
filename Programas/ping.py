import subprocess
import platform


def ping(host):
    """
    Hace ping a un host determinado.

    Parámetros:
    host (str): La dirección IP o el nombre del host al que se desea hacer ping.

    Retorna:
    bool: True si el ping fue exitoso, False en caso contrario.
    """
    # Determinar el parámetro de conteo de paquetes dependiendo del sistema operativo
    param = "-n" if platform.system().lower() == "windows" else "-c"

    # Construir el comando de ping
    command = ["ping", param, "1", host]

    # Ejecutar el comando de ping y capturar la salida
    return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0


# Ejemplo de uso
ip_address = "10.22.77.1"
if ping(ip_address):
    print(f"Ping a {ip_address} exitoso!")
else:
    print(f"Ping a {ip_address} fallido.")