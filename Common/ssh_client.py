import os

import paramiko
from scp import SCPClient


class SSh:

    def __init__(self, hostname, port, username):
        self._hostname = hostname
        self._port = port
        self._username = username
        _ssh = paramiko.SSHClient()
        _ssh.load_system_host_keys()
        _ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        _ssh.connect(self._hostname, self._port, username=self._username, look_for_keys=False)
        self.ssh = _ssh

    def scp_put_files(self, file, destination_volume):
        ssh = self.ssh
        with SCPClient(ssh.get_transport()) as scp:
            scp.put(file, recursive=True, remote_path=destination_volume)

    def run_jar(self, destination_volume, application, params=None):
        ssh = self.ssh
        if params is not None:
            comand = f'cd {destination_volume} && sudo java -jar {application} {params}'
        else:
            comand = f'cd {destination_volume} && sudo java -jar {application}'
        stdin, stdout, stderr = ssh.exec_command(comand)
        print("stderr: ", stderr.readlines())
        print("pwd: ", stdout.readlines())

