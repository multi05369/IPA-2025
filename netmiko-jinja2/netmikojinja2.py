"""Example of Netmiko with Jinja2"""

from jinja2 import Environment, FileSystemLoader
import yaml
from netmiko import ConnectHandler
import time
from pathlib import Path

def makeCommand(tFile=None, vFile=None):
    '''Input template and data file to create command'''
    if tFile is None:
        tFile = input("Input Your template file (that in templates folder): ")
    if vFile is None:
        vFile = input("Input Your data file (that in data_file folder): ")

    template_dir = "../templates"
    template_file = str(tFile)
    vars_file = "../data_file/" + str(vFile)

    env = Environment(
        loader=FileSystemLoader(template_dir),
        trim_blocks=True,
        lstrip_blocks=True
    )
    template = env.get_template(template_file)

    with open(vars_file) as f:
        vars_dict = yaml.safe_load(f)
    return template.render(vars_dict)

def connectDevice(ip : str, username="WINDOWS", password="cisco"):
    '''Connect to Cisco device with IP, username and password (you can choose your username and password)'''
    BASE_DEVICE_PARAMS = {
        "device_type": "cisco_ios",
        "username": username,
        "secret": password,
        "use_keys": True,
        "key_file": str(Path.home() / ".ssh" / "id_rsa"),
        "disabled_algorithms": {
            "pubkeys": ["rsa-sha2-256", "rsa-sha2-512"],
            "kex": [
                "diffie-hellman-group1-sha1",
                "diffie-hellman-group14-sha256",
                "diffie-hellman-group16-sha512",
                "diffie-hellman-group18-sha512",
                "diffie-hellman-group-exchange-sha256",
                "ecdh-sha2-nistp256",
                "ecdh-sha2-nistp384",
                "ecdh-sha2-nistp521",
                "curve25519-sha256",
                "curve25519-sha256@libssh.org",
            ],
            "hostkeys": [
                "ssh-ed25519",
                "ecdsa-sha2-nistp256",
                "ecdsa-sha2-nistp384",
                "ecdsa-sha2-nistp521",
            ],
        },
        "allow_agent": False
    }

    print(f"Connecting to {ip}...")

    device_params = BASE_DEVICE_PARAMS.copy()
    device_params["ip"] = ip

    rendered_config = makeCommand()
    command_set = [line.strip() for line in rendered_config.strip().split('\n') if line.strip()]

    with ConnectHandler(**device_params) as ssh:
        ssh.enable()
        print(f"Connected to {ip}")
        result = ssh.send_config_set(command_set)
        print(f"Configuration result for {ip}:\n{result}")
        time.sleep(2)
        print(f"Finished configuration for {ip}")

# connectDevice("172.31.18.3")
print(makeCommand())