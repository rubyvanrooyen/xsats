#! /usr/bin/env python

##############################################################
# Determine SALT visibility windows for a list of targets    #
##############################################################

import sys
import datetime
import calendar


########################################################################################
# Function to read a file containing source, RA and DEC and passes it to main program  #
########################################################################################
def readfile(datafile):
   """Read in the input file per line and 
   returns data to main program
   """
   # Try to open the file and return an error if this fails
   try:
      f = open(datafile,'r')
   except IOError:
      print('Failed to open '+file)
      return None
       
   # read in the file (as a list of lines for which each line is a string) 
   s = f.readlines()
   rows = len(s)
   target = []
   RA = []
   DEC = []
   EPOCH = []
   
   # FOR loop START
   for n in range(rows):
       if (str(s[n])).count('%') <= 0:
           # read in each line and split the string into a list of entries
           col = s[n].split(' \t ')
           # remove all list items that are unwanted
           while col.count('\t')>=1: 
               col.remove('\t')
           while col.count('')>=1: 
               col.remove('') 
           # add the column entries to the arrays   
           target.append(col[0].strip(' ').replace(' ','_'))
           RA.append(col[1])
           DEC.append(col[2])
           EPOCH.append(col[3])
   # FOR loop END
     
   # close the file
   f.close()
   
   # return values to main program 
   return target,RA,DEC,EPOCH
   
   
####################
##################
#  MAIN PROGRAM  #
##################
####################
if __name__=='__main__':
   _nargs = len(sys.argv)
   if _nargs == 1:
      file = raw_input("Enter the name of the file containing SALT targets:  ")
      stop = raw_input("Enter the date where to stop (CCYY MM DD):  ")
      stops = stop.split(' ')
      stopdatey = int(stops[0])
      stopdatem = int(stops[1])
      stopdated = int(stops[2])

   else:
      file = sys.argv[1]
      stopdatey = int(sys.argv[2])
      stopdatem = int(sys.argv[3]) 
      stopdated = int(sys.argv[4])
      
   target,RA,DEC,EPOCH = readfile(file)
   startdate = datetime.date.today()
   stopdate = datetime.date(stopdatey,stopdatem,stopdated)
   oneday = datetime.timedelta(days=1)
   script = open('script','w')
   print('#! /bin/bash', file=script)
   targets = open('targetsDONE','w')
   
   

   
   for n in range(len(target)):    
       date = startdate      
       while date <= stopdate:
           inputfile = open('inputfile'+str(target[n])+'_'+str(date),'w')
           print(str(date.day) +'/'+ str(date.month) +'/'+ str(date.year), file=inputfile)
           print(RA[n], file=inputfile)
           print(DEC[n], file=inputfile)
           print(EPOCH[n], file=inputfile)
           print(1, file=inputfile)
           print('../IDLroutines/track.exe<"inputfile'+str(target[n])+'_'+str(date)+'">"outputfile'+str(target[n])+'_'+str(date)+'"', file=script)
           
           date += oneday  
       print(str(target[n]), file=targets)
