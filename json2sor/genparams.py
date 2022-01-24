#!/usr/bin/python
from __future__ import absolute_import, print_function, unicode_literals
import sys
import logging
from json2sor import tools
import struct

logger = logging.getLogger('pyOTDR')

sep = "\t:"

def process(results): 
    """
    fh: file handle;
    results: dict for results;
    we assume mapblock.process() has already been run
    """
    bname = "GenParams"
    params = results[bname]
    s = bytearray(bname, "ascii")
    s += bytes(1)
    s += bytearray('EN', 'ascii')
    # s += bytes(2)
    # if params['fiber type'].find("unknown") > -1:
    #   s += tools.get_uint(int(params['fiber type'][0:3]))
    # else:
    #     s += tools.get_uint(fiber_type(params['fiber type']),2) #fiber type
    # s += bytes((2,))
    # s += tools.get_uint(params['wavelength'], 2) # wavelength
    # s += bytes((6,)) # ??
    # s += bytes(1)
    # s += bytearray('BC','ascii')
    # s += bytes(10)
    s += process2(params)
    return s



# ================================================================
def build_condition(bcstr):
    """decode build condition"""
    condition = ''
    if bcstr == 'BC (as-built)':
        condition = "BC"
    elif bcstr == 'CC (as-current)':
        condition = "CC"
    elif bcstr == 'RC (as-repaired)':
        condition = "RC"
    elif bcstr == 'OT (other)':
        condition = "OT"
    else:
        condition = ""
    
    return condition

# ================================================================
def fiber_type(val):
    """ 
    decode fiber type 
    REF: http://www.ciscopress.com/articles/article.asp?p=170740&seqNum=7
    """
    if val == "G.651 (50um core multimode)": # ITU-T G.651
        fstr = 651
    elif val == "G.652 (standard SMF)": # standard nondispersion-shifted 
        fstr = 652
        # G.652.C low Water Peak Nondispersion-Shifted Fiber            
    elif val == "G.653 (dispersion-shifted fiber)":
        fstr = 653
    elif val == "G.654 (1550nm loss-minimzed fiber)":
        fstr = 654
    elif val == "G.655 (nonzero dispersion-shifted fiber)":
        fstr = 655
    else: # TODO add G657
        fstr = val[0:3]
    
    return fstr
"""
def process1(fh, results):
    
    bname = "GenParams"
    xref  = results[bname]
    
    # lang = fh.read(2).decode('ascii')
    # xref['language'] = lang
    logger.debug("{} language '{}', next pos {}".format(sep, lang, fh.tell()))
    
    fields = (
              "cable ID",    # ........... 0
              "fiber ID",    # ........... 1
              "wavelength",  # ............2: fixed 2 bytes value
              "location A", # ............ 3
              "location B", # ............ 4
              "cable code/fiber type", # ............ 5
              "build condition", # ....... 6: fixed 2 bytes char/string
              "user offset", # ........... 7: fixed 4 bytes (Andrew Jones)
              "operator",    # ........... 8
              "comments",    # ........... 9
             )
    
    count = 0
    for field in fields:
        fh.write(bytes(0))
        val = results['GenParams'][field]
        if field == 'build condition':
            xstr = build_condition(val)
            fh.write(struct.pack('<H', xstr))
        elif field == 'wavelength':
            # val = tools.get_uint(fh, 2)
            # xstr = "%d nm" % val
            fh.write(struct.pack('<H', int(val.replace(' nm', ''))))
        elif field == "user offset":
            # val = tools.get_signed(fh, 4)
            fh.write(struct.pack('<h', val))
            # xstr = "%d" % val
        else:
            fh.write(bytearray(val,'ascii'))
            # xstr = tools.get_string(fh)
        
        logger.debug("{}  {}. {}: {}".format(sep, count, field, xstr))
        # xref[field] = xstr
        count += 1
        
    status = 'ok'
    
    return status
"""
# =============*************===================================================
def process2(results):
    """ process version 2 format """
    bname = "GenParams"
    # lang = 'en'#fh.read(2)#.decode('ascii')
    # xref['language'] = lang
    xstr = b''
    fields = (
              "cable ID",    # ........... 0
              "fiber ID",    # ........... 1
              "fiber type",  # ........... 2: fixed 2 bytes value
              "wavelength",  # ............3: fixed 2 bytes value
              "location A", # ............ 4
              "location B", # ............ 5
              "cable code/fiber type", # ............ 6
              "build condition", # ....... 7: fixed 2 bytes char/string
              "user offset", # ........... 8: fixed 4 bytes int (Andrew Jones)
              "user offset distance", # .. 9: fixed 4 bytes int (Andrew Jones)
              "operator",    # ........... 10
              "comments",    # ........... 11
             )
    for field in fields:
        val = results[field]
        if field == 'build condition':
            xstr += tools.getStr(results['build condition'][0:2]) #build condition
        elif field == 'fiber type':
            xstr += tools.get_uint(fiber_type(val), 2)
        elif field == 'wavelength':
            xstr += tools.get_uint(val, 2)
        elif field == "user offset" or field == "user offset distance":
            xstr += tools.get_signed(val, 4)
        else:
            val = tools.getStr(val)
            xstr += val
   
    return xstr
