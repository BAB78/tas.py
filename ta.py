import os
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoTimeoutException

max_retries = 3
debug = False

router = {
    "device_type": "cisco_ios",
    "ip": "192.168.56.101",
    "username": "cisco",
    "password": "cisco123!",
    "secret": "class123!",
    "verbose": debug,
}

print(f"Pinging {router['ip']}...")
response = os.system(f"ping {router['ip']} -c 2")
if response != 0:
    print(f"{router['ip']} is unreachable. Please check connectivity.")
    exit()

retry = 0
while retry < max_retries:
    try:
        print(f"Connection attempt {retry + 1}...")
        net_connect = ConnectHandler(**router)
        net_connect.enable()

        interface_commands = [
            "interface Loopback0",
            "ip address 10.0.0.1 255.255.255.255",
            "interface GigabitEthernet0/0",
            "ip address 192.168.56.101 255.255.255.0",
        ]

        print("Configuring interfaces...")
        net_connect.send_config_set(interface_commands)

        # Similar config commands...

        print("Disconnecting...")
        net_connect.disconnect()
        print(f"Connection successful after {retry + 1} attempts!")
        break

    except NetmikoTimeoutException as e:
        print(f"Retry attempt {retry + 1} failed due to timeout. {e}")
        retry += 1

if retry == max_retries:
    print("Maximum retries exceeded. Script ending.")
