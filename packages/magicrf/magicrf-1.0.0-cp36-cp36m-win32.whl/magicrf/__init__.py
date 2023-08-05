# -*- coding:UTF-8 -*-
""" Library for UHF RFID Soc Reader Chip M100 and QM100 """
# !/usr/bin/python
# Python:   3.5.2
# Platform: Windows/Linux/ARMv7
# Author:   Heyn (heyunhuan@gmail.com)
# Program:  Library for UHF RFID Soc Reader Chip M100 and QM100.
# History:  2018-10-29 Wheel Ver:1.0.0 [Heyn] Initialize


import sys
import serial
import serial.threaded
from magicrf import _m100

class ReaderCallBack( serial.threaded.FramedPacket ):

    def __init__(self, trigger=_m100.TRIGGER_QUERY):
        self.__trigger = trigger

    def __call__(self):
        return self

    def data_received(self, data):
        _m100.unpack( data, self.__trigger )


def uart_register(func):
    def wrapper(self, *args, **kwargs):
        payload = func(self, *args, **kwargs)
        return self.ser.write(payload)
    return wrapper


class m100( object ):
    HFSS_AUTO = _m100.HFSS_AUTO
    HFSS_STOP = _m100.HFSS_STOP

    MODE_HIGH_SENSITIVITY = _m100.MODE_HIGH_SENSITIVITY
    MODE_DENSE_READER     = _m100.MODE_DENSE_READER

    TRIGGER_QUERY     = _m100.TRIGGER_QUERY
    TRIGGER_READ_DATA = _m100.TRIGGER_READ_DATA

    BANK_RFU  = _m100.BANK_RFU
    BANK_EPC  = _m100.BANK_EPC
    BANK_TID  = _m100.BANK_TID
    BANK_USER = _m100.BANK_USER

    def __init__(self, port='COM1', baudrate=115200, bytesize=8, parity=serial.PARITY_NONE, stop=serial.STOPBITS_ONE):
        _m100.init()
        self.ser = serial.serial_for_url(port, do_not_open=True)
        self.ser.baudrate = baudrate
        self.ser.bytesize = bytesize
        self.ser.parity   = parity
        self.ser.stopbits = stop

        self.open()

    def open(self):
        try:
            self.ser.open()
        except serial.SerialException as e:
            sys.stderr.write('Could not open serial port {}: {}\n'.format(self.ser.name, e))
            self.sys.exit(1)

    def rxcallback(self, func):
        _m100.unpack_cb( func )

    @uart_register
    def query(self, loop=1):
        return _m100.query(loop)

    @uart_register
    def power(self, dbm=22):
        return _m100.power(dbm)

    @uart_register
    def mode(self, param=_m100.MODE_DENSE_READER):
        return _m100.mode(param)

    @uart_register
    def hfss(self, mode=_m100.HFSS_AUTO):
        return _m100.hfss(mode)

    @uart_register
    def insert(self, start=0, stop=5):
        return _m100.insert(start=start, stop=stop)

    @uart_register
    def setchannel(self, index=1):
        return _m100.setchannel(index)

    @uart_register
    def param(self, select=0, session=0, target=0, q=4):
        return _m100.param(select=0, session=0, target=0, q=4)

    @uart_register
    def select(self, epc, target=0, action=0, bank=_m100.BANK_EPC, ptr=2, truncate=False):
        return _m100.select(epc, target=target, action=action, bank=bank, ptr=ptr, truncate=truncate)
    
    @uart_register
    def read(self, bank, password='00000000', addr=0, length=2):
        return _m100.read(bank=bank, pwd=password, addr=addr, length=length)

    @uart_register
    def write(self, bank, data, addr=0):
        return _m100.write(bank=bank, data=data, addr=addr)

    def start(self, callback=ReaderCallBack, trigger=_m100.TRIGGER_QUERY):
        serial_worker = serial.threaded.ReaderThread( self.ser, callback(trigger) )
        serial_worker.start()
