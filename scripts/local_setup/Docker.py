import subprocess
__all__ = ["install", "compose_up"]

def run_command(*args) -> subprocess.CompletedProcess:
    return subprocess.run(" ".join(["sudo", *args]), check=True, shell=True)

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
    print("Should be running Docker hello")
    # run_command("docker", "run", "--rm", "hello-world")

def install():
    setup_repo()
    install_docker_engine()

def compose_up():
    print("Starting docker compose")
    run_command("docker", "compose", "up", "-d")
    print("Finished docker compose up")
