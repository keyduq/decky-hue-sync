import os
import subprocess
import urllib.request
import json

class Plugin:
    async def _main(self):
        pass

    async def _unload(self):
        pass

    async def get_hyperhdr_info(self):
        try:
            url = "http://localhost:8090/json-rpc"
            payload = {"command": "serverinfo"}
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='POST')
            with urllib.request.urlopen(req, timeout=2) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            return {"error": str(e)}

    async def set_hdr(self, state: int):
        try:
            url = "http://localhost:8090/json-rpc"
            payload = {
                "command": "videomodehdr",
                "HDR": state
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='POST')
            with urllib.request.urlopen(req, timeout=2) as response:
                return True
        except Exception as e:
            return str(e)

    async def set_brightness(self, value: int):
        try:
            url = "http://localhost:8090/json-rpc"
            payload = {
                "command": "adjustment",
                "adjustment": {
                    "classic_config": False,
                    "brightness": value
                }
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='POST')
            with urllib.request.urlopen(req, timeout=2) as response:
                return True
        except Exception as e:
            return str(e)

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