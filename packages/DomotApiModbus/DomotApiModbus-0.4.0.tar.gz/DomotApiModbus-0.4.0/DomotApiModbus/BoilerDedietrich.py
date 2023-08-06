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

import DomotApiModbus

class BoilerDedietrich(DomotApiModbus.Modbus):

    def __init__(self, Port, SlaveAddress = 10, Mode = 'rtu', Serial = {'baudrate':9600,'bytesize':8,'parity':'N','stopbits':1 }, Timeout = 0.05):
        self._ITEMS={
                'mesure_exterieur': { 'type':'holding_register','params':{'RegisterAddress':7,'NumberOfDecimals':1,'Signed':True},'actions':('get')},
                }
        super(BoilerDedietrich,self).__init__(Port = Port,SlaveAddress = SlaveAddress,Mode = Mode,Serial = Serial, Timeout = Timeout)
        self.SetRetryStopMaxAttemptNumber(6)
        self.SetRetryWaitFixed(1000)

