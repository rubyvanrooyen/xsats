#! /usr/bin/env python

###########################################################################################################################################################
#  readfile is a program to read in a XMM weekly schedule webfile (txt format) and print parameters for SALTVisibilityCalculator to an output file
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
endhrs = []
endmins = []
endsecs = []
startmjd = []
endmjd = []
startgjd = []
endgjd = []
number = 0
cols = []
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
   year = []
   month = []
   day = []
   starthrs = []
   startmins = []
   startsecs = []    
   duration = []
   flag = 0
   row = 0
   
      
   # read in the file (as a list of lines for which each line is a string) 
   s = f.readlines()
   rows = len(s)
   
    
   # FOR loop START
   for n in range(rows):
      # read in each line and split the string into a list of entries
      col=''
      # read in each line and split the string into a list of entries
      col0 = s[n].split('<TD ALIGN="CENTER"> <B>')
      if len(col0)>1:
          col1 = col0[1].split('<')
          col = col1[0]
      else:
          col0 = s[n].split('<TD COLSPAN="2" ALIGN="CENTER"> <B>')
          if len(col0)>1:
              col1 = col0[1].split('<')
              col = col1[0]  
          else:
              col0 = s[n].split('<TH COLSPAN="7" BGCOLOR="#ADD8E6" ALIGN="CENTER">')
              if len(col0)>1:
                  col1 = col0[1].split('<')
                  col = col1[0]
              else:
                  col0 = s[n].split('<TH><B><FONT COLOR="#FFFFFF">')
                  if len(col0)>1:
                      col1 = col0[1].split('<')
                      col = col1[0]
                  else:
                      col = col0[0]
      row = row+1
      if len(col) >= 1:   
         if str(col).strip(' ') == 'Target_Name':
             flag = 1
             row = -28
         if col == '</BODY>\n':
             flag = 0    
         if flag == 1 :
             if row == 8:   
                 source.append(col.strip(' ')) 
             if row == 9:                      
                 ra.append(col)
             if row == 10:
                 dec.append(col)
             if row == 17:                          
                 startsplit = col.split('@')
                 datesplit = startsplit[0].split('-')
                 timesplit = startsplit[1].split(':')                 
                 year.append(datesplit[0])   
                 month.append(datesplit[1])               
                 day.append(datesplit[2])
                 starthrs.append(timesplit[0])
                 startmins.append(timesplit[1])
                 startsecs.append(timesplit[2])
             if row == 16:     
                 dur = col.split(' ')
                 while dur.count('')>=1: 
                     dur.remove('') 
                 duration.append(dur[0])
             if str(col).strip(' ') == 'End_of_Obs':
                 row = 0
      cols.append(col)                                         
       
   # FOR loop END
               
   # close the file
   f.close()
   
   # return values to main program 
   return source, ra, dec, year, month, day, starthrs, startmins, startsecs , duration,cols,s

#################
#  MAIN PROGRAM #
#################
if __name__=='__main__':
   _nargs = len(sys.argv)
   if _nargs == 1:
      file = raw_input("Enter the name of the XMM webfile:  ")
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
   output = open(outfile+'_XMMoutput','w')   
   source, ra, dec, year, month, day, starthrs, startmins, startsecs , duration,col,s = readfile(file)
   
   fjdmem = 0
   
   for k in range(len(source)):
   
       startdate.append(datetime.date(int(year[k]), int(month[k]), int(day[k])))       

       # Determine the RA (hh:mm:ss) from the inputs
       rasplit = str(ra[k]).split(':')
       RAhrs.append(rasplit[0])
       RAmins.append(rasplit[1])
       RAsecs.append(rasplit[2])
       
       # Determine the DEC (sign & deg:':") from the inputs
       decsplit = str(dec[k]).split(':')
       DECdegs = abs(float(decsplit[0]))
       if float(decsplit[0]) < 0 :
           DECsign.append(str('-'))
       else :
           DECsign.append(str('+'))           
       DECdeg.append(int(DECdegs))
       DECarcmins.append(decsplit[1])
       DECarcsecs.append(decsplit[2])
            
       # calculate START mean julian day number (mjd) and geocentric julian day (gjd):
       iyr=int(year[k])
       mon=int(month[k])+1
       if int(month[k]) <= 2 :
           iyr=int(year[k])-1
           mon=int(month[k])+13	
       jd=int((36525*iyr)/100)+int((306001*mon)/10000)+int(day[k])+1720981
       jut=3600*int(starthrs[k])+60*int(startmins[k])+int(startsecs[k])
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

       duration[k] = float(duration[k])
       startGTI.append(datetime.datetime(int(year[k]),int(month[k]),int(day[k]),int(starthrs[k]),int(startmins[k]),int(startsecs[k])))
       endGTI.append(startGTI[k] + datetime.timedelta(seconds=duration[k]))
       
   listxmm = open('listxmm','w')   
   targets = open('xmm_targets','w')
   gtis = open('xmm_gti','w')

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
           print('XMM', file=output)
           print(startgjd[k], file=output)
           print(endgjd[k], file=output)
           print('-', file=output)
           
           if len(listlist)==0 or (source[k] not in listlist):
               print(source[k],'\t',RAhrs[k],RAmins[k],int(float(RAsecs[k])),str(DECsign[k])+str(DECdeg[k]),DECarcmins[k],int(float(DECarcsecs[k])), file=listxmm)
               listlist.append(source[k])
           

           if (startGTI[k] >= observationdatenoon and startGTI[k] <= observationdatemnoon) or (endGTI[k] >= observationdatenoon and endGTI[k] <= observationdatemnoon) or (startGTI[k] <= observationdatenoon and endGTI[k] >= observationdatemnoon):            
# OUTPUT for SALTvisibility.py routine to determine SALT observability windows
               if len(targetlist)==0 or (source[k] not in targetlist):
                   print(source[k],'\t',RAhrs[k],RAmins[k],RAsecs[k],'\t',str(DECsign[k])+str(DECdeg[k]),DECarcmins[k],DECarcsecs[k],'\t','2000', file=targets)
                   targetlist.append(source[k])
# OUTPUT for GTIvsSALT.py routine to determine overlaps
               print(source[k],'\t',str(startGTI[k]).replace('-',':').replace(' ',':'),'\t',str(endGTI[k]).replace('-',':').replace(' ',':'),'\t',duration[k],'\t','XMM', file=gtis)
