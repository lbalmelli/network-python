import threading
import paramiko
import subprocess
import sys

def ssh_command( ip, user , passwd, command):
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(ip,username = user, password = passwd)
	ssh_session = client.get_transport().open_session()
	if ssh_session.active:
		ssh_session.exec_command(command)
		print ssh_session.recv(1024)
	return

if len(sys.argv)>4:
	print("Connection set-up")
	print("target: %s" % sys.argv[1])
	print("username: %s" % sys.argv[2])
	print("password: %s" %sys.argv[3])
	print("command: %s"%sys.argv[4])

	ssh_command(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])

else:
	print("Error: not enough arguments!")
	print("format: %s target_up username password command"% sys.argv[0])
	print("Example: %s 192.168.1.94 user password 'ip addr show'"% sys.argv[0])
