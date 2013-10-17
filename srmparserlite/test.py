import os

"""
def Test():
   with open(
         os.path.join(
            os.path.normpath(r"/myfiles/Source/vsProject/srmparserlite/pplog/"),
            "OneBigLog.log")) as l_bfileObj:

            for l_line in l_bfileObj:
               yield l_line

it = Test()
ln = next(it)

print(ln)
print(ln)
print("--------------------")

for a in it:
   print(a)
"""

class Test(object):
   __slots__ = ["a"]
   def __init__(this):
      pass

   def fuck(this):
      if hasattr(this, "a"):
         print("fuck")
      else:
         this.a = "10"
         print("asd")

class DE(Test):
   pass

t = DE()
t.b = 20
t.fuck()
t.fuck()
t.fuck()
t.fuck()
t.fuck()
