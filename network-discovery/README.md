# 🗺️ Network Topology Discovery Script

A Useful Python script that automatically discovers and maps your Cisco network topology. Using Netmiko for device connections and TextFSM for parsing, this tool scans your network via CDP (Cisco Discovery Protocol) and generates both a detailed command-line summary and a professional visual diagram (Optional).

## ✨ Features

* **Automated Discovery**: Connects to a list of seed devices and recursively finds all connected neighbors.
* **Detailed Terminal Output**: Prints a clean, readable list of all discovered devices and their specific interface-to-interface connections.
* **Visual Diagram Generation**: Automatically creates a `.dot` file compatible with Graphviz to generate high-quality PNG or SVG topology maps.
* **Secure Connection**: Uses SSH with private key authentication to connect to devices.

## Sample Output
```bash
Starting topology discovery...

[+] Querying device: R0 (172.31.4.1)
    - Found 2 neighbor(s).
      - Discovered link: R0 (GigabitEthernet0/0) <--> KMITL-IT-LAB-9200L-STACK (GigabitEthernet1/0/24)
      - Discovered link: R0 (GigabitEthernet0/1) <--> S0 (GigabitEthernet0/0)

[+] Querying device: R1 (172.31.4.6)
    - Found 2 neighbor(s).
      - Discovered link: R1 (GigabitEthernet0/2) <--> R2 (GigabitEthernet0/1)
      - Discovered link: R1 (GigabitEthernet0/0) <--> S0 (GigabitEthernet0/1)

[+] Querying device: R2 (172.31.4.9)
    - Found 3 neighbor(s).
      - Discovered link: R2 (GigabitEthernet0/1) <--> R1 (GigabitEthernet0/2)
      - Discovered link: R2 (GigabitEthernet0/0) <--> S0 (GigabitEthernet0/2)
      - Discovered link: R2 (GigabitEthernet0/2) <--> S1 (GigabitEthernet0/1)

[+] Querying device: S0 (172.31.4.2)
    - Found 4 neighbor(s).
      - Discovered link: S0 (GigabitEthernet0/2) <--> R2 (GigabitEthernet0/0)
      - Discovered link: S0 (GigabitEthernet0/1) <--> R1 (GigabitEthernet0/0)
      - Discovered link: S0 (GigabitEthernet0/3) <--> S1 (GigabitEthernet0/0)
      - Discovered link: S0 (GigabitEthernet0/0) <--> R0 (GigabitEthernet0/1)

[+] Querying device: S1 (172.31.4.3)
    - Found 2 neighbor(s).
      - Discovered link: S1 (GigabitEthernet0/1) <--> R2 (GigabitEthernet0/2)
      - Discovered link: S1 (GigabitEthernet0/0) <--> S0 (GigabitEthernet0/3)

============================================================
                Detailed Network Topology Results
============================================================

[DEVICES DISCOVERED (Nodes)]
  - KMITL-IT-LAB-9200L-STACK
  - R0
  - R1
  - R2
  - S0
  - S1

[CONNECTIONS (Edges)]
  - KMITL-IT-LAB-9200L-STACK (GigabitEthernet1/0/24) <------> R0 (GigabitEthernet0/0  )
  - R0 (GigabitEthernet0/0  ) <------> S0 (GigabitEthernet0/1  )
  - R1 (GigabitEthernet0/1  ) <------> R2 (GigabitEthernet0/2  )
  - R2 (GigabitEthernet0/1  ) <------> S1 (GigabitEthernet0/2  )
  - R1 (GigabitEthernet0/0  ) <------> S0 (GigabitEthernet0/1  )
  - R2 (GigabitEthernet0/0  ) <------> S0 (GigabitEthernet0/2  )
  - S0 (GigabitEthernet0/0  ) <------> S1 (GigabitEthernet0/3  )

============================================================

[🏁] Topology discovery complete.
```

-->


## 🛠️ Usage Guide (For Windows)

Follow these steps to get the script up and running.

### 1. Prerequisites

* **Python 3.x**: Ensure Python is installed and added to your PATH.
* **Git**: To clone the repository.
* **SSH Access**: You must have SSH key-based access configured for your network devices.

### 2. Setup and Configuration

**Step 1: Get the Code**
Clone the repository and navigate into the project directory.

**Step 2: Install Dependencies**
Activate your Python virtual environment (`venv`). Then, run the following command to install all required packages:

```bash
venv\Scripts\activate

pip install -r requirements.txt
```

**Step 3: Configure Script Variables**
Open the display-connection.py file and edit the following variables to match your environment:

`PRIVATE_KEY` (`line 10`): Update this with the absolute path to your SSH private key.

```bash
# Example PRIVATE_KEY = "C:/Users/LAB306_XX/.ssh/id_rsa"
```

`DEVICES` (`line 51`): Update this dict with the hostnames and IP addresses of your devices.  The script will start its discovery from here.


**Step 4: Set Environment Variable**
This script relies on ntc-templates to parse command output. You must set an environment variable pointing to the templates directory. Open PowerShell and run this command, replacing {YourPath} with the absolute path to your project's venv folder.

Note: This command sets the variable for the current PowerShell session only. You will need to run it again if you open a new terminal.

```bash
$env:NET_TEXTFSM = "{YourPath}\ntc_templates\templates" 
# change {YourPath} to your own path"
```

**Run the Discovery**
Once configured, execute the script from your terminal:

The script will connect to your devices and print the discovered topology directly to the terminal.

```bash
python .\display-connection.py
```

## Optional: Visualizing the Topology with Graphviz
To generate a visual diagram, follow these additional steps.

**Step 1: Install Graphviz**

- Download the Graphviz installer from the official website: https://graphviz.org/download/

- During installation, it is critical that you check the box labeled "Add Graphviz to the system PATH for all users". This is required to run the diagram generation command.

**Step 2: Enable Graphviz Output in the Script**

- Open `display-connection.py` and find the `main()` function at the bottom.

- Uncomment the line that calls `generate_graphviz_file` and the `print` statements that follow it.

```python
# Change this:
# generate_graphviz_file(discovered_topology)
# print("\nNEXT STEP: ...")

# To this:
generate_graphviz_file(discovered_topology)
print("\nNEXT STEP: To create a visual diagram, run this command in your terminal:")
print("dot -Tpng topology.dot -o topology.png")
```

**Step 3: Generate the Diagram**

- Run the Python script again: python .\display-connection.py

- This time, it will create a topology.dot file.

- In your terminal, run the following command to convert the .dot file into a PNG image:

```bash
dot -Tpng topology.dot -o topology.png
```

A `topology.png file` containing your network map will be created in the project folder.
