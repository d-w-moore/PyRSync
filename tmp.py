from ctypes import *
lib=cdll.LoadLibrary('./rchksum.so')
rf=lib.repeat_fill
rf.argtypes = [ c_long*10,c_int,c_uint8]
b=(c_long*10)()
rf.restype = None

print('b',list(b))
rf( (c_long*5).from_buffer(b), 9, 32)
print('a',list(b))
