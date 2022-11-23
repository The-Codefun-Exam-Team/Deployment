import requests
from os import path

config_files = ['proxy.env', 'backend.env', 'cert.pem']
def check_config():
    def real_path(name: str) -> str:
        return str(path.realpath(
            path.join(__file__,
                path.pardir, path.pardir, path.pardir,
                "data", name)))

    for name in config_files:
        with open(real_path(name), "r") as file:
            print(f"{name} exists")

def check_availability(hostname: str, verify: bool) -> None:
    requests.packages.urllib3.disable_warnings()
    def check_address(url: str):
        r = requests.get(url, verify=verify)
        if r.status_code != 200:
            raise RuntimeError(f"{url} not live")
        print(f"{url} is alive")

    check_address(f"https://{hostname}/login")
    check_address(f"https://{hostname}/api/ping")
