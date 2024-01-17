
from collections.abc import ByteString
import random


class NAND:
  def __init__(self, in1, in2):
    self.in1 = in1
    self.in2 = in2
  def get_value(self):
    return not(self.in1.get_value() and self.in2.get_value())
  def count(self):
    return 1 + self.in1.count() + self.in2.count()
  def toString(self):
    return "NAND(" + self.in1.toString() + ", " + self.in2.toString() + ")"

class NOR:
  def __init__(self, in1, in2):
    self.in1 = in1
    self.in2 = in2
  def get_value(self):
    return not(self.in1.get_value() or self.in2.get_value())
  def count(self):
    return 1 + self.in1.count() + self.in2.count()
  def toString(self):
    return "NOR(" + self.in1.toString() + ", " + self.in2.toString() + ")"

class Switch:
  def __init__(self, name):
    self.value = False
    self.name = name
  def count(self):
    return 0
  def get_value(self):
    return self.value
  def get_name(self):
    return self.name
  def set_value(self, value):
    self.value = value
  def flip(self):
    self.value = not self.value
    return self.value
  def toString(self):
    return self.name



#A = Switch("A")
#B = Switch("B")
#C = Switch("C")
#D = Switch("D")
SWITCHES = []

def reset():
  global SWITCHES
  for switch in SWITCHES:
    switch.set_value(False)

def next():
  global SWITCHES
  for i in range(len(SWITCHES)):
    if SWITCHES[i].flip():
      return False
  return True



def trNAND(tt, max, ins):
  global SWITCHES
  outs = []
  for i in range(len(SWITCHES)):
    outs.append(SWITCHES[i])

  for i in range(max):
    outs.append(NAND(outs[int(random.random()*len(outs))], outs[int(random.random()*len(outs))]))
    reset()
    for i2 in range(2**4):
      tsum = 0
      for i3 in range(len(SWITCHES)):
        tsum += SWITCHES[i3].get_value()*2**(len(SWITCHES)-i3-1)
      if outs[len(outs)-1].get_value() != tt[tsum]:
        break

      if next():
        count = outs[len(outs)-1].count()
        if count <= max:
          print("\nfound a solution with " + str(count) + " gates")
          print(outs[len(outs)-1].toString())
        return count

  return False


def trNOR(tt, max, ins):
  global SWITCHES
  outs = []
  for i in range(len(SWITCHES)):
    outs.append(SWITCHES[i])

  for i in range(max):
    outs.append(NOR(outs[int(random.random()*len(outs))], outs[int(random.random()*len(outs))]))
    reset()
    for i2 in range(2**ins):
      tsum = 0
      for i3 in range(len(SWITCHES)):
        tsum += SWITCHES[i3].get_value()*2**(len(SWITCHES)-i3-1)
      if outs[len(outs)-1].get_value() != tt[tsum]:
        break

      if next():
        count = outs[len(outs)-1].count()
        if count <= max:
          print("\nfound a solution with " + str(count) + " gates")
          print(outs[len(outs)-1].toString())
        return count

  return False



print("----------------------------\nWelcome to the NAND/NOR logic converter\nThis program was written by Andrew B\n----------------------------\n\n")

ALPH = ["A", "B", "C", "D", "E", "F", "G", "H"]
TT = []
ins = 9

while True:
  ins = int(input("Enter number of inputs: "))
  if ins > 1 and ins < 9:
    break
  print("Invalid input. Please enter a number between 2 and 8.\n")

for i in range(ins):
  SWITCHES.append(Switch(ALPH[i]))
#ins = 4 #default
print("\nFill out the corresponding outputs to the truth table")
for i in range(2**ins):
  #form prompt string
  tprompt = ""
  for i2 in range(ins):
    tprompt += str(i//(2**(ins-i2-1))%2)
    if i2 != ins-1:
      tprompt += " - "
  #print prompt string
  TT.append(int(input(tprompt + "  : ")))
ns = input('\nNAND gates or NOR gates? (type "nand" or "nor")  : ')
if ns == "NAND" or ns == "nand":
  nands = True
else:
  nands = False

best = int(input("\nMaximum number of gates  : "))+1
print("\n----------------------------\nAttempting to find a solution with " + str(best-1) + " gates or less...\nThis may take a while depending on how complex the circuit is...\n\nThe program will not find a solution if the maximum gate input is too low\n----------------------------\n")
count = 0
while True:
  count+=1
  if count%100000 == 0:
    print(str(count) + str(" attempts"))
  if nands:
    val = trNAND(TT, best-1, ins)
  else:
    val = trNOR(TT, best-1, ins)
  if val and val < best:
    best = val
    print("*solution found on try " + str(count) + "*\n")

