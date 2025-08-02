import os
import networkx as nx
from netmiko import ConnectHandler
from textfsm import clitable
import getpass

# --- Configuration and Constants ---

USERNAME = "admin"
PRIVATE_KEY = "C:/Users/LAB306_XX/.ssh/id_rsa" # IMPORTANT: Update this path to your own path

# Set the path to your ntc-templates directory
# use this command with your ntc-template path to set path to your ntc-templates directory
# $env:NET_TEXTFSM = "{YourPath}\ntc_templates\templates" change {YourPath} to your own path
if "NET_TEXTFSM" not in os.environ:
    print("Error: The NET_TEXTFSM environment variable is not set.")
    print("Please set it to the path of your ntc_templates/templates directory.")
    exit()

# Base connection parameters for Netmiko
BASE_PARAMS = {
    "device_type": "cisco_ios",
    "username": USERNAME,
    "use_keys": True,
    "key_file": PRIVATE_KEY,
    "allow_agent": False,
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
}

# Dictionary of devices to connect to 
DEVICES = {
    # "R0": "172.31.4.1",
    # "R1": "172.31.4.6",
    # "R2": "172.31.4.9",
    # "S0": "172.31.4.2",
    # "S1": "172.31.4.3"
}

# --- Helper Functions ---

def connect(ip):
    """Establishes a Netmiko connection to a device."""
    params = BASE_PARAMS.copy()
    params["ip"] = ip
    try:
        return ConnectHandler(**params)
    except Exception as e:
        print(f"Failed to connect to {ip}: {e}")
        return None

def parse_cdp(output: str):
    """Parses 'show cdp neighbors' output using TextFSM."""
    cli_table = clitable.CliTable(
        "index",
        os.environ.get("NET_TEXTFSM")
    )
    attributes = {
        "Command": "show cdp neighbors detail", # Using detail to ensure we get all data
        "Platform": "cisco_ios"
    }
    cli_table.ParseCmd(output, attributes)
    result = [dict(zip(cli_table.header, row)) for row in cli_table]
    return result

# --- Main Logic ---

def generate_topology(devices_dict):
    """
    Connects to each device, gathers CDP data, and builds a network graph.
    """
    topology_graph = nx.Graph()
    
    print("Starting topology discovery...")

    for device_name, ip in devices_dict.items():
        print(f"\n[+] Querying device: {device_name} ({ip})")
        
        topology_graph.add_node(device_name)

        conn = connect(ip)
        if not conn:
            continue

        try:
            conn.enable()
            # FEATURE: Using 'show cdp neighbors detail' to get more reliable interface info
            cdp_output = conn.send_command("show cdp neighbors detail", use_textfsm=False)
            conn.disconnect()

            cdp_entries = parse_cdp(cdp_output)

            if not cdp_entries:
                print(f"    - No CDP neighbors found on {device_name}.")
                continue
            
            print(f"    - Found {len(cdp_entries)} neighbor(s).")
            for entry in cdp_entries:
                local_device = device_name
                remote_device = entry["NEIGHBOR_NAME"].split('.')[0]
                
                # FEATURE: Capture local and remote interface details
                local_interface = entry["LOCAL_INTERFACE"]
                remote_interface = entry["NEIGHBOR_INTERFACE"]

                # Add the connection with interface details as attributes
                topology_graph.add_edge(
                    local_device, 
                    remote_device, 
                    local_int=local_interface, 
                    remote_int=remote_interface
                )
                print(f"      - Discovered link: {local_device} ({local_interface}) <--> {remote_device} ({remote_interface})")

        except Exception as e:
            print(f"    - An error occurred with {device_name}: {e}")
            if conn:
                conn.disconnect()

    return topology_graph

def display_topology(graph):
    """
    Prints the detailed network topology to the terminal.
    """
    print("\n" + "="*60)
    print("                Detailed Network Topology Results")
    print("="*60)

    if not graph.nodes():
        print("No devices were discovered.")
        return

    print("\n[DEVICES DISCOVERED (Nodes)]")
    for node in sorted(graph.nodes()):
        print(f"  - {node}")

    print("\n[CONNECTIONS (Edges)]")
    if not graph.edges():
        print("  - No connections were discovered.")
    else:
        # FEATURE: Access edge data to print interface details
        for u, v, data in sorted(graph.edges(data=True)):
            local_int = data.get('local_int', 'N/A')
            remote_int = data.get('remote_int', 'N/A')
            # Ensure consistent ordering for display
            if u > v:
                u, v = v, u
                local_int, remote_int = remote_int, local_int
            print(f"  - {u:<2} ({local_int:<20}) <------> {v:>2} ({remote_int:<20})")
            
    print("\n" + "="*60)

# FEATURE: New function to generate a Graphviz .dot file
def generate_graphviz_file(graph, filename="topology.dot"):
    """
    Generates a .dot file for visualization with Graphviz.
    """
    print(f"\n[+] Generating Graphviz file: {filename}")
    with open(filename, "w") as f:
        f.write("graph NetworkTopology {\n")
        f.write("    // Graph attributes\n")
        f.write("    graph [fontname=Helvetica, fontsize=10];\n")
        f.write("    node [shape=box, style=rounded, fontname=Helvetica, fontsize=10];\n")
        f.write("    edge [fontname=Helvetica, fontsize=8];\n\n")
        
        f.write("    // Nodes (Devices)\n")
        for node in sorted(graph.nodes()):
            f.write(f'    "{node}";\n')
        
        f.write("\n    // Edges (Connections)\n")
        for u, v, data in graph.edges(data=True):
            local_int = data.get('local_int', '').replace('GigabitEthernet', 'Gi')
            remote_int = data.get('remote_int', '').replace('GigabitEthernet', 'Gi')
            
            # Create a label for the connection line
            label = f"{local_int} - {remote_int}"
            f.write(f'    "{u}" -- "{v}" [label="{label}"];\n')
            
        f.write("}\n")
    print(f"    - Success! File '{filename}' created.")

# --- Main Execution Block ---

def main():
    # 1. Generate the topology by connecting to devices
    discovered_topology = generate_topology(DEVICES)
    
    # 2. Display the detailed results in the terminal
    display_topology(discovered_topology)
    
    # 3. Generate the .dot file for visualization
    # generate_graphviz_file(discovered_topology)
    
    print("\n[🏁] Topology discovery complete.")
    # print("\nNEXT STEP: To create a visual diagram, run this command in your terminal:")
    # print("dot -Tpng topology.dot -o topology.png")
main()
