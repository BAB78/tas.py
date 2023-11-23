from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoTimeoutException, NetmikoAuthenticationException

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

    # If the connection is successful, proceed with configuration
    print("Successfully connected to the device.")

    # Perform your device configurations here...

    # Disconnect from the router after configurations
    net_connect.disconnect()
    print("Disconnected from the device.")

except NetmikoAuthenticationException as auth_error:
    print(f"Authentication failed: {auth_error}")

except NetmikoTimeoutException as timeout_error:
    print(f"Connection timed out: {timeout_error}")

except Exception as e:
    print(f"An error occurred: {str(e)}")
