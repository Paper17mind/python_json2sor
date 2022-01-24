import struct
import re

sol = 299792.458/1.0e6#0.299792458

def space(number):
  s = bytes(number)
  return s
def getStr(name):
    if name == " ":
        val = b'\x20\x00'
    else:
        val = bytearray(name, 'ascii')
        val += bytes(1)

    return val
# -----------------------------------------------------
def get_string(fh):
    """fh is the file handle """
    mystr = b''
    byte = fh
    if fh != '':
        mystr = bytearray(fh, 'ascii')
    else:
        mystr = bytes(1)
    return mystr

# -----------------------------------------------------
def get_float(fh, nbytes):
    """get floating point; fh is the file handle """
    tmp = fh
    if nbytes == 4:
        val = struct.pack("<f", tmp)
    elif nbytes == 8:
        val = struct.pack("<d", tmp)
    else:
        logger.error("tools.get_float(): Invalid number of bytes {}".format(nbytes))
        # TODO this should raise
        val = None
    
    return val

# -----------------------------------------------------
def get_uint(value, nbytes=2):
    """
    get unsigned int (little endian), 2 bytes by default
    (assume nbytes is positive)
    """
    
    # word = fh.read(nbytes)
    if type(value) == int:
      word = int(value)
    elif type(value) == str:
      word = int(re.search(r'\d+', value).group()) #int(value.replace(' nm', ''))
    else:
        word = 0
    # print(word)
    if nbytes == 2:
        # unsigned short
        val = struct.pack("<H", word)
    elif nbytes == 4:
        # unsigned int
        val = struct.pack("<I", word)
    elif nbytes == 8:
        # unsigned long long
        val = struct.pack("<Q", word)
    else:
        val = None
        # TODO this should raise
        logger.error("tools.get_uint(): Invalid number of bytes {}".format(nbytes))
    # print("packed {} , packed {}".format(val, packed))
    return val

# -----------------------------------------------------
def get_signed(value, nbytes=2):
    """
    get signed int (little endian), 2 bytes by default
    (assume nbytes is positive)
    """
    if type(value) == int:
        word = value
    else:
        word = int(re.search(r'\d+', value).group()) #int(value.replace(' nm', ''))
    # word = fh.read(nbytes)
    # print(word)
    if nbytes == 2:
        # unsigned short
        val = struct.pack("<h",word)
    elif nbytes == 4:
        # unsigned int
        val = struct.pack("<i",word)
    elif nbytes == 8:
        # unsigned long long
        val = struct.pack("<q",word)
    else:
        val = None
        # TODO this should raise
    
    return val

# -----------------------------------------------------
def get_hex(fh, nbytes=1):
    """
    get nbyte bytes (1 by default)
    and display as hexidecimal
    """
    hstr = ""
    for i in range(nbytes):
        b = "%02X " % ord(fh)
        hstr += b
    
    return hstr
