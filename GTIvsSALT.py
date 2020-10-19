#! /usr/bin/env python

#################################################################################################
# Determine SALT visibility windows overlap with RXTE Good Time Intervals (GTI) for a target    #
#################################################################################################

import sys
import datetime
import calendar

####################################################
# Function to read a file containing the RXTE GTIs #
####################################################
def readGTIs(file):
   """Read in the input file per line and returns list of strings to main program   """
   # Try to open the file and return an error if this fails
   try:
      f = open(file,'r')
   except IOError:
      print('Failed to open '+file)
      return None
   
   GTIstart = []
   GTIend = []
   GTItarget = []
   satellite = []
     
   # read in the file (as a list of lines for which each line is a string) 
   s = f.readlines()
   rows = len(s)
   # FOR loop START
   for n in range(rows):
      # read in each line and split the string into a list of entries
      col = s[n].split('\t')
      # remove all list items that are unwanted
      while col.count('\n')>=1: 
         col.remove('\n')
      while col.count('')>=1: 
         col.remove('')
      columns = len(col)      
      if len(col) >= 1:
         GTItarget.append(col[0])              
         start = col[1].split(':')
         GTIstart.append(datetime.datetime(int(start[0]),int(start[1]),int(start[2]),int(start[3]),int(start[4])))
         end = col[2].split(':')
         GTIend.append(datetime.datetime(int(end[0]),int(end[1]),int(end[2]),int(end[3]),int(end[4]))) 
         satellite.append(col[4].strip('\n'))                       
   # FOR loop END
     
   # close the file
   f.close()
   
   # return values to main program 
   return GTItarget, GTIstart, GTIend, satellite


##################################################################
# Function to read a file containing the SALT visibility windows #
##################################################################
def readSALTvis(file):
   """Read in the input file per line and returns data to main program   """
   # Try to open the file and return an error if this fails
   try:
      f = open(file,'r')
   except IOError:
      print('Failed to open '+file)
      return None
   
   flag = 0
   SALTstart = []
   SALTend = []
   SALTtarget = []
          
   # read in the file (as a list of lines for which each line is a string) 
   s = f.readlines()
   rows = len(s)   
   # FOR loop START
   for n in range(rows):
   
       # read in each line and split the string into a list of entries
       col = s[n].split('\t')
       # remove all list items that are unwanted
       while col.count('\n')>=1: 
          col.remove('\n')
       while col.count('')>=1: 
          col.remove('')
         
       if col[0] == '------------------------------------------------------\n':
           flag = 1
                  
       else:
           SALTtarget.append(col[0])
           start = col[1].split('-') + col[2].split(':')       
           end = col[1].split('-') + col[3].split(':')
           startdatetime = datetime.datetime(int(start[0]),int(start[1]),int(start[2]),int(start[3]),int(start[4]))
           enddatetime = datetime.datetime(int(end[0]),int(end[1]),int(end[2]),int(end[3]),int(end[4]))
           SALTstart.append(startdatetime)
           if (enddatetime-startdatetime).days == -1 :           
               SALTend.append(enddatetime + datetime.timedelta(days=1))
           else:
               SALTend.append(enddatetime)
   # FOR loop END
     
   # close the file
   f.close()
   
   # return values to main program 
   return SALTstart, SALTend, SALTtarget
   
   
####################
##################
#  MAIN PROGRAM  #
##################
####################
if __name__=='__main__':
   _nargs = len(sys.argv)
   if _nargs == 1:
      GTIfile = raw_input("Enter the name of the file containing RXTE GTIs :  ")
      SALTfile = raw_input("Enter the name of the file containing SALT visibility windows :  ")
      mintrack = raw_input("Enter the minimum overlapping tracklength required (in hours):  ")

   else:
      GTIfile = str(sys.argv[1])
      SALTfile = str(sys.argv[2])
      mintrack = float(sys.argv[3])


   ##########################################################
   #  Get the lists of RXTE GTI and SALT visibility windows #
   ##########################################################  
 
   SALTstart, SALTend, SALTtarget = readSALTvis(SALTfile)
   GTItarget, GTIstart, GTIend, satellite =  readGTIs(GTIfile) 
     
   today = datetime.date.today()
   oneday = datetime.timedelta(days=1)
   overhead = datetime.timedelta(minutes=15)
   
   ##########################
   # Open the outputfile    #
   ##########################   
   overlaps = open('overlaps','w')

   targetlist = []
   
   ##########################
   # Determine the overlaps #
   ##########################

   for n in range(len(SALTstart)):       
       for m in range(len(GTIstart)):
           
           if GTItarget[m].replace('_',' ') == SALTtarget[n].replace('_',' ') and (len(targetlist)==0 or (GTItarget[m]+str(GTIstart[m]) not in targetlist)): 
               overlaplength = min(SALTend[n],GTIend[m]) - max((SALTstart[n]+overhead),GTIstart[m])
               obsstart = max((SALTstart[n]+overhead),GTIstart[m])-overhead
               obsend =  min(SALTend[n],GTIend[m])            
               if overlaplength.days == 0 and overlaplength.seconds >= mintrack*60*60 : 
                   targetlist.append(GTItarget[m]+str(GTIstart[m])) 
                   print('Target:',SALTtarget[n].replace('_',' '), file=overlaps)
                   print(' ', file=overlaps)
                   print('Start (UT):', obsstart, '\t', '\t', 'End (UT):', obsend, '\t', 'Overlap:', overlaplength, file=overlaps)
                   print(' ', file=overlaps)
                   print('SALT window:', '\t', '\t', SALTstart[n], '\t', SALTend[n], file=overlaps)
                   if len(satellite[m]) > 4:
                       print(satellite[m] + ' interval:', '\t', GTIstart[m], '\t', GTIend[m], file=overlaps)
                   else:
                       print(satellite[m] + ' interval:', '\t','\t', GTIstart[m], '\t', GTIend[m] , file=overlaps)
                   print('-----------------------------------------------------------------------------------', file=overlaps)
