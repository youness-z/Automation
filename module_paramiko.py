import paramiko
from paramiko.ssh_exception import *
import time
import re


def check_ip(Ip):
    if type(Ip) != str:
        raise Exception("Check Ip error: Ip is not of expected type")
    else:
        regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        if re.search(regex, Ip):
            print("Valid Ip address")
        else:
            print("Invalid Ip address")

def connect_pass(server_ip, server_port, user, password):
    """
    :param server_ip: ip address of the linux server
    :param server_port: ssh port on the server
    :param user: username
    :param password: password
    :return: ssh_client
    """
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f'Connecting to {server_ip}')
    try:
        ssh_client.connect(hostname=server_ip, port=server_port, username=user, password=password, look_for_keys=False, allow_agent=False)
        return ssh_client
    except AuthenticationException:
        print("Authentication failed for some reason, retry with different credentials")
    except TimeoutError:
        print(f"Connection to {server_ip} took too much time, check rules and retry")


def connect_keys(server_ip, server_port, user, keys):
    """
    :param server_ip: ip address of the linux server
    :param server_port: ssh port on the server
    :param user: username
    :param keys: path to the ssh keys on the local machine
    :return: ssh_client
    """
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f'Connecting to {server_ip}')
    try:
        ssh_client.connect(hostname=server_ip, port=server_port, username=user, key_filename=keys)
        return ssh_client
    except FileNotFoundError:
        raise ("The key file you provided does not exist")
    except BadHostKeyException:
        raise("You provided the wrong ssh key")
    except TimeoutError:
        raise(f"Connection to {server_ip} took too much time, check rules and retry")


def close(ssh_client):
    if ssh_client.get_transport().is_active():
        print('Closing the connection')
        ssh_client.close()


def get_shell(ssh_client):
    """
    :param ssh_client: ssh client
    :return: shell
    """
    return ssh_client.invoke_shell()


def send_command(ssh_client, command, timeout=1):
    """
    :param ssh_client: ssh client
    :param command: command (string)
    :param timeout: timeout, default= 1
    :return: command output
    """
    print(f"Sending the command : {command}")
    stdin, stdout, stderr = ssh_client.exec_command(command)
    time.sleep(timeout)
    return stdin, stdout, stderr


