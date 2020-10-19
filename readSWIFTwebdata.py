#! /usr/bin/env python

###########################################################################################################################################################
#  readfile is a program to read in a SWIFT weekly schedule webfile (txt format) and print parameters for SALTVisibilityCalculator to an output file
###########################################################################################################################################################

import sys
import datetime
import calendar
oneday = datetime.timedelta(days=1)

# Start with empty lists for the Information required by SALTVisibilityCalculator
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
startGTI = []
endGTI = [] 
duration = []

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
   gtiend = []
   flag = 0
   row = 0
   
      
   # read in the file (as a list of lines for which each line is a string) 
   s = f.readlines()
   rows = len(s)
   
    
   # FOR loop START
   for n in range(rows):
      col = []
      # read in each line and split the string into a list of entries
      col = s[n].split(';')
      
      if str(col[0]).replace('\t','')[:10] == "<tr class=":
          row = 0
          if str(col[0]).replace('\t','')[:19] == "<tr class='header'>":
              flag = 1  
              row = -1 
      if flag == 1:
      # 12 different rows contain different info per source.
          if row==5:
              sourcetemp0 = str(col[2]).replace('&nbsp','')
              source.append(sourcetemp0)
          if row==6:
              ra.append(str(col[1]).replace('&nbsp',''))
          if row==7:
              dec.append(str(col[1]).replace('&nbsp',''))                  
          if row==1:
              splitmission = (str(col[1]).replace('&nbsp','')).split(' ')
              dateobs.append(splitmission[0])         
              gtibegin.append(splitmission[1])  
          if row==2:
              splitmission = (str(col[1]).replace('&nbsp','')).split(' ')        
              gtiend.append(splitmission[1])       
          if row==14:
              if (str(col[0]).replace('\t','')).replace('\n','') == '</table>':
                  flag = 0
              else: row=0
    
                                     
      row = row+1
                       
   # FOR loop END
               
   # close the file
   f.close()
   
   # return values to main program 
   return source, ra, dec, dateobs, gtibegin, gtiend

#################
#  MAIN PROGRAM #
#################
if __name__=='__main__':
   _nargs = len(sys.argv)
   if _nargs == 1:
      file = raw_input("Enter the name of the SWIFT webfile:  ")
      # 2011-04-28
      obsdate = raw_input("Enter the observation date:  ")
   else:
      file = sys.argv[1]
      obsdate = sys.argv[2]

   splitdate = obsdate.split('-')

#   observationdate = datetime.date(2009,5,31) 
   observationdate = datetime.date(int(splitdate[0]),int(splitdate[1]),int(splitdate[2]))
   observationdatem = observationdate+oneday
   observationdatenoon = datetime.datetime(int(splitdate[0]),int(splitdate[1]),int(splitdate[2]),12,0,0)
   observationdatemnoon = observationdatenoon+oneday

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
   output = open(outfile+'_SWIFToutput','w')   
   source, ra, dec, dateobs, gtibegin, gtiend = readfile(file)
   
   for k in range(len(source)):
       # Determine the day, month and year from the inputs
       date = str(dateobs[k]).split('-')
       startyear.append(date[0])
       startmonth.append(date[1])
       startday.append(date[2])
       startdate.append(datetime.date(int(startyear[k]), int(startmonth[k]), int(startday[k])))
       
       # Determine the RA (hh:mm:ss) from the inputs
       RAhrs.append(int(float(ra[k])*24/360))
       RAmins.append(int((float(ra[k])*24/360-RAhrs[k])*60))
       RAsecs.append(round((((float(ra[k])*24/360-RAhrs[k])*60)-RAmins[k])*60,1))
       
       # Determine the DEC (sign & deg:':") from the inputs
       DECdegs = abs(float(dec[k]))
       if float(dec[k]) < 0 :
           DECsign.append(str('-'))
       else :
           DECsign.append(str('+'))           
       DECdeg.append(int(DECdegs))
       DECarcmins.append(int((DECdegs-DECdeg[k])*60))
       DECarcsecs.append(round(((DECdegs-DECdeg[k])*60-DECarcmins[k])*60,1))
       
       # Determine the starttime (hh:mm:ss) from the inputs
       gtibeginsplit = str(gtibegin[k]).split(':')
       starthrs.append(int(gtibeginsplit[0]))
       startmins.append(int(gtibeginsplit[1]))
       startsecs.append(int(gtibeginsplit[2]))
       
       # Determine the endtime (hh:mm:ss) from the inputs
       gtiendsplit = str(gtiend[k]).split(':')       
       endhrs.append(int(gtiendsplit[0]))
       endmins.append(int(gtiendsplit[1]))
       endsecs.append(int(gtiendsplit[2]))
       
       # calculate START mean julian day number (mjd) and geocentric julian day (gjd):
       iyr=int(startyear[k])
       mon=int(startmonth[k])+1
       if int(startmonth[k]) <= 2 :
           iyr=int(startyear[k])-1
           mon=int(startmonth[k])+13	
       jd=int((36525*iyr)/100)+int((306001*mon)/10000)+int(startday[k])+1720981
       jut=3600*starthrs[k]+60*startmins[k]+startsecs[k]
       jutmem = jut
       fjd=float(jut)/86400+0.50
       startgjd.append(float(jd+fjd))
       #print('startGJD: ',startgjd[k])
       startmjd=startgjd[k]-2400000.5 
       
       # calculate END mean julian day number (mjd) and geocentric julian day (gjd):
       iyr=int(startyear[k])
       mon=int(startmonth[k])+1
       if int(startmonth[k]) <= 2 :
           iyr=int(startyear[k])-1
           mon=int(startmonth[k])+13	
       jd=int((36525*iyr)/100)+int((306001*mon)/10000)+int(startday[k])+1720981
       jut=3600*endhrs[k]+60*endmins[k]+endsecs[k]
       fjd=float(jut)/86400+0.50
       if jut <= jutmem:
           endgjd.append(float(jd+fjd+1))
           nextday = startdate[k]+oneday
           enddate.append(datetime.date(nextday.year, nextday.month, nextday.day))
       else:
           endgjd.append(float(jd+fjd))
           enddate.append(datetime.date(startdate[k].year, startdate[k].month, startdate[k].day))
       endmjd=endgjd[k]-2400000.5   
       #print('endGJD: ',endgjd[k]) 

       duration.append((endgjd[k]-startgjd[k])*24*60*60)
       startGTI.append(datetime.datetime(int(startyear[k]),int(startmonth[k]),int(startday[k]),starthrs[k],startmins[k],startsecs[k]))
       endGTI.append(startGTI[k] + datetime.timedelta(seconds=duration[k]))
                     
   listswift = open('listswift','w')
   targets = open('swift_targets','w')
   gtis = open('swift_gti','w')  

   listlist = []
   targetlist = []             

# outputs for Steve Potters IDL routines 
   for k in range(len(source)):
       non = 0
       if source[k].count('saa')>=1 or source[k].count('swift_gal_survey')>=1 or source[k].count('SGWGS')>=1 or source[k].count('SBS2 J')>=1: 
           non = 1
       if ((observationdate >= startdate[k] and observationdate <= enddate[k]) or (observationdatem >= startdate[k] and observationdatem <= enddate[k])) and int(DECsign[k]+'1')*DECdeg[k] < 20 and non == 0:
           print(source[k], file=output)
           print(RAhrs[k],RAmins[k],int(RAsecs[k]), file=output)
           print(DECsign[k]+str(DECdeg[k]),DECarcmins[k],int(DECarcsecs[k]), file=output)
           print(2000, file=output)
           print(0, file=output)
           print(0, file=output)
           print(0, file=output)
           print(0, file=output)
           print('SWIFT', file=output)
           print(startgjd[k], file=output)
           print(endgjd[k], file=output)
           print('-', file=output)
           
           if len(listlist)==0 or (source[k] not in listlist):
               print(source[k],'\t',RAhrs[k],RAmins[k],int(float(RAsecs[k])),str(DECsign[k])+str(DECdeg[k]),DECarcmins[k],int(float(DECarcsecs[k])), file=listswift)
               listlist.append(source[k])
         

           if (startGTI[k] >= observationdatenoon and startGTI[k] <= observationdatemnoon) or (endGTI[k] >= observationdatenoon and endGTI[k] <= observationdatemnoon) or (startGTI[k] <= observationdatenoon and endGTI[k] >= observationdatemnoon): 
# OUTPUT for SALTvisibility.py routine to determine SALT observability windows
               if len(targetlist)==0 or (source[k] not in targetlist):
                   print(source[k],'\t',RAhrs[k],RAmins[k],RAsecs[k],'\t',str(DECsign[k])+str(DECdeg[k]),DECarcmins[k],DECarcsecs[k],'\t','2000', file=targets)
                   targetlist.append(source[k])
# OUTPUT for GTIvsSALT.py routine to determine overlaps
               print(source[k],'\t',str(startGTI[k]).replace('-',':').replace(' ',':'),'\t',str(endGTI[k]).replace('-',':').replace(' ',':'),'\t',duration[k],'\t','SWIFT', file=gtis)
