from os import path
import SSH

config_files = ['proxy.env', 'backend.env', 'cert.pem']

data_path = str(path.realpath(
        path.join(__file__, path.pardir, path.pardir, path.pardir, "data")))

if __name__ == '__main__':
    print("Setting up remotely")
    ssh_addr = input("Enter SSH host: ")
    real_domain = input("Real domain name: ")
    no_ip_domain = input("No-IP domain name: ")
    no_ip_username = input("No-IP username: ")
    no_ip_password = input("No-IP password: ")

    c = SSH.SSHSession(ssh_addr)
    c.run_command([
        "sudo apt-get update", "sudo apt-get -qq -y install git",
        "rm -f -r Deployment",
        "git clone https://github.com/The-Codefun-Exam-Team/Deployment.git"])
    
    c.send_file(data_path, f"Deployment")
    c.run_command(f"python3 Deployment/scripts/local_setup/LocalSetup.py {real_domain} {no_ip_domain} {no_ip_username} {no_ip_password}")
