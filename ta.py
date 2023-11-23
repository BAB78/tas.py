from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoTimeoutException, NetmikoAuthenticationException

# Define the router details
router = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': 'cisco',
    'password': 'cisco123!',
}

try:
    # Connect to the router
    print("Connecting to the router...")
    net_connect = ConnectHandler(**router)
    net_connect.enable()
    print("Connection established!")

    # i. Configure Access Control Lists (ACLs)
    acl_commands = [
        'access-list 101 permit tcp host 192.168.1.100 any eq www',
        'access-list 101 permit ip any host 192.168.1.50',
        'interface GigabitEthernet0/1',
        'ip access-group 101 in',
        'ip access-group 101 out',
    ]

    print("Configuring ACLs...")
    output = net_connect.send_config_set(acl_commands)
    print("ACLs configured!")

    # ii. Implement IPSec
    ipsec_commands = [
        'crypto isakmp policy 1',
        'encryption aes',
        'authentication pre-share',
        'group 2',
        'crypto isakmp key strongkey address 0.0.0.0',
        'crypto ipsec transform-set myset esp-aes esp-sha-hmac',
        'crypto map mymap 10 ipsec-isakmp',
        'set peer 192.168.1.50',
        'set transform-set myset',
        'match address 101',  # Use the ACL number defined above
        'interface GigabitEthernet0/1',
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
