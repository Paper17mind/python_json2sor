#!/usr/bin/python
from __future__ import absolute_import, print_function, unicode_literals
import re
import logging
from json2sor import tools

logger = logging.getLogger('pyOTDR')

sep = "    :"

# ================================================================
def process(format, results):
    """ process version 1 or 2 format """
    bname = "KeyEvents"
    xref  = tools.getStr(bname)
    # number of events
    nev = tools.get_uint(len(results[bname])-2, 2)
    indexParam = float(results['FxdParams']['index'])
    factor = 1e-4 * tools.sol / indexParam
    xref += nev
    events = results[bname]
    for j in events:
        if j != 'num events' and j != 'Summary':
            distance = int(float(events[j]['distance']) / factor)
            number = int(re.search(r'\d+',j).group())
            xref += tools.get_uint(number, 2) # 00-01: event number
            xref += tools.get_uint(distance, 4) # 02-05: time-of-travel; need to convert to distance
            xref += tools.get_signed(int(float(events[j]['slope'])*1000), 2)# 06-07: slope
            xref += tools.get_signed(int(float(events[j]['splice loss'])*1000), 2)# 08-09: splice loss
            xref += tools.get_signed(int(float(events[j]['refl loss'])*1000), 4) # 10-13: reflection loss
            xref += bytearray(events[j]['type'][0:8],'ascii')
            
            if format == 2:
                xref += tools.get_uint(int(float(events[j]['end of prev'])/factor), 4)  # 22-25: end of previous event
                xref += tools.get_uint(int(float(events[j]['start of curr'])/factor), 4) # 26-29: start of current event
                xref += tools.get_uint(int(float(events[j]['end of curr'])/factor), 4)   # 30-33: end of current event
                xref += tools.get_uint(int(float(events[j]['start of next'])/factor), 4)   # 34-37: start of next event
                xref += tools.get_uint(int(float(events[j]['peak'])/factor), 4) # 38-41: peak point of event
            if (events[j]['comments'] != None):
                xref += bytearray(events[j]['comments'],'ascii')
            
            xref += bytes(1)
    # ...................................................
    fh = results['KeyEvents']['Summary']
    total      = tools.get_signed(int(float(fh['total loss']) * 1000), 4)  # 00-03: total loss
    loss_start = tools.get_signed(int(float(fh['loss start']) / factor), 4) # 04-07: loss start position
    loss_finish= tools.get_uint(int(float(fh['loss end']) / factor), 4)   # 08-11: loss finish position
    orl        = tools.get_uint(int(float(fh['ORL'])) * 1000, 2)   # 12-13: optical return loss (ORL)
    orl_start  = tools.get_signed(int(float(fh['ORL start']) / factor), 4) # 14-17: ORL start position
    orl_finish = tools.get_uint(int(float(fh['ORL finish'])/factor), 4)   # 18-21: ORL finish position
    xref += total
    xref += loss_start
    xref += loss_finish
    xref += orl
    xref += orl_start
    xref += orl_finish
    
    # ................
    status = 'ok'
    return xref

