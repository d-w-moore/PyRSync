import time
import sys
import pyrsync

class timer:
  def __enter__(self):
      self.__t = time.time()
      return self
  def __exit__(self,*x):
      self.elapsed = time.time() - self.__t

if __name__ == '__main__':
    x = '1'
    stdin = (sys.stdin.buffer if sys.version_info >= (3,) else
             sys.stdin)
    with timer() as t:
        while x:
            x = stdin.read(4096)
            it = x if sys.version_info >= (3,) else [ord(_) for _ in x]
            y = pyrsync.weakchecksum(it)

    print(t.elapsed)


