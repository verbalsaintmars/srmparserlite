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

class Base(object):
  def __init__(this):
    this.a = 10

  def getA(this):
    return this.a

  A = property(getA)

class Derived(Base):
  def __init__(this):
    super(Derived,this).__init__()
    this.b = 20

d = Derived()
print(d.A)  # will this print?
