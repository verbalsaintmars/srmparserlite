import multiprocessing.pool as Po

i = 0


def Fuck(a_a):
   print(a_a + 1)

print(Po.cpu_count())

pool = Po.ThreadPool(processes=Po.cpu_count())
pool.map(Fuck, (1, 2, 3))
pool.close()
pool.join()

print("--------")


import datetime
import time
import os.path

l_fileTime = os.path.getmtime(r"/etc/zshrc")
l_currentTime = time.time()

def Tmp((a,b,c)):
   print(a)
   print(b)
   print(c)

def Ret():
   return (1,2,3)

Tmp(Ret())

