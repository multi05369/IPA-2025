"""Example how to use Pramiko"""

import time
import paramiko

username = "admin" # DEVASC if use VM
password = "your_password_here"  # Replace with your actual password

# Work better in Linux

device_ip = ["ip1", "ip2", "ip3"]  # Replace with actual device IPs

for ip in device_ip:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip)
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
