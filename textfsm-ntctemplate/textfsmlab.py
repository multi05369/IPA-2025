from netmiko import ConnectHandler
from pprint import pprint
from pathlib import Path
import re
from typing import List, Dict, Any


def get_base_device_params(ip: str, username: str = "WINDOWS", password: str = "cisco") -> Dict[str, Any]:
    """Get the base device parameters for connection."""
    return {
        "device_type": "cisco_ios",
        "ip": ip,
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


def execute_cisco_command(ip: str, command: str, username: str = "WINDOWS", password: str = "cisco", use_textfsm: bool = True):
    """Execute a command on a Cisco device and return the result."""
    
    print(f"Connecting to {ip}...")
    device_params = get_base_device_params(ip, username, password)
    
    with ConnectHandler(**device_params) as ssh:
        ssh.enable()
        print(f"Connected to {ip}")
        result = ssh.send_command(command, use_textfsm=use_textfsm)
        print(f"Finished configuration for {ip}")
        return result


def connectDevice(ip: str, username="WINDOWS", password="cisco", command=None):
    if command is None:
        command = input("Input your command (the command about showing not config): ")
    
    result = execute_cisco_command(ip, command, username, password)
    
    print(f"\nParsed Output for '{command}' on {ip}:")
    for itef in result:
        print(itef["description"])


def queriesDes(ip: str, username="WINDOWS", password="cisco", command="show interface description"):
    if command is None:
        command = input("Input your command (the command about showing not config): ")
    
    result = execute_cisco_command(ip, command, username, password)
    
    all_des = []
    for itef in result:
        status = itef.get("status", "")

        if re.fullmatch(r"up", status):
            data = {
                "description": itef.get("description", ""),
                "port": itef.get("port", ""),
                "status": status
            }
            all_des.append(data)

    return all_des


def seeNeighbor(ip: str, username="WINDOWS", password="cisco", command="show cdp neighbors"):
    if command is None:
        command = input("Input your command (the command about showing not config): ")
    
    result = execute_cisco_command(ip, command, username, password)
    
    # print(f"\nParsed Output for '{command}' on {ip}:")
    # pprint(result)
    all_neighbors = []
    for itef in result:
        all_neighbors.append({
            "local_interface": itef["local_interface"],
            "neighbor_interface": itef["neighbor_interface"],
            "neighbor_name": itef["neighbor_name"]
        })
    
    return all_neighbors

def execute_config_commands(ip: str, commands: List[str], username: str = "WINDOWS", password: str = "cisco"):
    """Send configuration commands to a Cisco device."""
    
    print(f"Connecting to {ip} to send config commands...")
    device_params = get_base_device_params(ip, username, password)

    with ConnectHandler(**device_params) as ssh:
        ssh.enable()
        print(f"Connected to {ip}")
        output = ssh.send_config_set(commands)
        print(f"Configuration complete on {ip}")
        return output


def main():
    """main function"""
    command_set = [
        "int g0/0",
        "desc Connect to Gig 0/1 of S0.ipa.com",
        "int g0/2",
        "desc Connect to Gig 0/2 of R2.ipa.com",
        "int g0/1",
        "desc Connect to PC",
    ]
    print(execute_config_commands("172.31.18.4", command_set))
    command_set = [
        "int g0/0",
        "desc Connect to Gig 0/2 of S0.ipa.com",
        "int g0/1",
        "desc Connect to Gig 0/2 of R1.ipa.com",
        "int g0/2",
        "desc Connect to Gig 0/1 of S1.ipa.com",
        "int g0/3",
        "desc Connect to WAN",
    ]
    print(execute_config_commands("172.31.18.5", command_set))
    
    command_set = [
        "int g0/0",
        "desc Connect to Gig 0/3 of S0.ipa.com",
        "int g1/1",
        "desc Connect to PC",
        "int g0/1",
        "desc Connect to Gig 0/2 of R2.ipa.com"
    ]
    print(execute_config_commands("172.31.18.3", command_set))

main()