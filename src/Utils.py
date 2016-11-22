"""
Utils for benchmark-daemon

@author FATESAIKOU
"""

#from tensorflow.python.client import device_lib

import time


def getDeviceList():
    #device_ids = [ device.name for device in device_lib.list_local_devices()]
    device_ids = [1, 2, 3]

    return device_ids

def getPerformance(benchmark_src):
    start = time.time()
    exec(benchmark_src)
    end = time.time()

    return end - start

def requestMsg(send_msg, wait_msg, sock, recive_size):
    counter = 0
    while True:
        counter += 1
        sock.send(send_msg)
        print "Send: ", send_msg
        msg = sock.recv(recive_size)
        print "Recv ", msg, "Aim: ", wait_msg

        if msg == wait_msg or wait_msg == None or counter > 10:
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
