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
output = net_connect = ConnectHandler(**router)
output = net_connect.enable()
print("Connection established!")

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
output =  net_connect.send_config_set(acl_commands)
print(output)

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
print(output)

# Disconnect from the router
print("Disconnecting from the router...")
output = net_connect.disconnect()
print("Disconnected!")


error message 
Connecting to the router...
Traceback (most recent call last):
  File "/home/devasc/.local/lib/python3.8/site-packages/netmiko/base_connection.py", line 899, in establish_connection
    self.remote_conn_pre.connect(**ssh_connect_params)
  File "/home/devasc/.local/lib/python3.8/site-packages/paramiko/client.py", line 368, in connect
    raise NoValidConnectionsError(errors)
paramiko.ssh_exception.NoValidConnectionsError: [Errno None] Unable to connect to port 22 on 192.168.56.101

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/devasc/labs/prne/task.py", line 14, in <module>
    output = net_connect = ConnectHandler(**router)
  File "/home/devasc/.local/lib/python3.8/site-packages/netmiko/ssh_dispatcher.py", line 266, in ConnectHandler
    return ConnectionClass(*args, **kwargs)
  File "/home/devasc/.local/lib/python3.8/site-packages/netmiko/base_connection.py", line 327, in __init__
    self._open()
  File "/home/devasc/.local/lib/python3.8/site-packages/netmiko/base_connection.py", line 332, in _open
    self.establish_connection()
  File "/home/devasc/.local/lib/python3.8/site-packages/netmiko/base_connection.py", line 905, in establish_connection
    raise NetmikoTimeoutException(msg)
netmiko.ssh_exception.NetmikoTimeoutException: Connection to device timed-out: cisco_ios 192.168.56.101:22
