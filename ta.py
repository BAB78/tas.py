Connection timed out: Connection to device timed-out: cisco_ios 192.168.56.101:22

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoTimeoutException

# Define the router details
router = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': 'cisco',
    'password': 'cisco123!',
    'secret': 'class123!',
    'timeout': 30,  # Set a higher timeout value (e.g., 30 seconds)
}

try:
    # Connect to the router
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

    # Configure OSPF
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

except NetmikoTimeoutException as timeout_error:
    print(f"Connection timed out: {timeout_error}")
