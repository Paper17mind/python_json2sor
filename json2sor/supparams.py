#!/usr/bin/python
from __future__ import absolute_import, print_function, unicode_literals
import logging
import struct
from json2sor import tools

logger = logging.getLogger('pyOTDR')

sep = "    :"

def process(results):
    bname = "SupParams"
    params = results[bname]
    s = bytearray(bname, "ascii")
    s += bytes(1)
    s += process_supparam(params)
    return s
    # return fh

# ================================================================
def process_supparam(results):
    """ process SupParams fields """
    bname = "SupParams"
    xref  = b''
    fields = (
              "supplier", # ............. 0
              "OTDR", # ................. 1
              "OTDR S/N", # ............. 2
              "module", # ............... 3
              "module S/N", # ........... 4
              "software", # ............. 5
              "other", # ................ 6
            )
    
    for field in fields:
        #fh.write(bytearray(val,'ascii'))
        val = results[field]
        if val == 'software':
          xref += tools.getStr('Gismandau')
          xref += b'\x00'
        else:
            xref += tools.getStr(val)
    
    return xref