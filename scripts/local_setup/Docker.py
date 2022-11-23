import subprocess
from os import path
__all__ = ["install", "compose_up"]

def run_command(*args) -> subprocess.CompletedProcess:
    return subprocess.run(" ".join(["sudo", *args]), check=True, shell=True, stdout=subprocess.PIPE)

def setup_repo() -> None:
    def enable_apt_https():
        run_command("apt-get", "-qq", "-y", "update")
        run_command("apt-get", "-qq", "-y", "install", "ca-certificates",
                    "curl", "gnupg", "lsb-release")

    def add_gpg_key():
        run_command("mkdir", "-p", "/etc/apt/keyrings")
        run_command("curl", "-fsSL", "https://download.docker.com/linux/debian/gpg", "|",
                    "sudo", "gpg", "--yes", "--dearmor", "-o", "/etc/apt/keyrings/docker.gpg")

    def setup_repo_apt():
        run_command("echo", '"deb [arch=$(dpkg --print-architecture) \
            signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
            $(lsb_release -cs) stable"', "|",
                    "tee /etc/apt/sources.list.d/docker.list > /dev/null")

    enable_apt_https()
    add_gpg_key()
    setup_repo_apt()

def install_docker_engine() -> None:
    run_command("apt-get", "-qq", "-y", "update")
    run_command("apt-get", "-qq", "-y", "install", "docker-ce",
                "docker-ce-cli", "containerd.io", "docker-compose-plugin")
    run_command("docker", "run", "--rm", "hello-world")

def install():
    setup_repo()
    install_docker_engine()

def compose_up():
    print("Starting docker compose")
    cwd = str(path.realpath(path.join(__file__,
                path.pardir, path.pardir, path.pardir)))
    subprocess.run(["docker", "compose", "up", "-d"], check=True, cwd=cwd, stdout=subprocess.PIPE)
    print("Finished docker compose up")
