## Copyright (c) 2018 Denis Sacchet <denis@sacchet.fr>
## 
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
## 
## The above copyright notice and this permission notice shall be included in all
## copies or substantial portions of the Software.
## 
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
## SOFTWARE.

import minimalmodbus
import functools
import os
import hashlib
import errno

from retrying import retry
import dogpile.cache

_RUN_DIR='/var/run/domot-api'
try:
    os.makedirs(_RUN_DIR)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

def minimalmodbus_cache_key_generator(namespace,fn):
    fname = fn.__name__
    def generate_key(*arg,**kw):
        if 'UseMapping' not in kw:
            kw['UseMapping'] = False
        key = fname + \
                "__Item__" + str(kw['Item']) + \
                "__UseMapping__" + str(kw['UseMapping'])
        return key
    return generate_key

region = dogpile.cache.make_region(function_key_generator = minimalmodbus_cache_key_generator)

class Utils(object):
    def md5(self,string):
        m = hashlib.md5()
        m.update(string)
        return m.hexdigest()

class DeviceLockException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Modbus(object):

    def __init__(self,Port,SlaveAddress,Serial,Mode = 'rtu',Timeout=0.05,Debug=False):
        self.Port = Port
        self.SlaveAddress = SlaveAddress
        self.Mode = Mode
        self.Serial = Serial
        self.Timeout = Timeout
        self.Debug = Debug
        self.Instrument = None
        self.Utils = Utils()
        self.RetryStopMaxAttemptNumber = 5
        self.RetryWaitFixed = int(self.Timeout * 1.1 * 1000)
        region.configure(
                'dogpile.cache.dbm',
                expiration_time = 60,
                arguments = {
                    "filename":self._GetCacheDevicePath()
                    }
                )

        self._func_mapping = {
                ('holding_register','get') : { 'func': self._ReadRegister,  'FunctionCode':3 },
                ('holding_register','put') : { 'func': self._WriteRegister, 'FunctionCode':16 },
                ('input_register','get') :   { 'func': self._ReadRegister,  'FunctionCode':4 },
                ('input_register','put') :   { 'func': self._WriteRegister, 'FunctionCode':6 },
                ('discrete_input','get') :   { 'func': self._ReadBit,       'FunctionCode':2 },
                ('discrete_input','put') :   { 'func': self._WriteBit,      'FunctionCode':5 },
                ('coils','get') :            { 'func': self._ReadBit,       'FunctionCode':1 },
                ('coils','put') :            { 'func': self._WriteBit,      'FunctionCode':15 },
        }

        self._mapping_read_write_function_code = {
                16:3,
                6:4,
                5:2,
                15:1,
                3:16,
                4:6,
                2:5,
                1:15,
                }

    def SetRetryStopMaxAttemptNumber(self,value):
        self.RetryStopMaxAttemptNumber = int(value)

    def SetRetryWaitFixed(self,value):
        self.RetryWaitFixed = int(value)

    def GetRetryStopMaxAttemptNumber(self):
        return int(self.RetryStopMaxAttemptNumber)

    def GetWaitFixed(self):
        return int(self.RetryWaitFixed)

    def _GetLockDevicePath(self):
        return _RUN_DIR+'/lock-'+self.Utils.md5(self.GetPort())

    def _GetCacheDevicePath(self):
        return _RUN_DIR+'/cache-'+self.Utils.md5(self.GetPort())

    @region.cache_on_arguments()
    def GetValue(self,Item,UseMapping=False):
        if Item in self._ITEMS:
            ItemConfig = self._ITEMS[Item]
            if 'get' not in ItemConfig['actions']:
                raise NotImplemntedError
            if (ItemConfig['type'],'get') not in self._func_mapping:
                raise NotImplemntedError
            else:
                func = self._func_mapping[(ItemConfig['type'],'get')]
                params = ItemConfig['params']
                params['FunctionCode'] = func['FunctionCode']
                result=func['func'](**params)
                if UseMapping:
                    try:
                        return ItemConfig['mapping'][result]
                    except:
                        return result
                else:
                    return result

    def PutValue(self,Item,Value,UseMapping=False):
        if Item in self._ITEMS:
            ItemConfig = self._ITEMS[Item]
            if 'put' not in ItemConfig['actions']:
                raise NotImplemntedError
            if (ItemConfig['type'],'put') not in self._func_mapping:
                raise NotImplemntedError
            else:
                func = self._func_mapping[(ItemConfig['type'],'put')]
                params = ItemConfig['params']
                params['Value'] = Value
                params['FunctionCode'] = func['FunctionCode']
                result = func['func'](**params)
                self.GetValue.invalidate(Item=Item,UseMapping=True)
                self.GetValue.invalidate(Item=Item,UseMapping=False)

    # Wrapper to allow define dynamically in subclass retry paramaters
    def RetryModbus(func=None):
        @functools.wraps(func)
        def wrap(self,*args, **kargs):
            stop_max_attempt_number = self.GetRetryStopMaxAttemptNumber()
            wait_fixed = self.GetWaitFixed()

            @retry(stop_max_attempt_number = stop_max_attempt_number, wait_fixed = wait_fixed)
            def retried_func(self,*args,**kargs):
                return func(self,*args,**kargs)
            return retried_func(self,*args,**kargs)
        return wrap

    def LockDevice(func=None):
        @functools.wraps(func)
        def wrap(self,*args, **kargs):
            _lock_path = self._GetLockDevicePath()
            if not os.access(_lock_path, os.F_OK):
                try:
                    _lock_file_fd=open(_lock_path,'w')
                    _lock_file_fd.write(str(os.getpid()))
                    _lock_file_fd.close()
                    result = func(self,*args,**kargs)
                    os.remove(_lock_path)
                    return result
                except:
                    os.remove(_lock_path)
                    raise
            else:
                _lock_file_fd=open(_lock_path,'r')
                pid=_lock_file_fd.read()
                _lock_file_fd.close()
                raise DeviceLockException('Access to '+self.GetPort()+' currently locked by PID '+pid)
        return wrap

    def InitInstrument(func):
        @functools.wraps(func)
        def wrap(self, *args, **kargs):
            if self.Instrument == None:
                self.Instrument = minimalmodbus.Instrument(
                        port = self.GetPort(),
                        slaveaddress = self.GetSlaveAddress(),
                        mode = self.GetMode()
                        )
                serial=self.GetSerial()
                self.Instrument.serial.baudrate = serial['baudrate']
                self.Instrument.serial.bytesize = serial['bytesize']
                self.Instrument.serial.parity   = serial['parity']
                self.Instrument.serial.stopbits = serial['stopbits']
                self.Instrument.serial.timeout  = self.GetTimeout()
                self.Instrument.debug           = self.GetDebug()
            return func(self,*args,**kargs)
        return wrap

    def GetDebug(self):
        return self.Debug

    def GetTimeout(self):
        return self.Timeout

    def GetPort(self):
        return self.Port

    def GetSlaveAddress(self):
        return self.SlaveAddress

    def GetMode(self):
        return self.Mode

    def GetSerial(self):
        return self.Serial

    @RetryModbus
    @LockDevice
    @InitInstrument
    def _ReadBit(self,RegisterAddress,FunctionCode):
        return self.Instrument.read_bit(
                registeraddress = RegisterAddress,
                functioncode = FunctionCode
                )

    @RetryModbus
    @LockDevice
    @InitInstrument
    def _WriteBit(self,RegisterAddress,Value,FunctionCode=5):
        self.Instrument.write_bit(
                registeraddress = RegisterAddress,value = Value, 
                functioncode = FunctionCode
                )

    @RetryModbus
    @LockDevice
    @InitInstrument
    def _ReadRegister(self,RegisterAddress,FunctionCode,NumberOfDecimals=0,Signed=False):
        return self.Instrument.read_register(
                registeraddress = RegisterAddress,
                numberOfDecimals = NumberOfDecimals,
                functioncode = FunctionCode,
                signed = Signed
                )

    @RetryModbus
    @LockDevice
    @InitInstrument
    def _WriteRegister(self,RegisterAddress,Value,FunctionCode,NumberOfDecimals=0,Signed=False):
        self.Instrument.write_register(
                registeraddress = RegisterAddress,
                value = Value,
                numberOfDecimals = NumberOfDecimals,
                functioncode = FunctionCode,
                signed = Signed
                )
