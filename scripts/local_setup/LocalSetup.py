"""Deploy the all parts of the project with a single click."""
import time, sys
import NoIP, Checks, Docker

VERSION = 'v1.0.0'

if __name__ == '__main__':
    real_domain, no_ip_domain = sys.argv[1], sys.argv[2]
    no_ip_cred = sys.argv[3], sys.argv[4]

    print("Checking config files")
    Checks.check_config()
    
    print("Installing docker")
    Docker.install()

    print("Calling docker compose up")
    Docker.compose_up()

    print("Waiting for services to finish setting up")
    time.sleep(10)

    print("Checking availability")
    Checks.check_availability("localhost", False)

    print('Updating No-IP record')
    no_ip_r = NoIP.no_ip_update(no_ip_domain, no_ip_cred, "abc@def.com", VERSION)

    print('No-IP update success. Response from No-IP: ', no_ip_r)

    print("Waiting 5 mins for No-IP records update")
    time.sleep(5*60)

    print("Checking availability at the real domain")
    Checks.check_availability(real_domain, True)
