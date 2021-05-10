
################################################

def intToVarLengthBytes(n):
    if n==0:
        return b'\x00'
    bs = bytearray()
    bs.insert(0, n % 128) # rightmost byte, bit 7 NOT set
    m = n >> 7
    while m > 0:
        bs.insert(0, (m % 128) | 0x80) # NOT rightmost byte, bit 7 IS set
        m >>= 7
    return bs

################################################

# Want a specified number of bytes in result
def intToBytes(n,numBytes):
    ls = []
    m = n
    for _ in range(0,numBytes):
        ls.insert(0, m % 256)
        m >>= 8
    return bytearray(ls)
    
################################################

# First byte is number of bytes in number.
# Rest of bytes represent the actual number.
# This is different from variable-length!
def intToLengthedInts(n):
    ls = []
    m = n
    while m > 0:
        ls.insert(0, m % 256)
        m >>= 8
    ls.insert(0,len(ls))
    return ls
    
def intToLengthedBytes(n):
    return bytearray(intToLengthedInts(n))

################################################

# First byte is number of bytes in number.
# Rest of bytes represent the actual number.
# This is different from variable-length!
# Hardcoded 3 bytes here.
def intToLengthedInts3(n):
    ls = []
    m = n
    for _ in range(0,3):
        ls.insert(0, m % 256)
        m >>= 8
    ls.insert(0,len(ls))
    return ls
    
def intToLengthedBytes3(n):
    return bytearray(intToLengthedInts3(n))
    
################################################
