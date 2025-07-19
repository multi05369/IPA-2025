"""Example how to use Pramiko Version Windows"""

import time
import paramiko
from pathlib import Path

username = "username"
password = "supersecret"
key_path = str(Path.home() / ".ssh" / "id_rsa")
private_key = paramiko.RSAKey.from_private_key_file(key_path)

device_ip = ["your ip"]

for ip in device_ip:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
    hostname=ip,
    username=username,
    pkey=private_key,
    look_for_keys=False,
    allow_agent=False,
    disabled_algorithms=dict(
        pubkeys=["rsa-sha2-256", "rsa-sha2-512"],
        kex=[
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
        hostkeys=["ssh-ed25519", "ecdsa-sha2-nistp256", "ecdsa-sha2-nistp384", "ecdsa-sha2-nistp521"],
        ),
    )
    print(f"Connected to {ip}")
    with client.invoke_shell() as ssh:
        print("Conntected to {}".format(ip))
        ssh.send("terminal length 0\n")
        time.sleep(1)
        result = ssh.recv(1000).decode("ascii")
        print(result)

        ssh.send("enable\n")
        time.sleep(1)
        result = ssh.recv(1000).decode("ascii")
        print(result)

        ssh.send(f"{password}\n")
        time.sleep(1)
        result = ssh.recv(1000).decode("ascii")
        print(result)

        ssh.send("sho ip int br\n")
        time.sleep(1)
        result = ssh.recv(1000).decode("ascii")
        print(result)
