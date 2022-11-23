from os import path
import fabric
from fabric import transfer

def real_path(name: str) -> str:
    return str(path.realpath(
        path.join(__file__,
            path.pardir, path.pardir,
            "data", name)))

config_files = ['proxy.env', 'backend.env', 'cert.pem']
if __name__ == '__main__':
    print("Setting up remotely")
    ssh_addr = input("Enter SSH host: ")
    real_domain = input("Real domain name: ")
    no_ip_domain = input("No-IP domain name: ")
    no_ip_username = input("No-IP username: ")
    no_ip_password = input("No-IP password: ")
    with fabric.Connection(host=ssh_addr, user="root") as c:
        c.run("sudo apt-get update; sudo apt-get -qq -y install git")
        c.run("rm -f -r Deployment")
        c.run("git clone https://github.com/The-Codefun-Exam-Team/Deployment.git")

        t = transfer.Transfer(c)
        for name in config_files:
            t.put(real_path(name), f"Deployment/data/{name}")
        c.run(f'cd Deployment/scripts/local_setup; python3 LocalSetup.py {real_domain} {no_ip_domain} {no_ip_username} {no_ip_password}')
