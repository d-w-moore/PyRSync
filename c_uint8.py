from ctypes import *
h.sumchar((c_uint8*5)(*(_ for _ in b'\0\1\2\3\4')),5)
h=cdll.LoadLibrary('./rchksum.so')
h.sumchar.argtypes=[POINTER(c_uint8),c_int]
h.sumchar((c_uint8*5)(0,1,2,3,4,5),6)
h.sumchar((c_uint8*6)(0,1,2,3,4,5),6)
h.sumchar((x:=(c_uint8*6)(0,1,2,3,4,5)),6)
x
list(x)
h.sumchar((x:=(c_uint8*6)(0,1,2,3,4,50)),6)
list(x)
