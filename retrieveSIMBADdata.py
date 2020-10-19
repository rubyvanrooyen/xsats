#! /usr/bin/env python

################################################################################################
#               Create query script for SIMBAD for all sources listed on webpage               #
#################################################################################################

import sys


# Function to read a datafile
def readfile(file):
   """Read in the input file per line and 

   returns list of strings to main program
   """
   # Try to open the file and return an error if this fails
   try:
      f = open(file,'r')
   except IOError:
      print('Failed to open '+file)
      return None
   filenamelist = []
   idname = []
   count = []
   
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
      # make a list of the files
      for k in range(columns): 
          entry0 = (str(col[int(k)]).strip('\n')).replace('NEAR_','')
          entry00 = entry0.split('/')
          entry1 = entry00[0].replace('_','')
          entry2 = entry1.replace('MGC','MCG')
          entry3 = entry2.replace('X-',' X-')
          entry4 = entry3.replace('RXSJ','RXJ')
          entry5 = entry4.replace('IGR-J','IGRJ')
          entry6 = entry5.replace('#','')
          entry = entry6.replace('+','%2B')
          filenamelist.append(str(entry)) 
          idname.append(str(entry6))   
          count.append(float(0))
   # FOR loop END
     
   entries = len(filenamelist)   
   for j in range(entries):
       for l in range(j):
           if str(filenamelist[j]) == str(filenamelist[l]):
               count[j] = float(count[j]) + 1   
       if j % 2 :
           if float(count[j-1]) < 1:
               coords = str(filenamelist[int(j)])
               coord = idname[j].split(' ')
               ra = coord[0] + ' ' + coord[1]+ ' ' + coord[2]
               dec = coord[3] + ' ' + coord[4]+ ' ' + coord[5]
               coordstring = 'RA = '+ra+';   DEC = '+dec
#           print >> scriptWGET, 'wget "http://simbad.u-strasbg.fr/simbad/sim-coo?output.format=HTML&Coord='+coords+'&Radius=2&Radius.unit=arcmin"'
               #format:  http://simbad.u-strasbg.fr/simbad/sim-coo?output.format=HTML&Coord=12 30 +10 20&Radius=10&Radius.unit=arcmin
#           print >> SIMBADfiles, identifier, 'sim-coo?output.format=HTML&Coord='+str(idname[int(j)])+'&Radius=2&Radius.unit=arcmin'
       else:
           if float(count[j]) < 1:         
               identifier = str(filenamelist[int(j)])   
               print('wget "http://simbad.u-strasbg.fr/simbad/sim-id?Ident='+identifier+'"', file=scriptWGET)
               #format:  http://simbad.u-strasbg.fr/simbad/sim-id?output.format=ASCII&Ident=hd 1
               print(idname[int(j)],'\t', "sim-id?Ident="+identifier.replace(' ','%20'), file=SIMBADfiles)
                 
   # close the file
   f.close()
   
   # return values to main program 
   return filenamelist

# Function to print a string
def printstring(s):
    """Prints a string to stdout"""
    print(s)

# MAIN PROGRAM
if __name__=='__main__':
   _nargs = len(sys.argv)
      
   # Open the output files
   SIMBADfiles = open('SIMBADfiles','w')
   scriptWGET = open('scriptWGET','w')
   print('#! /bin/bash', file=scriptWGET)
       
   filenamelist = readfile('listall')
