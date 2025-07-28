from netmiko import ConnectHandler
from pprint import pprint
from pathlib import Path

def connectDevice(ip: str, username="WINDOWS", password="cisco", command=None):
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

    if command is None:
        command = input("Input your command (the command about showing not config): ")
    
    with ConnectHandler(**device_params) as ssh:
        ssh.enable()
        print(f"Connected to {ip}")
        result = ssh.send_command(command, use_textfsm=True)
        print(f"\nParsed Output for '{command}' on {ip}:")
        pprint(result)

        print(f"\nFinished configuration for {ip}")

# Example call
connectDevice("172.31.18.4")
