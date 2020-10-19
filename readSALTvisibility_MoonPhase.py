#! /usr/bin/env python

##############################################################
# Determine SALT visibility windows for a list of targets    #
##############################################################

import sys
import datetime
import calendar

######################################################################
# Function to read a file containing the list of files to be plotted #
######################################################################
def readfilenames(file):
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
      col = s[n].split(' ')
      # remove all list items that are unwanted
      while col.count('\n')>=1: 
         col.remove('\n')
      while col.count('')>=1: 
         col.remove('')
      columns = len(col)      
      # make a list of the files
      for k in range(columns): filenamelist.append(str(col[int(k)]).strip('\n'))        
   # FOR loop END
     
   # close the file
   f.close()
   
   # return values to main program 
   return filenamelist


########################################################################################
# Function to read a file containing source, RA and DEC and passes it to main program  #
########################################################################################
def readfile(datafile,date):
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
   UT = []
   angle = []
   sunalt = []
   moonalt = []
   #print datafile

   yr = int(date.year)
   mnth = int(date.month)
   day = int(date.day)
   
   # FOR loop START
   for n in range(1,rows):

           # read in each line and split the string into a list of entries
           # format : is,jj,isdt,hjd,gjd,dt,sunalt,alt,altmoon
           col = s[n].split(' ')
           # remove all list items that are unwanted
           while col.count('\t')>=1: 
               col.remove('\t')
           while col.count('')>=1: 
               col.remove('') 
           # add the column entries to the arrays   
           SAST = col[0]
           sunalt.append(col[5])
           angle.append(col[6])
           moonalt.append(col[7])
           UTtemp = SAST.split(':')
           UThrs = int(UTtemp[0])                  
           UTmin = int(UTtemp[1])
           UTsec = int(UTtemp[2])
           if UThrs < 12:
               UT.append(datetime.datetime(yr, mnth, day, UThrs, UTmin)-datetime.timedelta(hours=2)+datetime.timedelta(days=1))
           else:
               UT.append(datetime.datetime(yr, mnth, day, UThrs, UTmin)-datetime.timedelta(hours=2))    
   # FOR loop END
     
   # close the file
   f.close()
   
   # return values to main program 
   return UT, angle, sunalt, moonalt
   
   
####################
##################
#  MAIN PROGRAM  #
##################
####################
if __name__=='__main__':
   _nargs = len(sys.argv)
   if _nargs == 1:
      stop = raw_input("Enter the date where to stop (CCYY MM DD):  ")
      stops = stop.split(' ')
      stopdatey = int(stops[0])
      stopdatem = int(stops[1])
      stopdated = int(stops[2])
      mintrack = raw_input("Enter the minimum tracklength required (in hours):  ")
      mintrack = float(mintrack)

   else:
      stopdatey = int(sys.argv[1])
      stopdatem = int(sys.argv[2])
      stopdated = int(sys.argv[3])
      mintrack = float(sys.argv[4])
     
      
   target = readfilenames('targetsDONE')
  
   startdate = datetime.date.today()
   stopdate = datetime.date(stopdatey,stopdatem,stopdated)
   oneday = datetime.timedelta(days=1)
   
   newmoon = datetime.datetime(2011,6,1,21,3,0)
   lunarmonth = 29.53 
   
   results = open('results','w')

   for n in range(len(target)):       
       date = startdate   
       
       while date <= stopdate:
           time = []
           moon = []
           filename = 'outputfile'+str(target[n])+'_'+str(date)
           UT, angle, sunalt, moonalt = readfile(filename,date)

           if len(UT) > 0:
               lunarphase = ((UT[0] - newmoon).days+float((UT[0] - newmoon).seconds)/(24*3600))/lunarmonth
               lunarcycle = lunarphase-int(lunarphase)

               if lunarcycle < 0.5 :
                   moonphase = int(round(100*2*lunarcycle))
               else:
                   moonphase = int(round(100*abs(2*(1-lunarcycle))))
                        
#           if len(UT) > 0:
#               print UT[0], UT[-1]

           for i in range(len(UT)):
               if float(angle[i]) > 47 and float(angle[i]) < 59 and float(sunalt[i]) < -18:
                  time.append(UT[i])
                  if float(moonalt[i]) > 0:
                      moon.append('up')
                  else:
                      moon.append('down')   
           
           flag = 0
               
           if len(time)>0:           
               for j in range(1,len(time)):          
                  if time[j] - time[j-1] > datetime.timedelta(hours=1):
                      track = (time[j-1] - time[0])
                      tracklength = float(track.seconds)
                      if tracklength/3600 > mintrack:
                          if moon[0] == 'up':
                              moonrise = 'already up'
                          if moon[j-1] == 'up':
                              moonset = 'still up'
                          if moon[0] == 'down':
                              moonrise = 'already down'
                          if moon[j-1] == 'down':
                              moonset = 'still down'           
                          for k in range(1,j-1):
                              if moon[k] == 'up' and moon[k-1] == 'down':
                                  moonrise = time[k].time()
                              elif moon[k] == 'down' and moon[k-1] == 'up':
                                  moonset = time[k].time()
                          print(target[n], '\t', time[0].date(), '\t', time[0].time(), '\t', time[j-1].time(), '\t', 'duration', int(tracklength/60) ,'min on east track', '	', 'moon = ', moonphase,'%', '\t', 'Rise: ', moonrise, '  Set: ', moonset, file=results)
                          print(target[n], '\t', time[0].date(), '\t', time[0].time(), '\t', time[j-1].time(), '\t', 'duration', int(tracklength/60) ,'min on east track', '	', 'moon = ', moonphase,'%', '\t', 'Rise: ', moonrise, '  Set: ', moonset)
                      track = (time[-1] - time[j])
                      tracklength = float(track.seconds)
                      if tracklength/3600 > mintrack:
                          if moon[j] == 'up':
                              moonrise = 'already up'
                          if moon[-1] == 'up':
                              moonset = 'still up'
                          if moon[j] == 'down':
                              moonrise = 'already down'
                          if moon[-1] == 'down':
                              moonset = 'still down'           
                          for k in range(j+1,len(time)):
                              if moon[k] == 'up' and moon[k-1] == 'down':
                                  moonrise = time[k].time()
                              elif moon[k] == 'down' and moon[k-1] == 'up':
                                  moonset = time[k].time()
                          print(target[n], '\t', time[j].date(), '\t', time[j].time(), '\t', time[-1].time(), '\t', 'duration', int(tracklength/60) ,'min on west track', '	', 'moon = ', moonphase,'%', '\t', 'Rise: ', moonrise, '  Set: ', moonset, file=results)
                          print(target[n], '\t', time[j].date(), '\t', time[j].time(), '\t', time[-1].time(), '\t', 'duration', int(tracklength/60) ,'min on west track', '	', 'moon = ', moonphase,'%', '\t', 'Rise: ', moonrise, '  Set: ', moonset)
                      flag = 1
                      
               if flag == 0:
                  track = (time[-1] - time[0])
                  tracklength = float(track.seconds)
                  if tracklength/3600 > mintrack:
                      if moon[0] == 'up':
                          moonrise = 'already up'
                      if moon[-1] == 'up':
                          moonset = 'still up'
                      if moon[0] == 'down':
                          moonrise = 'already down'
                      if moon[-1] == 'down':
                          moonset = 'still down'           
                      for k in range(1,len(time)):
                          if moon[k] == 'up' and moon[k-1] == 'down':
                              moonrise = time[k].time()
                          elif moon[k] == 'down' and moon[k-1] == 'up':
                              moonset = time[k].time()
                      print(target[n], '\t', time[0].date(), '\t', time[0].time(), '\t', time[-1].time(), '\t', 'duration', int(tracklength/60) ,'min', '	', 'moon = ', moonphase,'%', '\t', 'Rise: ', moonrise, '  Set: ', moonset, file=results)
                      print(target[n], '\t', time[0].date(), '\t', time[0].time(), '\t', time[-1].time(), '\t', 'duration', int(tracklength/60) ,'min', '	', 'moon = ', moonphase,'%', '\t', 'Rise: ', moonrise, '  Set: ', moonset)
  
           date += oneday   
       print('------------------------------------------------------'    , file=results)   
