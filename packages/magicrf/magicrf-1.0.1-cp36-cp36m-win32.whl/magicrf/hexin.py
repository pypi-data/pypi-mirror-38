# -*- coding:UTF-8 -*-
""" Library for UHF RFID Soc Reader Chip M100 and QM100 """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/Linux/ARMv7
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Library for UHF RFID Soc Reader Chip M100 and QM100.
# History:  2018-08-15 Wheel Ver:1.0.0 [Heyn] Initialize

import serial
import serial.threaded

from magicrf import m100

print('Initial magicrf m100 module.')

import queue
import struct
import datetime

q=queue.Queue(1024)

class ReaderCallBack( serial.threaded.FramedPacket ):

    def __init__(self):
        super().__init__()
        self.cb = None
        self.size = 0
        self.data = ''

        
        print('callback')
    def __call__(self):
        return self

    def data_received(self, data):
        # if self.cb is not None:
        #     self.cb(data)
        # print(data)
        try:
            # print(len(data))
            m100.unpack( data, m100.HEXIN_MAGICRF_QUERY )
        except BaseException as err:
            print(err)
            print('123')
        # for byte in serial.iterbytes(data):
        #     if byte == b'\xBB':
        #         self.in_packet = True
        #         self.packet.extend(byte)
        #     elif byte == b'\x7E':
        #         self.in_packet = False
        #         self.packet.extend(byte)
        #         if (self.size + 7 == len(self.packet)):
        #             self.handle_packet(bytes(self.packet)) # make read-only copy
        #             del self.packet[:]
        #         else:
        #             self.in_packet = True

        #     elif self.in_packet:
        #         self.packet.extend(byte)
        #         if len(self.packet) == 5:
        #             head, typecode, command, self.size = struct.unpack('!BBBH', self.packet)
        #             # print('size {}'.format(self.size))
        #     else:
        #         self.handle_out_of_packet_data(byte)

    def handle_packet(self, packet):
        # print('*****')
        print(m100.unpack(packet))

    def handle_packet123(self, data):
        self.data = data
        # q.put(data)
        # return True
        # print('*****###')
        # print(trigger)
        # print(datetime.datetime.now(), data)

ser = serial.serial_for_url('COM14', do_not_open=True)
ser.baudrate = 115200
ser.bytesize = 8
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE

try:
    ser.open()
except serial.SerialException as e:
    sys.stderr.write('Could not open serial port {}: {}\n'.format(ser.name, e))
    sys.exit(1)


def receive(data):
    # q.put(data)
    print(data)

read = ReaderCallBack()
# read.cb = receive

m100.unpack_cb(receive)

serial_worker = serial.threaded.ReaderThread(ser, read)
serial_worker.start()

m100.power(22)
m100.mode(m100.MODE_DENSE_READER)

xx = m100.query(100)

import time
while True:
    try:
        ser.write(xx)
    except BaseException as err:
        print(err)
    time.sleep(0.1)

    try:
        print(q.get(timeout=0.1))
    except BaseException:
        pass
    # break

print('Done')
