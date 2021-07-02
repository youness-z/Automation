import paramiko
from paramiko.ssh_exception import *
import time
import re


def check_ip(ip):
    if type(ip) != str:
        raise Exception("Check Ip type error: The provided ip is not of type string")
    else:
        regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        if re.search(regex, ip):
            print("Valid Ip address")
        else:
            print("Invalid Ip address")


class Connection:
    def __init__(self, server_ip, server_port, user, ssh_client):
        self.server_ip = server_ip
        self.server_port = server_port
        self.user = user
        self.ssh_client = ssh_client

    def connect_pass(self, password):
        """
        :param password: required password the connect to the server
        :return: returning the ssh client (password authentication case)
        """
        print(f'Connecting to {self.server_ip}')
        try:
            self.ssh_client.connect(hostname=self.server_ip, port=self.server_port, username=self.user,
                                    password=password, look_for_keys=False, allow_agent=False)
            return self.ssh_client
        except AuthenticationException:
            print("Authentication failed for some reason, retry with different credentials")
        except TimeoutError:
            print(f"Connection to {self.server_ip} took too much time, check rules and retry")

    def connect_keys(self, keys):
        """
        :param keys:
        :return: returning the ssh client (key authentication case)
        """
        print(f'Connecting to {self.server_ip}')
        try:
            self.ssh_client.connect(hostname=self.server_ip, port=self.server_port, username=self.user, key_filename=keys)
            return self.ssh_client
        except FileNotFoundError:
            raise ("The ssh key file you provided does not exist")
        except BadHostKeyException:
            raise("You provided the wrong ssh key")
        except TimeoutError:
            raise(f"Connection to {self.server_ip} took too much time, check rules and retry")


class SshClient:
    def __init__(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def close(self):
        """
        Closing the ssh connection
        """
        if self.ssh_client.get_transport().is_active():
            print('Closing the connection')
            self.ssh_client.close()
        pass

    def get_shell(self):
        """
        :param ssh_client: ssh client
        :return: shell
        """
        return self.ssh_client.invoke_shell()

    def send_command(self, command, timeout=1):
        """
        :param ssh_client: ssh client
        :param command: command (string)
        :param timeout: timeout, default= 1
        :return: command output
        """
        print(f"Sending the command : {command}")
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        time.sleep(timeout)
        return stdin, stdout, stderr


#Object1 = SshClient()
#Object2 = Connection()
#print(type(Object1.close()))
#print(type(Object1.get_shell()))
#print(type(Object1.send_command('ifconfig')))

