#! /usr/bin/env python

###########################################################################################################################################################
#  readfile is a program to read in a Gamma Ray Burst webfile (txt format) and print parameters for XSATS HTML to an output file
###########################################################################################################################################################

import sys
import datetime
import calendar
oneday = datetime.timedelta(days=1)

dateobs = []
startdate = []
startyear = []
startmonth = []
startday = []
enddate = []
endyear = []
endmonth = []
endday = []
RAhrs = []
RAmins = []
RAsecs = []
DECsign = []
DECdeg = []
DECarcmins = []
DECarcsecs = []
starthrs = []
startmins = []
startsecs = []
endhrs = []
endmins = []
endsecs = []
startmjd = []
endmjd = []
startgjd = []
endgjd = []
number = 0

#######################################
#      Function to read a datafile    #
#######################################
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
   
   # Start with empty lists for the Information required by SALTVisibilityCalculator
   source = []
   ra = []
   dec = []
   dateobs = []
   gtibegin = []
   flag = 0
   row = 0
   
   chart = []
      
   # read in the file (as a list of lines for which each line is a string) 
   s = f.readlines()
   rows = len(s)
   
    
   # FOR loop START
   for n in range(rows):
      # read in each line and split the string into a list of entries
      col = s[n]

      if str(col)[:18] == "<td><a href=other/" and flag == 0:
          source.append(str(col)[18:30])          
          row = 0
          
      if str(col)[:15] == "<td align=left>" and row == 1 and flag == 0:
          if str(col)[18] == '/' : 
              dateobs.append((str(col)[15:23]))
          else:
              dateobs.append('00/01/01')         

      if str(col)[:15] == "<td align=left>" and row == 2 and flag == 0:              
          if str(col)[18] == ':' :
              gtibegin.append((str(col)[15:23]))
          else:
              gtibegin.append('00:00:00')  
      
      if str(col)[:16] == "<td align=right>" and row == 3 and flag == 0:       
          RAdeg = col.split('</td><td align=right>')
          if len(RAdeg) >= 2:    
              ra.append(str(RAdeg[0]).replace('<td align=right>',''))
              dec.append(str(RAdeg[1]))
          else:
              ra.append('0')
              dec.append('0')  
          flag = 1

      if str(col)[:16] == "<td align=right>" and row == 4 and flag == 0:       
          RAdeg = col.split('</td><td align=right>')
          if len(RAdeg) >= 2:    
              ra.append(str(RAdeg[0]).replace('<td align=right>',''))
              dec.append(str(RAdeg[1]))
          else:
              ra.append('0')
              dec.append('0')  
          flag = 1
          
      if str(col)[:21] == "<td><A HREF=notices_s" and flag == 1:
          images = col.split('</A> <A HREF=')
          for i in range(len(images)):
              if images[i][-11:] == 'FIELD_JPEG1':
                  chart.append(str(images[i][:-12]).replace('</A> <A HREF=notices_s/',''))
          # image at :  http://gcn.gsfc.nasa.gov/ + chart
                  flag = 2 
              elif images[i][-11:] == 'FIELD_JPEG2' and flag == 1:     
                  chart.append(str(images[i][:-12]).replace('</A> <A HREF=notices_s/',''))                 
                                     
      row = row+1
                       
   # FOR loop END
               
   # close the file
   f.close()
   
   # return values to main program 
   return source, ra, dec, dateobs, gtibegin, chart

#################
#  MAIN PROGRAM #
#################
if __name__=='__main__':
   _nargs = len(sys.argv)
   if _nargs == 1:
      file = 'swift_grbs.html'
   else:
      file = sys.argv[1]
      
#   observationdate = datetime.date(2009,6,8) 
   observationdate = datetime.date.today()
   observationdatem = observationdate+oneday

# Open the output files
   if int(observationdate.month)>=10 and int(observationdate.day)>=10:
       outfile = str(observationdate.year)+str(observationdate.month)+str(observationdate.day)   
   else:
       if int(observationdate.month)<10 and int(observationdate.day)>=10:
           outfile = str(observationdate.year)+'0'+str(observationdate.month)+str(observationdate.day)
       if int(observationdate.day)<10 and int(observationdate.month)>=10:
           outfile = str(observationdate.year)+str(observationdate.month)+'0'+str(observationdate.day)
       if int(observationdate.month)<10 and int(observationdate.day)<10:
           outfile = str(observationdate.year)+'0'+str(observationdate.month)+'0'+str(observationdate.day)            
   source, ra, dec, dateobs, gtibegin, chart = readfile(file)
   
   listgrb = open('listGRB','w')
   
   for k in range(len(source)):
       # Determine the day, month and year from the inputs
       date = str(dateobs[k]).split('/')
       startyear.append(int(date[0])+2000)
       startmonth.append(date[1])
       startday.append(date[2])
       startdate.append(datetime.date(int(startyear[k]), int(startmonth[k]), int(startday[k])))
       
       # Determine the RA (hh:mm:ss) from the inputs
       RAhrs.append(int(float(ra[k])*24/360))
       RAmins.append(int((float(ra[k])*24/360-RAhrs[k])*60))
       RAsecs.append((((float(ra[k])*24/360-RAhrs[k])*60)-RAmins[k])*60)
       
       # Determine the DEC (sign & deg:':") from the inputs
       DECdegs = abs(float(dec[k]))
       if float(dec[k]) < 0 :
           DECsign.append(str('-'))
       else :
           DECsign.append(str('+'))           
       DECdeg.append(int(DECdegs))
       DECarcmins.append(int((DECdegs-DECdeg[k])*60))
       DECarcsecs.append(((DECdegs-DECdeg[k])*60-DECarcmins[k])*60)
       
       # Determine the starttime (hh:mm:ss) from the inputs
       gtibeginsplit = str(gtibegin[k]).split(':')
       starthrs.append(int(gtibeginsplit[0]))
       startmins.append(int(gtibeginsplit[1]))
       startsecs.append(int(gtibeginsplit[2]))
              
       # calculate START mean julian day number (mjd) and geocentric julian day (gjd):
       iyr=int(startyear[k])
       mon=int(startmonth[k])+1
       if int(startmonth[k]) <= 2 :
           iyr=int(startyear[k])-1
           mon=int(startmonth[k])+13	
       jd=(36525*iyr)/100+(306001*mon)/10000+int(startday[k])+1720981
       jut=3600*starthrs[k]+60*startmins[k]+startsecs[k]
       jutmem = jut
       fjd=float(jut)/86400+0.50
       startgjd.append(float(jd+fjd))
       startmjd=startgjd[k]-2400000.5 

# outputs 
   for k in range(len(source)):     
           print(source[k],'\t',RAhrs[k],RAmins[k],int(float(RAsecs[k])),'\t',str(DECsign[k])+str(DECdeg[k]),DECarcmins[k],int(float(DECarcsecs[k])), '\t', chart[k], file=listgrb)
