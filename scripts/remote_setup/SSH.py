import subprocess

class SSHSession:
    cred: str
    def __init__(self, addr: str):
        self.cred = f"root@{addr}"
    
    def send_file(self, src: str, dst: str):
        subprocess.run(["scp", "-r", src, f"{self.cred}:{dst}"], check=True)
    
    def run_command(self, cmd: list[str] | str):
        if isinstance(cmd, str):
            cmd = [cmd]
        subprocess.run(["ssh", self.cred, f'"{";".join(cmd)}"'], check=True, shell=True)
