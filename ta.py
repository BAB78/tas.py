from netmiko import ConnectHandler

# Define the router details
router = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': 'cisco',
    'password': 'cisco123!',
    'secret': 'class123!',
}

# Connect to the router
print("Connecting to the router...")
net_connect = ConnectHandler(**router)
net_connect.enable()
print("Connection established!")

# Configure interfaces with IP addresses
interface_commands = [
    'interface Loopback0',
    'ip address 10.0.0.1 255.255.255.255',
    'interface GigabitEthernet0/0',
    'ip address 192.168.56.101 255.255.255.0',
]

print("Configuring interfaces...")
net_connect.send_config_set(interface_commands)
print("Interfaces configured!")

# Configure OSPF
ospf_commands = [
    'router ospf 1',
    'network 10.0.0.0 0.255.255.255 area 0',
    'network 192.168.56.0 0.0.0.255 area 0',
]

print("Configuring OSPF...")
net_connect.send_config_set(ospf_commands)
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
net_connect.send_config_set(acl_commands)
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
net_connect.send_config_set(ipsec_commands)
print("IPSec configured!")

# Disconnect from the router
print("Disconnecting from the router...")
net_connect.disconnect()
print("Disconnected!")
