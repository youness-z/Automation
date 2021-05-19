import paramiko
import time
from paramiko import *
#from paramiko.ssh_exception import AuthenticationException

linux_server = {'hostname': '20.188.61.107', 'port': 22, 'username': 'youness',
                   'key_filename': 'C:/Users/youness.zarhali/PycharmProjects/Automation/.ssh/id_ed25519'}
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Accept the host key
print(f'Connecting to {linux_server["hostname"]}')
try:
    ssh_client.connect(**linux_server)
except AuthenticationException as e:
    print("Authentication failed for some reason, retry with different credentials")
except TimeoutError as e:
    print(" the connected party took too long to connect")
else:
    stdin, stdout, stderr = ssh_client.exec_command('ifconfig')
    output = stdout.read()
    time.sleep(1)

    print(output.decode('utf-8'))


if ssh_client.get_transport().is_active():
    print(f"Closing connection to {linux_server['hostname']}")
    ssh_client.close()


