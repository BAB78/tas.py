from socket import error
import paramiko
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoTimeoutException, NetmikoAuthenticationException

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh_client.connect(hostname='192.168.56.101', username='cisco', password='cisco123!')
    print("Connected!")
    ssh_client.close()

    # Define the router details
    router = {
        'device_type': 'cisco_ios',
        'ip': '192.168.56.101',
        'username': 'cisco',
        'password': 'cisco123!',
        'secret': 'class123!',
        'port': 22,  # Specify the SSH port if it's different from the default (22)
        'timeout': 120,  # Adjust timeout as needed
    }

    try:
        # Connect to the router
        print("Connecting to the router...")
        net_connect = ConnectHandler(**router)
        net_connect.enable()
        print("Connection established!")

        # Configuration steps...

        # Configure interfaces with IP addresses
        interface_commands = [
            'interface Loopback0',
            'ip address 10.0.0.1 255.255.255.255',
        ]

        print("Configuring interfaces...")
        output = net_connect.send_config_set(interface_commands)
        print("Interfaces configured!")

        # Configure OSPF
        ospf_commands = [
            'router ospf 1',
            'network 10.0.0.0 255.255.255 area 0',
            'network 192.168.56.0 0.0.0.255 area 0',
        ]

        print("Configuring OSPF...")
        output = net_connect.send_config_set(ospf_commands)
        print("OSPF configured!")

        # Configure ACLs
        acl_commands = [
            'access-list 101 permit tcp host 192.168.56.101 any eq www',
            'access-list 101 permit ip any host 192.168.56.30',
            'interface GigabitEthernet0/0',
            'ip access-group 101 in',
            'ip access-group 101 out',
        ]

        print("Configuring ACLs...")
        output = net_connect.send_config_set(acl_commands)
        print("ACLs configured!")

        # Configure IPSec
        ipsec_commands = [
            'crypto isakmp policy 1',
            'encryption aes',
            'authentication pre-share',
            'group 2',
            'crypto isakmp key your_shared_key address 0.0.0.0',
            'crypto ipsec transform-set myset esp-aes esp-sha-hmac',
            'crypto map mymap 10 ipsec-isakmp',
            'set peer 192.168.56.30',
            'set transform-set myset',
            'match address 101',  # Use the ACL number defined in acl_commands
            'interface GigabitEthernet0/0',
            'crypto map mymap',
        ]

        print("Configuring IPSec...")
        output = net_connect.send_config_set(ipsec_commands)
        print("IPSec configured!")

        # Disconnect from the router
        print("Disconnecting from the router...")
        net_connect.disconnect()
        print("Disconnected!")

    except NetmikoAuthenticationException as auth_error:
        print(f"Authentication failed: {auth_error}")

    except NetmikoTimeoutException as timeout_error:
        print(f"Connection to device timed out: {timeout_error}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

except error as e:
    print(f"Socket error occurred: {str(e)}")
