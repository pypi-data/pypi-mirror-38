# -*- coding:UTF-8 -*-
""" Case3 """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/Linux/ARMv7
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Read tag Data.
# History:  2018-10-30 Ver:1.0 [Heyn] Initialization

import time
import queue
import datetime
import threading
from magicrf import m100
from magicrf import _m100

SERIAL_PORT = 'COM14'

QUEUE_READER = queue.Queue(2048)

READER = m100(SERIAL_PORT)

def receive_callback(data):
    # QUEUE_READER.put(data)
    print(data)
    # for i in data:
    #     print('{} '.format(hex(ord(i))), end=' ')
    # print()

READER.rxcallback( receive_callback )
READER.start( trigger=m100.TRIGGER_QUERY|_m100.TRIGGER_SET_PA_POWER )


def realtime_threading( queue ):
    while True:
        data = queue.get()
        for item in data.split(';'):
            if not item:
                continue
            try:
                epc, rssi = item.split(',')
            except ValueError:
                print(item)
                continue
            timenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print('{0} -> {1} RSSI: -{2} dBm'.format(timenow, epc, int(rssi, 16)))



# REALTIME_THD = threading.Thread( target=realtime_threading, args=( QUEUE_READER, ) )
# REALTIME_THD.setDaemon(True)
# REALTIME_THD.start()

# for _ in ( READER.power(22), READER.mode(), READER.hfss(m100.HFSS_AUTO), READER.param(q=4) ):
#     time.sleep(0.1)

# while True:
#     READER.query(500)
#     time.sleep(0.01)

# READER.query(5)

READER.power()
# READER.param(session=m100.PARAM_SESSION_S1)
# # time.sleep(3)
# # data = READER.select(epc='31323334')
# data = READER.select(epc='646C', target=m100.PARAM_TARGET_B, truncate=True)
# READER.query(20)
# data = READER.select(epc='52533A505744000000000000')
# print(data)
# for item in data:
#     print(hex(item), end=' ')
# print()
# time.sleep(3)

# data = READER.read(bank=m100.BANK_EPC, length=4)
# data = READER.read(memory=m100.BANK_USER, length=8)
# data = READ
# ER.read(bank=m100.BANK_USER, length=8)
# print(data)
# for item in data:

#     print(hex(item), end=' ')
# print()

# data = READER.write(data='11223344556677889900', bank=m100.BANK_USER)
# print(data)
# for item in data:
#     print(hex(item), end=' ')
# print()
time.sleep(8)
