#include <stddef.h>

// # libFoo.c:
// # (don't forget to use extern "C" if this is a .cpp file)
// #
// # void foo(unsigned char* buf, size_t bufSize) {
// #   for (size_t n = 0; n < bufSize; ++n) {
// #     buf[n] = n;
// #   }
// # }
// 
// fooLib = ctypes.cdll.LoadLibrary('./lib/libFoo.dylib')
// 
// ba = bytearray(10)
// 
// char_array = ctypes.c_char * len(ba)
// 
// fooLib.foo(char_array.from_buffer(ba), len(ba))
// 
// for b in ba:
//   print b

typedef unsigned char byte;

int dummy_fill( long output[3]) {
    output[0]=0xfeedface;
    output[1]=-1;
    output[2]=0x7fffffff;
}

#define conglom(A,B) (((unsigned long)(B))<<16)|(A)

int weakchecksum(const byte *buf, size_t bufsize, long output[3]) {
  unsigned int a=0,b=0;
  for (int i=0; i<bufsize;i++) {
    a += *buf;
    b += (bufsize-i) * (*buf++);
  }
  output[0] = conglom(a,b);
  output[1] = a;
  output[2] = b;
}

long update_weakchecksum(byte *buf, size_t blocksize, int *offs,
                         int new, long*a, long*b) {
  byte removed = buf[*offs];
  buf[(*offs)++] = new ;
  *offs %= blocksize;
  *a -= (removed - new);
  *b -= (removed * blocksize - *a);
  return conglom(*a,*b);
}

void repeat_update_weakchecksum(byte *buf, size_t blocksize, int *offs,
                                byte *newbuf, int nnew, long *outbuf,
                                long *a, long *b)
{
    for (int i=0; i<nnew;i++) {
        *outbuf++ = update_weakchecksum(buf,blocksize,offs,
                                        *newbuf++, a, b);
    }
}

void repeat_fill(long *output,int buf,byte c){
  while (buf-- > 0) {*output++ = c; c++;}
}

/*
void repeat_rchecksum_calc(byte* win, int *checksums)
{
  int *p_new , *p_removed;
}
*/

int sumchar(unsigned char *c, int ln) {
 int s = 0;
 for (int i=0;i<ln;i++) {s+=(*c); *c++='\xff';}
 return s;
}

