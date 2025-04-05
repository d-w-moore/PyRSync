import ctypes
import pyrsync
import array
import sys
import wcs
import getopt

lib = ctypes.cdll.LoadLibrary('./rchksum.so')
opts,args=getopt.getopt(sys.argv[1:],'i:')
optD=dict(opts)
i = int(args[0])

import pdb;pdb.set_trace()
if '-i' in optD:
  sys_stdin = open(optD['-i'],'r')
else:
  sys_stdin = sys.stdin
#dwm

p = print if (i&1) else lambda *p,**kw:None

out = (ctypes.c_ulong*3)(0,0,0)
buf = bytearray((0xff,))*4096
newbuf = bytearray([0])*len(buf)

J = j = i&(32|64|128)  
assert j in [32,64,128]# only one please
with wcs.timer() as t:
  while True:
    b = sys_stdin.buffer.read(4096)
    lb = len(b)
    if (lb == 0): break
    buf[:lb] = b
    if i&2:
      lib.weakchecksum(
        (ctypes.c_char * lb).from_buffer(buf),
        lb,
        out
      )
      x1 = [_ for _ in out]
      p(x1,end='\t')
    if i&4:
      x2 = list(pyrsync.weakchecksum(buf[:lb]))
      p(x2,end='\t')
    if i&6:
      p()
    if i&6 == 6:
      if x1 != x2: break
    if J  == 32: break
    J >>= 1

print('elapsed =',t.elapsed)
#lib.dummy_fill( out)
#print([hex(_) for _ in out])

rucs = lib.repeat_update_weakchecksum
rucs.restype = ctypes.c_long
byte_ptr_type=ctypes.POINTER(ctypes.c_uint8)
long_ptr_type=ctypes.POINTER(ctypes.c_long)
rucs.argtypes = [
        ctypes.c_char * len(buf),       # buf
        ctypes.c_int,                   # blocksize
        ctypes.POINTER(ctypes.c_int),   # offs
        byte_ptr_type,                  # newbuf
        ctypes.c_int,                   # nnew
        long_ptr_type,                  # outbuf
        ctypes.POINTER(ctypes.c_long),  # a
        ctypes.POINTER(ctypes.c_long),  # b
]
rucs.restype = None

if i&2:
  ucs = lib.update_weakchecksum
  ucs.restype = ctypes.c_long
  ucs.argtypes = [
        ctypes.c_char * len(buf),       # buf
        ctypes.c_int,                   # blocksize
        ctypes.POINTER(ctypes.c_int),   # offs
        ctypes.c_int,                   # new
        ctypes.POINTER(ctypes.c_long),  # a
        ctypes.POINTER(ctypes.c_long),  # b
  ]
  I = ctypes.c_int(0)
  from ctypes import(c_uint8,c_long,POINTER,sizeof,byref,cast)
  if i&32:
    L=0
    with wcs.timer() as timer:
        while True:
          newbuf = sys_stdin.buffer.read(len(buf)*4);
          lnb=len(newbuf)
          newbuf = (c_uint8*lnb)(*(_ for _ in newbuf))
          if lnb == 0: break
          L+=lnb
          #print(f'step {L = }',file=sys.stderr)
          outsums = (c_long*lnb)()
          rucs(
            (ctypes.c_char * len(buf)).from_buffer(buf), len(buf), ctypes.pointer(I),     # buf,blocksize,offs
            newbuf, lnb, cast(byref(outsums),long_ptr_type), # newbuf,nnew,outbuf
            cast(byref(out,sizeof(c_long)),POINTER(c_long)),   #a
            cast(byref(out,2*sizeof(c_long)),POINTER(c_long))  #b
          )
    print(f'{L = }{timer.elapsed = }')
    exit()
  if i&64:
   for x in range(4096):
     l = ucs( 
       (ctypes.c_char * lb).from_buffer(buf), len(buf), ctypes.pointer(I),
       ord(sys_stdin.buffer.read(1)),
       cast(byref(out,sizeof(c_long)),POINTER(c_long)),
       cast(byref(out,2*sizeof(c_long)),POINTER(c_long))
     )
     out[0] = l
  print('after->',[(_) for _ in out])
