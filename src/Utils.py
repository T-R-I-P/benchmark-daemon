"""
Utils for benchmark-daemon

@author FATESAIKOU
"""

import time
import subprocess
import pprint
import thread
import json


def getDeviceList():
	sh_command = "../scripts/getDeviceList.py 2>/dev/null"
	device_ids = json.loads(subprocess.check_output(sh_command, shell=True))

	print("[GET] DEVICE_LIST: " + json.dumps(device_ids))

	return device_ids

def getPerformance(benchmark_src):
	sh_command = "cat | python 2>/dev/null | grep 'It cost' | awk '{print $3}'"
	proc = subprocess.Popen(sh_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	proc.stdin.write(benchmark_src)
	proc.stdin.close()
	execute_time = float(proc.stdout.read())
	
	print("[GET] PERFORMANCE: " + str(execute_time) + " sec")

	return execute_time

def requestMsg(send_msg, wait_msg, sock, recive_size):
	while True:
		sock.send(send_msg)
		msg = sock.recv(recive_size)

		if msg == wait_msg or wait_msg == None:
			break

	return msg

def responseMsg(send_msg, wait_msg, sock, recive_size):
	while True:
		msg = sock.recv(recive_size)

		if msg == wait_msg or wait_msg == None:
			break
		else:
			sock.send("Resend")

	sock.send(send_msg)
	return msg
