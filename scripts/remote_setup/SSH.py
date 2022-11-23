import subprocess

class SSHSession:
    cred: str
    def __init__(self, addr: str):
        self.cred = f"root@{addr}"
    
    def send_file(self, src: str, dst: str):
        subprocess.run(["scp", src, f"{self.cred}:{dst}"])
    
    def run_command(self, cmd: list[str]):
        subprocess.run(["ssh", {self.cred}, ";".join(cmd)])
