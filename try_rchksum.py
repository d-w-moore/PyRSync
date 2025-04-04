import ctypes
import pyrsync
import array
import sys
import wcs

lib = ctypes.cdll.LoadLibrary('./rchksum.so')

i = int(sys.argv[1])
p = print if (i&1) else lambda *p,**kw:None

out = (ctypes.c_ulong*3)(0,0,0)
buf = bytearray((0xff,))*4096
with wcs.timer() as t:
  while True:
    b = sys.stdin.buffer.read(4096)
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

print('elapsed =',t.elapsed)
#lib.dummy_fill( out)
#print([hex(_) for _ in out])
