#! /usr/bin/env python

#################################################################################################
# Determine SALT visibility windows overlap with RXTE Good Time Intervals (GTI) for a target    #
#################################################################################################

import sys
import datetime
import os

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
      col = s[n].split(' \t ')
      # remove all list items that are unwanted
      while col.count('\n')>=1: 
         col.remove('\n')
      while col.count('')>=1: 
         col.remove('')
      columns = len(col)      
      if len(col) >= 1:
         GTItarget.append(col[0].strip(' '))              
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
   moonphase = []
   moonstatus = []
          
   # read in the file (as a list of lines for which each line is a string) 
   s = f.readlines()
   rows = len(s)   
   # FOR loop START
   for n in range(rows):   
       # read in each line and split the string into a list of entries
       col = s[n].split(' \t ')
       # remove all list items that are unwanted
       while col.count('\n')>=1: 
          col.remove('\n')
       while col.count('')>=1: 
          col.remove('')
         
       if col[0] == '------------------------------------------------------\n':
           flag = 1                 
       else:
           SALTtarget.append(col[0].strip(' '))
           start = col[1].split('-') + col[2].split(':')       
           end = col[1].split('-') + col[3].split(':')
           startdatetime = datetime.datetime(int(start[0]),int(start[1]),int(start[2]),int(start[3]),int(start[4]))
           enddatetime = datetime.datetime(int(end[0]),int(end[1]),int(end[2]),int(end[3]),int(end[4]))
           SALTstart.append(startdatetime)
           if (enddatetime-startdatetime).days == -1 :           
               SALTend.append(enddatetime + datetime.timedelta(days=1))
           else:
               SALTend.append(enddatetime)
           moonphase.append(col[5])
           moonstatus.append(col[6])
   # FOR loop END
     
   # close the file
   f.close()
   
   # return values to main program 
   return SALTstart, SALTend, SALTtarget, moonphase, moonstatus
   
################################
# Function to read SIMBADtypes #
################################
def readSIMBAD(file):
   """Read in the input file per line and returns data to main program   """

   sourceid = []
   sourcetype = []
   sourcename = []
   
   # Try to open the file and return an error if this fails
   try:
      f = open(file,'r')
   except IOError:
      print('Failed to open '+file)
      return None
   
   s = f.readlines() 
   rows = len(s)
   if rows > 0:
   # FOR loop START
      for n in range(rows):
         # read in each line and split the string into a list of entries
         col = s[n].split('\t')
         while col.count('\n')>=1: 
            col.remove('\n')
         while col.count('')>=1: 
            col.remove('')      
         sourceid.append(col[0].replace(' ','').replace('_','').strip(' '))
         sourcetype.append(col[1].strip(' '))         
         sourcename.append(col[2].strip(' '))    
   else:
         sourceid.append('-')
         sourcetype.append('-')         
         sourcename.append('-')  
   # FOR loop END
     
   # close the file
   f.close()
   
   # return values to main program 
   return sourceid, sourcetype, sourcename, s

########################################################################################
# Function to read a file containing source, RA and DEC and passes it to main program  #
########################################################################################
def readfile(file):
   """Read in the input file per line and returns data to main program """
   # Try to open the file and return an error if this fails
   try:
      f = open(file,'r')
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
           target.append(col[0].strip(' '))
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
      GTIfile = raw_input("Enter the name of the file containing RXTE GTIs :  ")
      SALTfile = raw_input("Enter the name of the file containing SALT visibility windows :  ")
      mintrack = raw_input("Enter the minimum overlapping tracklength required (in hours):  ")

   else:
      GTIfile = str(sys.argv[1])
      SALTfile = str(sys.argv[2])
      mintrack = float(sys.argv[3])
 
   rundate = GTIfile.replace('_gti','')[0:4] +'-'+  GTIfile.replace('_gti','')[4:6] +'-'+ GTIfile.replace('_gti','')[6:]
   
   oneday = datetime.timedelta(days=1)
   obsdatestart = datetime.datetime(int(GTIfile.replace('_gti','')[0:4]),int(GTIfile.replace('_gti','')[4:6]),int(GTIfile.replace('_gti','')[6:]),12,0,0)
   obsdateend = obsdatestart + oneday
   
   ##########################################################
   #  Get the lists of RXTE GTI and SALT visibility windows #
   ##########################################################  
   SALTstart, SALTend, SALTtarget, moonphase, moonstatus = readSALTvis(SALTfile)
   GTItarget, GTIstart, GTIend, satellite =  readGTIs(GTIfile) 

   ###################
   # Get SIMBADtypes #
   ###################
   sourceid, sourcetype, sourcename, s =  readSIMBAD('SIMBADtypes_'+GTIfile.replace('_gti',''))

   ###################
   # Get Coordinates #
   ###################
   target, RA, DEC, EPOCH = readfile(GTIfile.replace('gti','')+'targets') 
               
   ##########################
   # Open the outputfile    #
   ##########################   
   overlaps = open('OverlapAlertInfo','w')
   targetlist = []
   
   ##########################
   # Determine the overlaps #
   ##########################
   teststring = []
   duplicate = 0
   success = 0
   for n in range(len(SALTtarget)):       
       for m in range(len(GTItarget)):
           count = 0
           for l in range(len(target)):
               #for k in range(len(sourceid)):           
                   #if GTItarget[m] == SALTtarget[n] and GTItarget[m] == target[l] and GTItarget[m] == sourceid[k]: 
                   if GTItarget[m].replace('_',' ') == SALTtarget[n].replace('_',' ') and GTItarget[m] == target[l] and count < 1:
                       count = count + 1
                       overlapbegin = max(SALTstart[n],GTIstart[m])
                       overlapend = min(SALTend[n],GTIend[m])
                       overlaplength =  overlapend - overlapbegin
                       prior = max(SALTstart[n],GTIstart[m]) - SALTstart[n] 
                       currentstring = SALTtarget[n]+RA[l]+DEC[l]+str(SALTstart[n])+str(SALTend[n])+str(GTIstart[m])+str(GTIend[m])
                       for j in range(len(teststring)):                           
                           if teststring[j] == currentstring:
                               duplicate = 1
                           else:
                               duplicate = 0                               
                       if overlaplength.days == 0 and overlaplength.seconds >= mintrack*60*60 and duplicate == 0 and ((overlapbegin <= obsdateend and overlapbegin >= obsdatestart) or (overlapend <= obsdateend and overlapend >= obsdatestart)) and (len(targetlist)==0 or (GTItarget[m]+str(GTIstart[m]) not in targetlist)):
                           targetlist.append(GTItarget[m]+str(GTIstart[m]))
                           for k in range(len(sourceid)):
                               entry0 = currentstring.replace('NEAR_','')
                               entry00 = entry0.split('/')
                               entry1 = entry00[0].replace('_','')
                               entry2 = entry1.replace('MGC','MCG')
                               entry3 = entry2.replace('X-',' X-')
                               entry4 = entry3.replace('RXSJ','RXJ')
                               entry5 = entry4.replace('IGR-J','IGRJ')
                               entry6 = entry5.replace('#','')
                               if (entry6.replace(' ','')).count(sourceid[k]) > 0:
                                   SIMBADsourcetype = sourcetype[k]
                                   SIMBADalias = sourcename[k]
                           print('Target:', '\t', '\t',SALTtarget[n].replace('_',' '), file=overlaps)
                           print('--------------------------------------------------------------------------------------------------------------------------------', file=overlaps)  
                           if SIMBADsourcetype == '-':
                               SIMBADsourcetype = 'Undetermined'
                           if SIMBADalias == '-':
                               SIMBADalias = 'Undetermined'    
                           if SIMBADsourcetype == 'Undetermined' and SIMBADalias == 'Undetermined':
                               print('Please use the SIMBAD (coordinate) query below for further details of the target. SIMBAD (identifier) query did not yield a result.', file=overlaps)
                           else:    
                               print(SIMBADsourcetype, '   a.k.a.  ', SIMBADalias, file=overlaps)
                           print(' ', file=overlaps)                                               
                           print('\t', '\t','\t','Start (UT):','\t','\t', 'End (UT):''\t', '\t', '\t', 'Overlap:', file=overlaps)
                           print('Simultaneity: ','\t','\t', max(SALTstart[n],GTIstart[m]),'\t', min(SALTend[n], GTIend[m]), '\t', '\t', overlaplength, file=overlaps)
                           print(' ', file=overlaps)
#                           print('Moonphase:',moonphase[n].replace('moon = ',''),'\t', moonstatus[n], file=overlaps)
                           print('SALT window:', '\t', '\t',SALTstart[n], '\t', SALTend[n],'\t','\t','Preperation time:  ','\t', prior, file=overlaps)
                           if len(satellite[m]) > 4:
                               print(satellite[m] + ' interval:', '\t', GTIstart[m], '\t', GTIend[m], file=overlaps)
                           else:
                               print(satellite[m] + ' interval:', '\t','\t', GTIstart[m], '\t', GTIend[m], file=overlaps)                          
                           print(' ', file=overlaps)
                           print('Coordinates:', file=overlaps)
                           print('RA:','\t', RA[l], file=overlaps)
                           print('DEC:','\t', DEC[l], file=overlaps)                        
                           print(' ', file=overlaps)               
                           print('SIMBAD (Identifier):', file=overlaps)
                           print(str('http://simbad.u-strasbg.fr/simbad/sim-id?Ident='+SALTtarget[n].replace('_',' ')).replace(' ','%20'), file=overlaps)
                           coords = RA[l]+' '+DEC[l]
                           print('SIMBAD (Coordinates):', file=overlaps)
                           print(str('http://simbad.u-strasbg.fr/simbad/sim-coo?output.format=HTML&Coord='+coords+'&Radius=2&Radius.unit=arcmin').replace(' ','%20'), file=overlaps)
                           print('Sky View Query:', file=overlaps)
                           print(str('http://skyview.gsfc.nasa.gov/cgi-bin/runquery.pl?Interface=quick&Position='+RA[l]+' '+DEC[l]+'&SURVEY=Digitized+Sky+Survey&Size=0.167').replace(' ','%20'), file=overlaps)
                           print(' ', file=overlaps)
                           print('--------------------------------------------------------------------------------------------------------------------------------', file=overlaps)
                           teststring.append(SALTtarget[n]+RA[l]+DEC[l]+str(SALTstart[n])+str(SALTend[n])+str(GTIstart[m])+str(GTIend[m]))
                           success = 1
                           
   if success == 1:
      email = open('OverlapEMAIL','w')
      f = open('../emaillist')
      s = f.read()
      print('#! /bin/bash', file=email) 
      print('mail -s "Overlap Alert for observation date '+rundate+'" '+s.replace('\n',',').rstrip(',')+' < ./OverlapAlertInfo', file=email) 
   else:
      os.remove('OverlapEMAIL')   
