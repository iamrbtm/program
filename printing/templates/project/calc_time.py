#!/usr/bin/python3
# Utility to calculate print time of gcode file
# Written by M.A.Helmreich (c)2016. V0.0.1
# expect bugs, tested (a little with reprap flavour Gcode).

# send improvements/bug reports to mail@helmreich.com.au

# usage:  Time_calc.py filename

# assumptions Feedrate in units per minute, dimensions are mm.
# 
Units='Millimetres'

import io, os, string, math, sys

for arg in sys.argv[1:]:
 FileName = arg
#Trace=1  for LOG file.(example below)
Trace=0



MoveDelay=0.000014945651469
PauseDelay=0.0006

os.system('clear')

print ('\n\n\n')
print ('Usage:  Time_calc.py filename')

print ('\n\n\nProcessing ', FileName)


f = open(FileName)
if Trace == 1:
 o = open(FileName + '._LOG', 'w')

BaseTime=15  
FeedRate=0.0
Material=0.0
MatFeed=0.0

DeltaX=0.0
DeltaY=0.0
DeltaZ=0.0
LastX=0.0
LastY=0.0
lastz=0.0
x=0.0
y=0.0
z=0.0
m=0.0

PauseCount=0
TotalMotion=0.0
Totaltime=0.0
MatTotaltime=0.0
Motion=0.0
gflag = 0
MoveCount=0

LineCount=0

while True:

 flin = f.readline()
 if flin == '':
  break
 array1 = flin.split()
 LineCount += 1 
 print ('\033[12;5f Calculating Line '+ str(LineCount))

 for item in array1:
  gg = item[0]
  if item[0:3] == 'G28':
   break
  elif gg == ';':
   break
  elif gg == 'X':
   x = float(item[1:])
  elif gg == 'Y':
   y = float(item[1:])
  elif gg == 'Z':
   z = float(item[1:])
  elif item[0:3] == 'G92':
   if MatFeed > 0:
    Material += MatFeed
    MatTotaltime +=  MatFeed / FeedRate * 2
    PauseCount += 1
# example of LOG output.
    if Trace ==1:
     outy = str(LineCount) +  ') Material ' + str(Material) + '\n'
     print(outy)    
     o.write(outy)
   break   
  elif gg == 'E':
   MatFeed = m
   m = float(item[1:])
  elif gg == 'F':
   FeedRate = float(item[1:])
  elif item[0:2] == 'G1':
   gflag = 1
   MoveCount += 1
  
 if gflag == 1:
  DeltaX = x - LastX
  DeltaY = y - LastY
  DeltaZ = z - lastz
  Motion = math.sqrt(DeltaX * DeltaX + DeltaY * DeltaY + DeltaZ *DeltaZ)
  TotalMotion += Motion
  Totaltime += Motion / FeedRate
  LastX = x
  LastY = y
  lastz = z   
 gflag = 0
f.closed

os.system('clear')

print ('\n\n\n')
print ('   REPORT for: ', FileName ,'\n\n')
print ('   Length of Motion', int(TotalMotion), Units)

print ('     Time of Motion', int( Totaltime + MoveCount * MoveDelay + BaseTime + PauseCount * PauseDelay + MatTotaltime), ' minutes')
print ('\n\n')

print ('         Move count', MoveCount)
print ('        Pause count', PauseCount)
print ('\n')
print ('    Material Length', int(Material), Units)
print ('\n\n\n\n\n')
input('Press [Enter] to close')