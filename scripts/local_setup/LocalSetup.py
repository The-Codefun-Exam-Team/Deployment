"""Deploy the all parts of the project with a single click."""
VERSION = 'v1.0.0'
print(f"Local setup script version {VERSION}", flush=True)

import time, sys
import NoIP, Checks, Docker

if __name__ == '__main__':
    real_domain, no_ip_domain = sys.argv[1], sys.argv[2]
    no_ip_cred = sys.argv[3], sys.argv[4]

    print("Checking config files", flush=True)
    Checks.check_config()
    
    print("Installing docker", flush=True)
    Docker.install()

    print("Calling docker compose up", flush=True)
    Docker.compose_up()

    print("Waiting for services to finish setting up", flush=True)
    time.sleep(10)

    print("Checking availability", flush=True)
    Checks.check_availability("localhost", False)

    print("Updating No-IP record", flush=True)
    no_ip_r = NoIP.no_ip_update(no_ip_domain, no_ip_cred, "abc@def.com", VERSION)

    print(f"No-IP update success. Response from No-IP: {no_ip_r}", flush=True)

    print("Waiting 5 mins for No-IP records update", flush=True)
    time.sleep(5*60)

    print("Checking availability at the real domain", flush=True)
    Checks.check_availability(real_domain, True)
