#!/usr/bin/env python
"""
To test Benchmark-daemon

@author FATESAIKOU
"""

import sys
import socket
import json

import Utils

import pprint

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('', 22222))

command = sys.argv[1]
Utils.requestMsg(command, 'Connection-Success', sock, 1024)

if command == 'get-device-list':
    result_size = int(Utils.requestMsg('Exec', None, sock, 1024))
    result = json.loads(Utils.requestMsg('Got-Size', None, sock, result_size))
elif command == 'get-performance':
    benchmark_src = 'print "Hello World"'
    benchmark_src_size = str(len('print "Hello World"'))
    Utils.requestMsg(benchmark_src_size, 'Got-Size', sock, 1024)
    result_size = int(Utils.requestMsg(benchmark_src, None, sock, 1024))
    result = float(Utils.requestMsg('Got-Size', None, sock, result_size))
elif command == 'get-net-con':
    sh_command = "iperf -c %s -n %d | grep sec | awk '{print $4}'" % ('localhost', 100 * 1024 * 1024)
    Utils.requestMsg(sh_command, 'Got-Cmd', sock, 1024)
    result_size = int(Utils.requestMsg('Exec', None, sock, 1024))
    result = float(Utils.requestMsg('Got-Size', None, sock, result_size))

pprint.pprint(result)
