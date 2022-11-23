import requests

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

    no_ip_r = send_request()
    return no_ip_r
