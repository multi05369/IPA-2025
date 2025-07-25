"""Example of Netmiko with re (regex)"""

from netmiko import ConnectHandler
import time
from pathlib import Path
import re

def matchRegex(output : str, reg=None):
    '''Use out put from network device to find the match'''
    temp = output.split("\n")
    output = temp
    ans = []
    if reg is None:
        reg = input("Input your pattern that want to search: ")
    for itef in output:
        match = re.search(reg, itef)
        if match:
            ans.append(match.groups())
    return ans
    

def connectDevice(ip : str, username="WINDOWS", password="cisco", command=None):
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

    #rendered_config = makeCommand(tFile, vFile)
    if command is None:
        command = input("Input you command if command is about show put do first: ")
    command_set = str(command)
    # [line.strip() for line in rendered_config.strip().split('\n') if line.strip()]

    with ConnectHandler(**device_params) as ssh:
        ssh.enable()
        print(f"Connected to {ip}")
        result = ssh.send_config_set(command_set)
        temp = matchRegex(result)
        result = temp
        print(f"Configuration result for {ip}:\n{result}")
        time.sleep(2)
        print(f"Finished configuration for {ip}")

