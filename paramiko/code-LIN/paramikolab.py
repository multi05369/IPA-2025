"""Example how to use Pramiko Version Linux"""

import time
import paramiko

username = "username"
password = "supersecret"

device_ip = ["your ip"]

for ip in device_ip:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username=username, look_for_keys=True)
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
