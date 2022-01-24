#!/usr/bin/python
from __future__ import absolute_import, print_function, unicode_literals
import sys
import pytz
from datetime import datetime
import logging
from json2sor import tools
import re
import struct
import math

logger = logging.getLogger('pyOTDR')
unit_map = {
            "mt (meters)":"mt",
            "km (kilometers)":"km",
            "mi (miles)" : "mi",
            "kf (kilo-ft)":"kf"
           }

tracetype = {
             "ST[standard trace]" : 'ST',
             "RT[reverse trace]" : 'RT',
             "DT[difference trace]" : 'DT',
             "RF[reference]" : 'RF',
            }

def process(results, format):
    """
    fh: file handle;
    results: dict for results;
    
    we assume mapblock.process() has already been run
    """
    bname = "FxdParams"
    fh = tools.getStr(bname)
    
    params = results[bname]
    fh += _process_fields(params)

    return fh

# ================================================================
def _process_fields(results):
    
    # functions to use
    # 'h': get_hexstring
    # 'v': get_uint
    # 's': get_string
    # 'i': get_signed
    """
    0-3: date/time: 4 bytes
    4-5: units: 2 characters
    6-7: wavelength: 2 bytes
    8-11: acqusition offset: 4 bytes integer
    12-15: acqusition offset distance: 4 bytes integer
    16-17: number of pulse width entries: 2 bytes (the next three parameters are repeated according to the number of entries)
    18-19: pulse-width: 2 bytes (repeated)
    20-23: sample spacing: 4 bytes (repeated)
    24-27: number of data points in trace: 4 bytes (repeated)
    28-31: index of refraction: 4 bytes
    32-33: backscattering coefficient: 2 bytes
    34-37: number of averages (?): 4 bytes
    38-39: averaging time: 2 bytes
    40-43: range (?): 4 bytes
    44-47: acquisition range distance: 4 bytes signed int
    48-51: front panel offset: 4 bytes signed int
    52-53: noise floor level: 2 bytes
    54-55: noise floor scaling factor: 2 bytes signed int
    56-57: power offset first point: 2 bytes
    58-59: loss threshold: 2 bytes
    60-61: reflection threshold: 2 bytes
    62-63: end-of-transmission threshold: 2 bytes
    64-65: trace type: 2 characters
    66-69: X1: 4 bytes signed int
    70-73: Y1: 4 bytes signed int
    74-77: X2: 4 bytes signed int
    78-81: Y2: 4 bytes signed int
    """
    unix = re.search(r'\d+',results['date/time'].split('(')[1]).group()
    xstr = struct.pack('<I', int(unix))
    xstr += bytearray(results['unit'][0:2], 'ascii')
    wave = float(results['wavelength'].replace(' nm', ''))/0.1
    xstr += tools.get_uint(int(wave))
    xstr += tools.get_signed(results['acquisition offset'],4)
    xstr += tools.get_signed(results['acquisition offset distance'], 4)
    xstr += tools.get_uint(results['number of pulse width entries'])
    xstr += tools.get_uint(results['pulse width'])
    ss = re.search(r'\d+', results['sample spacing']).group()
    xstr += tools.get_uint(int(float(ss) / 1e-8),4)
    xstr += tools.get_uint(int(results['num data points']), 4)
    # print("Number data points => {}".format(results['num data points']))   
    
    index = float(results['index']) * 100000
    xstr += tools.get_uint(int(index), 4)
    bc=float(results['BC'].replace(' dB', '')) / -0.1
    xstr += tools.get_uint(int(bc))
    xstr += tools.get_uint(results['num averages'], 4)
    avt=results['averaging time'].replace(' sec', '')
    xstr += tools.get_uint(int(avt))

    rng =int(results['range'] / 2e-5)
    xstr += tools.get_uint(int(rng), 4)
    # print("Range => {}".format(rng))
    # print("Range distance  => {}".format(results['acquisition range distance']))

    xstr += tools.get_signed(results['acquisition range distance'], 4)
    xstr += tools.get_signed(results['front panel offset'], 4)
    xstr += tools.get_uint(results['noise floor level'], 2)
    xstr += tools.get_signed(results['noise floor scaling factor'], 2)
    xstr += tools.get_uint(results['power offset first point'])
    
    '''threshold'''
    lth = float(results['loss thr'].replace(' dB', '')) / 0.001
    ref = float(results['refl thr'].replace(' dB', '')) /-0.001
    eot = float(results['EOT thr'].replace(' dB', '')) / 0.001
    xstr += tools.get_uint(int(lth), 2)
    xstr += tools.get_uint(math.ceil(ref), 2)
    xstr += tools.get_uint(math.ceil(eot), 2)
    xstr += bytearray(results['trace type'][0:2],'ascii')
    xstr += tools.get_signed(results['X1'],4)
    xstr += tools.get_signed(results['Y1'],4)
    xstr += tools.get_signed(results['X2'],4)
    xstr += tools.get_signed(results['Y2'],4)
    
    return xstr