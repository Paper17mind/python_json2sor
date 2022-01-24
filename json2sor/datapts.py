#!/usr/bin/python
from __future__ import absolute_import, print_function, unicode_literals

import logging
import sys
import struct
from json2sor import tools

sep = "    :"

logger = logging.getLogger('pyOTDR')


def process(results, tracedata):
    """
    fh: file handle;
    results: dict for results;
    
    we assume mapblock.process() has already been run
    """
    bname = "DataPts"
    # include trailing '\0'
    fh = bytearray(bname, 'ascii')
    fh += bytes(1)
    # number of data points
    # method used by STV: minimum reading shifted to zero
    # method used by AFL/Noyes Trace.Net: maximum reading shifted to zero (approx)
    _process_data(fh, results, tracedata)
    return fh

def toHex(val, yMax, fs=1000):
  number = float(val.split('\t')[1].replace('\n', ''))
  value = abs(int(number * fs) - yMax)
  return struct.pack('H', value)

def toNum(val, yMax, fs=1000):
    number = float(val.split('\t')[1].replace('\n', ''))
    value = abs(int(number * fs) - yMax)
    return value
# ================================================================
def _process_data(fh, results, tracedata, dumptrace=True):
    """ process version 1 format """
    bname = "DataPts"
    traces = results['trace']
    point = results['data'][bname]
    traces_len = len(traces)
    fh += tools.get_uint(traces_len, 4)
    fh += tools.get_signed(point['num traces'], 2)
    # xref['num data points'] = N
    # val = tools.get_signed(fh, 2)
    # xref['num traces'] = val
    fh += tools.get_uint(traces_len, 4)
    # xref['num data points 2'] = val
    # logger.debug("{} num data points again = {}".format(sep, val))
    fh += tools.get_uint(int(point['scaling factor'] * 1000),2)
    # val = tools.get_uint(fh, 2)
    # scaling_factor = val / 1000.0
    # xref['scaling factor'] = scaling_factor
    # logger.debug("{} scaling factor = {}".format(sep, scaling_factor))

    # .....................................
    # adjusted resolution
    ymax = int(point['max before offset'] * 1000)
    # ymin = min(dlist)
    # fs = 1000 * point['scaling factor']

    # dx = results['data']['FxdParams']['resolution']
    # dlist = [toHex(x, ymax) for x in traces]

    # disp_min = "%.3f" % (ymin * fs)
    # disp_max = "%.3f" % (ymax * fs)
    # xref['max before offset'] = float(disp_max)
    # xref['min before offset'] = float(disp_min)
    for x in traces:
        fh += toHex(x, ymax)
    # .........................................
    # save to file
    
    return fh
