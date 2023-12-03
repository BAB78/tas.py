from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoTimeoutException
import time

max_retries = 3

router = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': 'cisco',
    'password': 'cisco123!',
    'secret': 'class123!',
    'timeout': 10,  # Adjust timeout as needed
}

retry = 0
while retry < max_retries:
    try:
        print(f"Connection attempt {retry + 1}...")
        net_connect = ConnectHandler(**router)
        net_connect.enable()

        # Configure interfaces with IP addresses
        interface_commands = [
            'interface Loopback0',
            'ip address 10.0.0.1 255.255.255.255',
            'interface GigabitEthernet0/0',
            'ip address 192.168.56.101 255.255.255.0',
        ]
        net_connect.send_config_set(interface_commands)

        # Configure OSPF or other protocols
        ospf_commands = [
            'router ospf 1',
            'network 10.0.0.0 0.255.255.255 area 0',
            'network 192.168.56.0 0.0.0.255 area 0',
        ]
        net_connect.send_config_set(ospf_commands)

        # Configure ACLs
        acl_commands = [
            'access-list 101 permit tcp host 192.168.56.101 any eq www',
            'access-list 101 permit ip any host 192.168.56.30',
            'interface GigabitEthernet0/0',
            'ip access-group 101 in',
            'ip access-group 101 out',
        ]
        net_connect.send_config_set(acl_commands)

        # Configure IPSec
        ipsec_commands = [
            'crypto isakmp policy 1',
            # Add your IPSec configuration here...
        ]
        net_connect.send_config_set(ipsec_commands)

        # Disconnect from the router
        net_connect.disconnect()
        print(f"Connection successful after {retry + 1} attempts!")
        break

    except NetmikoTimeoutException as e:
        print(f"Retry attempt {retry + 1} failed due to timeout. {e}")
        retry += 1
        if retry == max_retries:
            print("Maximum retries exceeded. Script ending.")
        else:
            print("Retrying...")
            time.sleep(5)  # Wait before retrying


Connection attempt 1...
Retry attempt 1 failed due to timeout. Connection to device timed-out: cisco_ios 192.168.56.101:22
Retrying...
Connection attempt 2...
Retry attempt 2 failed due to timeout. Connection to device timed-out: cisco_ios 192.168.56.101:22
Retrying...
Connection attempt 3...
Retry attempt 3 failed due to timeout. Connection to device timed-out: cisco_ios 192.168.56.101:22
Maximum retries exceeded. Script ending.
