#! /usr/bin/env python

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
      for k in range(columns): filenamelist.append((str(col[int(k)]).strip('\n')))        
   # FOR loop END
     
   # close the file
   f.close()
   
   # return values to main program 
   return filenamelist   
   
# MAIN PROGRAM
if __name__=='__main__':
   _nargs = len(sys.argv)
   if _nargs == 1:
      file = 'SIMBADfiles'
   else:
      file = sys.argv[1]
   
   sourcename = []
   filenamelist = readfile(file)
   entries = len(filenamelist)
   for j in range(entries):
       sourcename.append(filenamelist[int(j)])
   
   # Open the output files
   SIMBADtypes = open('SIMBADtypes','w')

   print('The complete list of SIMBAD types was written to file named SIMBADtypes')   
   
   for j in range(entries):
       flag = 0
       count = 0
       success = 0
       if j % 2 == 0 :
           # even numbers
           target = sourcename[j]
       else:
           # odd numbers
           SIMBADresult = readfile(sourcename[j].lstrip(' '))
           rows = len(SIMBADresult)
           # FOR loop START
           for n in range(rows):
           # read in each line and split the string into a list of entries
               col = SIMBADresult[n].split('\n')
               # remove all list items that are unwanted
               while col.count('\n')>=1: 
                   col.remove('\n')
               while col.count('')>=1: 
                   col.remove('')
               if flag == 1:
                   count = count +1           
               if col[0] ==  'Basic data : ':
                   flag = 1
               if count == 15:
                   altname = col[0]
               if count == 18:      
                    print(target,'\t\t\t\t', col[0], '\t\t\t\t', altname, '\t\t\t\t', sourcename[j], file=SIMBADtypes)             
                    if len(target) < 16 :
                        if len(target) < 8 :
                            #print >> SIMBADtypes, target,'\t\t\t\t', col[0], '\t\t\t\t', altname, '\t\t\t\t', sourcename[j]
                            print(target,'\t\t\t\t', col[0])                      
                        else:
                            #print >> SIMBADtypes, target,'\t\t\t', col[0], '\t\t\t\t', altname, '\t\t\t\t', sourcename[j]
                            print(target,'\t\t\t', col[0])
                    else:    
                        if len(target) < 24 :
                            #print >> SIMBADtypes, target,'\t\t', col[0],'\t\t\t\t', altname, '\t\t\t\t', sourcename[j]
                            print(target,'\t\t', col[0])
                        else:
                            #print >> SIMBADtypes, target,'\t', col[0], '\t\t\t\t', altname, '\t\t\t\t', sourcename[j]
                            print(target,'\t', col[0])                        
                    success = 1
           if success == 0:
               print(target,'\t\t', '-','\t\t', '-','\t\t', sourcename[j], file=SIMBADtypes)
