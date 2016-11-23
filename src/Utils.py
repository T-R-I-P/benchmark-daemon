"""
Utils for benchmark-daemon

@author FATESAIKOU
"""

from tensorflow.python.client import device_lib

import time
import subprocess
import pprint
import thread


def getDeviceList():
	device_ids = [ device.name for device in device_lib.list_local_devices()]

	return device_ids

def getPerformance(benchmark_src):
	sh_command = "cat | python 2>/dev/null | grep 'It cost' | awk '{print $3}'"
	proc = subprocess.Popen(sh_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	proc.stdin.write(benchmark_src)
	proc.stdin.close()
	execute_time = float(proc.stdout.read())

	return execute_time

def requestMsg(send_msg, wait_msg, sock, recive_size):
	counter = 0
	while True:
		counter += 1
		sock.send(send_msg)
		msg = sock.recv(recive_size)

		if msg == wait_msg or wait_msg == None or counter > 10:
			break

	return msg

def responseMsg(send_msg, wait_msg, sock, recive_size):
	counter = 0
	while True:
		counter += 1
		msg = sock.recv(recive_size)

		if msg == wait_msg or wait_msg == None or counter > 10:
			break
		else:
			sock.send("Resend")

	sock.send(send_msg)
	return msg
