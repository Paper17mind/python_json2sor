#!/usr/bin/python
from __future__ import absolute_import, print_function, unicode_literals
import re
import logging
import math
from json2sor import tools

logger = logging.getLogger('pyOTDR')

sep = "    :"
def distToNS(val, factor):
  res = (float(val) + 0.0004) / factor
#   print(res)
  return int(res)
# ================================================================
def process(format, results):
    """ process version 1 or 2 format """
    bname = "KeyEvents"
    xref  = dict()
    # number of events
    nev = 9
    indexParam = float(results['data']['FxdParams']['index'])
    refractor = results['data']['FxdParams']['index'].replace('.', '')
    factor = 1e-4 * tools.sol / indexParam
    xref['num events'] = nev
    xEvent = dict()
    # print("sol {} index {}, factor {}".format(tools.sol, indexParam, factor))
    events = results['data']['KeyEvents']
    for j in events:
        if j != 'num events' and j != 'Summary':
            # factor = ('%d',% )#int((float(events[j]['distance']) / tools.sol * indexParam) / 100)
            number = int(re.search(r'\d+',j).group())
            xEvent[number] = dict()
            xEvent[number]['id'] = number             # 00-01: event number
            xEvent[number]['dist'] = distToNS(events[j]['distance'], factor)
            # int(float(events[j]['distance'])/factor)    # 02-05: time-of-travel; need to convert to distance
            
            xEvent[number]['slope'] = int(float(events[j]['slope'])*1000) # 06-07: slope
            xEvent[number]['splice loss'] = int(float(events[j]['splice loss'])*1000)# 08-09: splice loss
            xEvent[number]['refl loss'] = int(float(events[j]['refl loss'])*1000) # 10-13: reflection loss
            xEvent[number]['type'] = events[j]['type'][0:8]
            if format == 2:
                xEvent[number]['enf of prev'] = int(float(events[j]['end of prev'])/factor)  # 22-25: end of previous event
                xEvent[number]['star of curr'] =  int(float(events[j]['start of curr'])/factor) # 26-29: start of current event
                xEvent[number]['end of curr'] =  int(float(events[j]['end of curr'])/factor)   # 30-33: end of current event
                xEvent[number]['start of next'] =  int(float(events[j]['start of next'])/factor)   # 34-37: start of next event
                xEvent[number]['peax'] =  int(float(events[j]['peak'])/factor) # 38-41: peak point of event
            xEvent[number]['comments'] = events[j]['comments']
            xref[j] = xEvent[number]
    # ...................................................
    fh = results['data']['KeyEvents']['Summary']
    total      = int(float(fh['total loss']) * 1000)  # 00-03: total loss
    loss_start = int(float(fh['loss start']) / factor) # 04-07: loss start position
    loss_finish= int(float(fh['loss end']) / factor)   # 08-11: loss finish position
    orl        = float(fh['ORL']) * 1000   # 12-13: optical return loss (ORL)
    orl_start  = int(float(fh['ORL start']) / factor) # 14-17: ORL start position
    orl_finish = int(float(fh['ORL finish'])/factor)   # 18-21: ORL finish position
    xsum = xref['Summary'] = dict()
    xsum['total'] =  total
    xsum['loss start'] =  loss_start
    xsum['loss finish'] =  loss_finish 
    xsum['ORL'] =  orl
    xsum['ORL Start'] =  orl_start
    xsum['ORL Finish'] =  orl_finish
    
    # ................
    status = 'ok'
    return xref

