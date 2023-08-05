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

class VmcUnelvent(DomotApiModbus.Modbus):

    def __init__(self, Port, SlaveAddress = 1, Mode = 'rtu', Serial = {'baudrate':19200,'bytesize':8,'parity':'E','stopbits':1 }):
        self._ITEMS={
    'mode': { 'type':'holding_register','params':{'RegisterAddress':15},'mapping':{ 0:'normal',1:'boost',2:'bypass'},'actions':('get','put')},
    'tint': { 'type':'input_register','params':{'RegisterAddress':21,'NumberOfDecimals':1,'Signed':True},'mapping':{ '0':'normal','1':'boost','2':'bypass'},'actions':('get')},
    'tout': { 'type':'input_register','params':{'RegisterAddress':22,'NumberOfDecimals':1,'Signed':True},'mapping':{ '0':'normal','1':'boost','2':'bypass'},'actions':('get')},
    'text': { 'type':'input_register','params':{'RegisterAddress':23,'NumberOfDecimals':1,'Signed':True},'mapping':{ '0':'normal','1':'boost','2':'bypass'},'actions':('get')},
    'tins': { 'type':'input_register','params':{'RegisterAddress':24,'NumberOfDecimals':1,'Signed':True},'mapping':{ '0':'normal','1':'boost','2':'bypass'},'actions':('get')},
    'bypass_auto': { 'type':'coils','params':{'RegisterAddress':8},'actions':('get','put')},
    'bypass_mode': { 'type':'coils','params':{'RegisterAddress':9},'actions':('get','put')},
    'regulation': { 'type':'input_register','params':{'RegisterAddress':10},'mapping':{ 2:'vitesse constante',4:'proportionnelle par entree 0 10',5:'CLP'},'actions':('get')},
    'vit_mot_ext': { 'type':'input_register','params':{'RegisterAddress':19},'actions':('get')},
    'vit_mot_ins': { 'type':'input_register','params':{'RegisterAddress':20},'actions':('get')},
    'etat_filtre': { 'type':'discrete_input','params':{'RegisterAddress':13},'mapping': {0 : 'ok', 1 : 'nok' }, 'actions':('get')},
                }
        super(VmcUnelvent,self).__init__(Port = Port,SlaveAddress = SlaveAddress,Mode = Mode,Serial = Serial)
