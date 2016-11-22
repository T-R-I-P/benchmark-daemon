#!/usr/bin/env python
"""
Benchmark-daemon for tensorflow performance & network connection

@author FATESAIKOU
"""

import sys
import socket
import json
import subprocess

import Utils


""" Env paramaters """
COMMAND_MAX = 1024
host = ''
port = 22222

""" Initialize socket """
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    sys.stderr.write("[ERROR] %s\n" % msg[1])
    sys.exit(1)

sock.bind((host, port))
sock.listen(2)


""" Reading """
while True:
    """ Client Connection Start """
    (csock, addr) = sock.accept()
    print "[Connect] Connected from ", addr
    
    """ Get Command """
    msg = Utils.responseMsg("Connection-Success", None, csock, COMMAND_MAX)

    """ Execute """
    if msg == 'get-device-list':
        send_data = json.dumps(Utils.getDeviceList())
        Utils.responseMsg(str(len(send_data)), 'Exec', csock, COMMAND_MAX)
        Utils.responseMsg(send_data, 'Got-Size', csock, COMMAND_MAX)
    elif msg == 'get-performance':
        benchmark_src_size = int(Utils.responseMsg('Got-Size', None, csock, COMMAND_MAX))

        """ Program Execution """
        benchmark_src = csock.recv(benchmark_src_size)
        send_data = str(Utils.getPerformance(benchmark_src))
        csock.send(str(len(send_data)))

        Utils.responseMsg(send_data, 'Got-Size', csock, COMMAND_MAX)
    elif msg == 'get-net-con':
        sh_command = Utils.responseMsg('Got-Cmd', None, csock, COMMAND_MAX)
        transfer_time = subprocess.check_output(sh_command, shell=True)
        Utils.responseMsg(str(len(transfer_time)), 'Exec', csock, COMMAND_MAX)
        Utils.responseMsg(transfer_time, 'Got-Size', csock, COMMAND_MAX)
    elif msg == 'end':
        sys.exit(0)
    else:
        send_data = 'Unknow-Command'
