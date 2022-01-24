#!/usr/bin/python
from __future__ import absolute_import, print_function, unicode_literals
import sys
import logging
import crcmod
from json2sor import tools


def process(results):
    bname = 'Cksum'
    fh = tools.getStr(bname)
    fh += tools.get_uint(results[bname]['checksum'])
    
    return fh