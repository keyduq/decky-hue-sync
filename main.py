import os
import subprocess

class Plugin:
    async def _main(self):
        pass

    async def _unload(self):
        pass

    async def toggle_hue(self):
        # 1. Copiamos el entorno y borramos las mentiras de Decky Loader
        entorno_limpio = os.environ.copy()
        entorno_limpio["USER"] = "keyduq"
        entorno_limpio["LOGNAME"] = "keyduq"
        entorno_limpio["HOME"] = "/home/keyduq"
        
        # 2. Inyectamos las variables vitales para systemd y Wayland
        entorno_limpio["XDG_RUNTIME_DIR"] = "/run/user/1000"
        entorno_limpio["DBUS_SESSION_BUS_ADDRESS"] = "unix:path=/run/user/1000/bus"

        # Archivo chismoso para saber qué pasó
        log_file = "/home/keyduq/decky-debug.log"

        try:
            with open(log_file, "a") as f:
                f.write("--- Ejecutando Toggle Hue desde Decky ---\n")

            # 3. Usamos sudo pasándole nuestro entorno purificado
            comando = ['sudo', '-E', '-u', 'keyduq', '/home/keyduq/toggle-hue.sh']
            
            resultado = subprocess.run(comando, env=entorno_limpio, capture_output=True, text=True, check=True)
            
            with open(log_file, "a") as f:
                f.write(f"STDOUT (Éxito): {resultado.stdout}\n")
            return True

        except subprocess.CalledProcessError as e:
            with open(log_file, "a") as f:
                f.write(f"STDERR (Error del script): {e.stderr}\n")
            return f"Error: {e}"
            
        except Exception as e:
            with open(log_file, "a") as f:
                f.write(f"ERROR FATAL PYTHON: {str(e)}\n")
            return f"Error: {str(e)}"