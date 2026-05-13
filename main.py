import os
import subprocess

class Plugin:
    async def _main(self):
        pass

    async def _unload(self):
        pass

    async def toggle_hue(self):
        try:
            command = 'su keyduq -c "XDG_RUNTIME_DIR=/run/user/1000 /home/keyduq/toggle-hue.sh"'
            subprocess.run(command, shell=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"
