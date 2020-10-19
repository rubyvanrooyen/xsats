#! /usr/bin/env python

###########################################################################################################################################################
#  readfile is a program to read in a NUSTAR weekly schedule webfile (txt format) and print parameters for SALTVisibilityCalculator to an output file
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
dateobsend = []
dateobsstart = []

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
   missiondaybegin = []
   missionyearbegin = []
   missiondayend = []
   missionyearend = []
   gtibegin = []
   gtiend = []
   flagupcoming = 0
   flagtable = 0
   row=0
      
   # read in the file (as a list of lines for which each line is a string) 
   s = f.readlines()
   rows = len(s)
   
    
   # FOR loop START
   for n in range(rows):
      # read in each line and split the string into a list of entries
      col = s[n].split('</td><td>')

      # each row in the table contains all info per source.

      if len(col) > 1:
         source.append(col[3])
         ra.append(col[4].replace('nan','0'))
         dec.append(col[5].replace('nan','0'))  
         splitmissiondays = ((col[0]).split('<td>')[1]).split(':')
         missionyearbegin.append(splitmissiondays[0])               
         missiondaybegin.append(splitmissiondays[1])                  
         gtibegin.append(splitmissiondays[2]+':'+splitmissiondays[3]+':'+splitmissiondays[4])  
         splitmissiondays = ((col[1]).split(':'))
         missionyearend.append(splitmissiondays[0])               
         missiondayend.append(splitmissiondays[1])                  
         gtiend.append(splitmissiondays[2]+':'+splitmissiondays[3]+':'+splitmissiondays[4])                    

   # FOR loop END
               
   # close the file
   f.close()
   
   # return values to main program 
   return source, ra, dec, missiondaybegin, missionyearbegin, gtibegin, missiondayend, missionyearend, gtiend

#################
#  MAIN PROGRAM #
#################
if __name__=='__main__':
   _nargs = len(sys.argv)
   if _nargs == 1:
      file = raw_input("Enter the name of the NUSTAR webfile:  ")
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
   output = open(outfile+'_NUSTARoutput','w')   
   source, ra, dec, missiondaybegin, missionyearbegin, gtibegin, missiondayend, missionyearend, gtiend = readfile(file)  
   
   fjdmem = 0
   
   for k in range(len(source)):
       # Determine the start day, month and year from the inputs
       dateobsstart.append(datetime.date(int(missionyearbegin[k]),1,1)+(int(missiondaybegin[k])-1)*oneday)
       date = str(dateobsstart[k]).split('-')
       startyear.append(date[0])
       startmonth.append(date[1])
       startday.append(date[2])
       startdate.append(datetime.date(int(startyear[k]), int(startmonth[k]), int(startday[k])))

       # Determine the starttime (hh:mm:ss) from the inputs
       gtibeginsplit = str(gtibegin[k]).split(':')
       starthrs.append(int(gtibeginsplit[0]))
       startmins.append(int(gtibeginsplit[1]))
       startsecs.append(int(float(gtibeginsplit[2])))

       # Determine the end day, month and year from the inputs
       dateobsend.append(datetime.date(int(missionyearend[k]),1,1)+(int(missiondayend[k])-1)*oneday)
       date = str(dateobsend[k]).split('-')
       endyear.append(date[0])
       endmonth.append(date[1])
       endday.append(date[2])
       enddate.append(datetime.date(int(endyear[k]), int(endmonth[k]), int(endday[k])))

       # Determine the end time (hh:mm:ss) from the inputs
       gtiendsplit = str(gtiend[k]).split(':')
       endhrs.append(int(gtiendsplit[0]))
       endmins.append(int(gtiendsplit[1]))
       endsecs.append(int(float(gtiendsplit[2])))

       startGTI.append(datetime.datetime(int(startyear[k]),int(startmonth[k]),int(startday[k]),int(starthrs[k]),int(startmins[k]),int(startsecs[k])))
       endGTI.append(datetime.datetime(int(endyear[k]),int(endmonth[k]),int(endday[k]),int(endhrs[k]),int(endmins[k]),int(endsecs[k])))
       duration.append((endGTI[k]-startGTI[k]).days*24*60*60 + (endGTI[k]-startGTI[k]).seconds)

       # Determine the RA (hh:mm:ss) from the inputs
       rasplit = str(ra[k])
       RAhrs.append(int(float(rasplit)*24/360))
       RAmins.append(int((float(rasplit)*24/360-RAhrs[k])*60))
       RAsecs.append(round((((float(rasplit)*24/360-RAhrs[k])*60)-RAmins[k])*60,1))
       
       # Determine the DEC (sign & deg:':") from the inputs
       decsplit = str(dec[k])
       DECdegs = abs(float(decsplit))
       if float(decsplit) < 0 :
           DECsign.append(str('-'))
       else :
           DECsign.append(str('+'))           
       DECdeg.append(int(DECdegs))
       DECarcmins.append(int((DECdegs-DECdeg[k])*60))
       DECarcsecs.append(round(((DECdegs-DECdeg[k])*60-DECarcmins[k])*60,1))
      
            
       # calculate START mean julian day number (mjd) and geocentric julian day (gjd):
       iyr=int(startyear[k])
       mon=int(startmonth[k])+1
       if int(startmonth[k]) <= 2 :
           iyr=int(startyear[k])-1
           mon=int(startmonth[k])+13	
       jd=int((36525*iyr)/100)+int((306001*mon)/10000)+(int(startday[k]))+1720981
       jut=3600*int(starthrs[k])+60*(int(startmins[k]))+float(startsecs[k])
       fjd=float(jut)/86400+0.50
       startgjd.append(float(jd+fjd))
       startmjd=startgjd[k]-2400000.5 
       
       # calculate END mean julian day number (mjd) and geocentric julian day (gjd):
       jd=startgjd[k]
       jut=float(duration[k])
       fjd=float(jut)/86400
       endgjd.append(float(jd+fjd))
       endmjd=endgjd[k]-2400000.5
       nextday = startdate[k]+int(endgjd[k]-startgjd[k])*oneday
       enddate.append(datetime.date(nextday.year, nextday.month, nextday.day))



   listnustar = open('listnustar','w') 
   targets = open('nustar_targets','w')
   gtis = open('nustar_gti','w')      

   listlist = []
   targetlist = []
   
# outputs for Steve Potters IDL routines   
   for k in range(len(source)):
       if ((observationdate >= startdate[k] and observationdate <= enddate[k]) or (observationdatem >= startdate[k] and observationdatem <= enddate[k])) and int(DECsign[k]+'1')*DECdeg[k] < 20:
           print(source[k], file=output)
           print(RAhrs[k],RAmins[k],int(float(RAsecs[k])), file=output)
           print(DECsign[k]+str(DECdeg[k]),DECarcmins[k],int(float(DECarcsecs[k])), file=output)
           print(2000, file=output)
           print(0, file=output)
           print(0, file=output)
           print(0, file=output)
           print(0, file=output)
           print('NUSTAR', file=output)
           print(startgjd[k], file=output)
           print(endgjd[k], file=output)
           print('', file=output)
           
           if len(listlist)==0 or (source[k] not in listlist):
               print(source[k],'\t',RAhrs[k],RAmins[k],int(float(RAsecs[k])),str(DECsign[k])+str(DECdeg[k]),DECarcmins[k],int(float(DECarcsecs[k])), file=listnustar)
               listlist.append(source[k])
           
           
           if (startGTI[k] >= observationdatenoon and startGTI[k] <= observationdatemnoon) or (endGTI[k] >= observationdatenoon and endGTI[k] <= observationdatemnoon) or (startGTI[k] <= observationdatenoon and endGTI[k] >= observationdatemnoon):
# OUTPUT for SALTvisibility.py routine to determine SALT observability windows
               if len(targetlist)==0 or (source[k] not in targetlist):
                   print(source[k],'\t',RAhrs[k],RAmins[k],RAsecs[k],'\t',str(DECsign[k])+str(DECdeg[k]),DECarcmins[k],DECarcsecs[k],'\t','2000', file=targets)
                   targetlist.append(source[k])
# OUTPUT for GTIvsSALT.py routine to determine overlaps
               print(source[k],'\t',str(startGTI[k]).replace('-',':').replace(' ',':'),'\t',str(endGTI[k]).replace('-',':').replace(' ',':'),'\t',duration[k],'\t','NUSTAR', file=gtis)
