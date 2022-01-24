#!/usr/bin/python
import sys
import logging
import binascii
import struct
from json2sor import genparams,tools, supparams, fxdparams, keyevents, datapts, cksum

logger = logging.getLogger('pyOTDR')

def block(name, size, version=200):
  s = tools.getStr(name)
  s += tools.get_uint(version) #version
  s += tools.get_uint(size, 4) #size
  s += bytes(0)
  return s

def process(data): 
    """
    fh: file handle;
    results: dict for results;
    """
    
    gParam = genparams.process(data['data'])
    sParam = supparams.process(data['data'])
    fParam = fxdparams.process(data['data'],2)
    kEvent = keyevents.process(2, data['data'])
    dtPts = datapts.process(data,[])
    ckSum = cksum.process(data['data'])
    #print("Length = gen: {}, sup: {}, fix:{}, evt:{}, pts:{}, mapblock:{}".format(len(gParam), len(sParam), len(fParam), len(kEvent), len(dtPts), len(mblock)))
    results = data['data']
    fh = tools.getStr('Map')
    tt = float(data['version']) * 100
    fh += tools.get_uint(int(tt))
    blocks = b''
    # maps = (
    #     ['GenParams', len(genparams)],
    #     ['SupParams', len(sParam)],
    #     ['FxdParams', len(fParam)],
    #     ['KeyEvents', len(kEvent)],
    #     ['DataPts', len(dtPts)],
    #     ['Cksum', len(ckSum)]
    # )
    maps = (
        'GenParams',
        'SupParams',
        'FxdParams',
        'KeyEvents',
        'DataPts',
        'Cksum',
    )
    
    for item in maps:
        name = item
        # i = results['blocks'][name]
        ver = float(data['version']) * 100
        blocks += bytearray(name, 'ascii') #name
        blocks += bytes(1) #space
        blocks += tools.get_uint(int(ver),2) #struct.pack('H', int(ver)) #version
        if name == 'GenParams':
            size = len(gParam)
        elif name == 'SupParams':
            size = len(sParam)
        elif name == 'FxdParams':
            size = len(fParam)
        elif name == 'KeyEvents':
            size = len(kEvent)
        elif name == 'DataPts':
            size = len(dtPts)
        else:
          size = len(ckSum)
        
        blocks += tools.get_uint(size, 4)
    # print(len(fParam))
    fh += tools.get_uint(102, 4) #
    fh += tools.get_uint(6) #no of block dibuat static
    fh += blocks
    # 
    fh += gParam
    fh += sParam
    fh += fParam
    fh += kEvent
    fh += dtPts
    fh += ckSum
    return fh

