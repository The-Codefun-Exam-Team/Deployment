"""Deploy the all parts of the project with a single click."""
import requests
import subprocess
VERSION = 'v1.0.0'

config_files = ['proxy.env', 'backend.env', 'cert.pem']
def check_config():
    print("Creating dummy config files")
    for name in config_files:
        with open(name, "r") as file:
            pass

def run_command(*args) -> subprocess.CompletedProcess:
    return subprocess.run(" ".join(["sudo", *args]), check=True, shell=True)

def install_docker():
    def setup_docker_repo() -> None:
        def enable_apt_https():
            run_command("apt", "-qq", "-y", "update")
            run_command("apt", "-qq", "-y", "install", "ca-certificates",
                        "curl", "gnupg", "lsb-release")

        def add_gpg_key():
            run_command("mkdir", "-p", "/etc/apt/keyrings")
            run_command("curl", "-fsSL", "https://download.docker.com/linux/debian/gpg", "|",
                        "sudo", "gpg", "--yes", "--dearmor", "-o", "/etc/apt/keyrings/docker.gpg")

        def setup_repo():
            run_command("echo", '"deb [arch=$(dpkg --print-architecture) \
                signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
                $(lsb_release -cs) stable"', "|",
                        "tee /etc/apt/sources.list.d/docker.list > /dev/null")

        enable_apt_https()
        add_gpg_key()
        setup_repo()

    def install_docker_engine() -> None:
        run_command("apt", "-qq", "-y", "update")
        run_command("apt", "-qq", "-y", "install", "docker-ce",
                    "docker-ce-cli", "containerd.io", "docker-compose-plugin")
        run_command("docker", "run", "--rm", "hello-world")

    print("Installing docker")
    setup_docker_repo()
    install_docker_engine()
    print("Docker installed successfully")


def compose_up():
    print("Calling docker compose up")
    run_command("docker", "compose", "up", "-d")


def check_availability(hostname: str, verify: bool) -> None:
    requests.packages.urllib3.disable_warnings() 
    def check_frontend():
        r = requests.get(f"https://{hostname}/login", verify=verify)
        if r.status_code != 200:
            raise RuntimeError("Frontend not live")
        print(r.text)

    def check_backend():
        r = requests.get(f"https://{hostname}/api/ping", verify=verify)
        if r.status_code != 200:
            raise RuntimeError("Backend not live")
        print(r.text)
    
    print("Checking availability")
    check_frontend()
    check_backend()
    print("All services running")

def no_ip_update(hostname: str, credentials: tuple[str, str], mail: str) -> str:
    # No-IP credentials
    def send_request():
        r = requests.get("https://dynupdate.no-ip.com/nic/update",
                         auth=credentials,
                         params={'hostname': hostname},
                         headers={'User-Agent': f'Codefun-Debug SingleClickDeployer/{VERSION} {mail}'})
        if r.status_code != 200 or not (r.text.startswith("good") or r.text.startswith("nochg")):
            raise RuntimeError(f"No-IP responded with {r.text}")
        return r.text

    print('Updating No-IP record')
    no_ip_r = send_request()
    print('No-IP update success. Response from No-IP: ', no_ip_r)


def local_setup(real_domain: str, no_ip_domain: str, no_ip_cred: tuple[str, str]):
    check_config()
    install_docker()
    compose_up()
    check_availability("localhost", False)

    no_ip_update(no_ip_domain, no_ip_cred, "abc@def.com")
    check_availability(real_domain, True)

if __name__ == '__main__':
    import fabric
    from fabric import transfer
    print("Entering remote setup mode")
    ssh_addr = input("Enter SSH host: ")
    real_domain = input("Real domain name: ")
    no_ip_domain = input("No-IP domain name: ")
    no_ip_username = input("No-IP username: ")
    no_ip_password = input("No-IP password: ")
    c = fabric.Connection(host=ssh_addr, user="root")

    c.run("rm -f -r Deployment")
    c.run("git clone https://github.com/The-Codefun-Exam-Team/Deployment.git")
    c.run("cd Deployment")

    t = transfer.Transfer(c)
    for name in config_files:
        t.put(name, name)
    
    c.run(f"python3 -c 'from SingleClick import local_setup; \
local_setup({real_domain}, {no_ip_domain}, ({no_ip_username}, {no_ip_password}))'")
