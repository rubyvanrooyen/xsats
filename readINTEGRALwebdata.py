#! /usr/bin/env python

###########################################################################################################################################################
#  readfile is a program to read in a INTEGRAL weekly schedule webfile (txt format) and print parameters for SALTVisibilityCalculator to an output file
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
   pi = []
   flag = 0
   row=0
      
   # read in the file (as a list of lines for which each line is a string) 
   s = f.readlines()
   rows = len(s)
   
    
   # FOR loop START
   for n in range(rows):
      col=''
      # read in each line and split the string into a list of entries
      col0 = s[n].replace('<td class="">','')
      col1 = col0.replace('<td class="number ">','')
      col2 = col1.replace('<td class="number current">','')
      col3 = col2.replace('<td class="current">','')
      col4 = col3.replace('</td>','')
      col = col4.replace('  ','')
                       
      if col == '</body>\n':
          flag = 0

      if flag == 0 and str(col) == '<th>Rev</th>\n':
          flag = 1
          row=-32

      if flag == 1:
                  #print n, row, col
                  if str(col)[:18]  =='\t<div class="too">':
                      row = row-2
                  if row==6:
                      sourcetemp0 = col.split('\t')
                      sourcetemp1 = sourcetemp0[1].split('\n')
                      source.append(sourcetemp1[0]) 
                  if row==21:
                      ra.append(col)
                  if row==22:
                      dec.append(col)   
                  if row==1:
                      startsplit = col.split(' ')
                      if len(startsplit) > 1: 
                          datesplit = startsplit[0].split('-')
                          timesplit = startsplit[1].split(':')
                          year.append(datesplit[0])   
                          month.append(datesplit[1])               
                          day.append(datesplit[2])
                          starthrs.append(timesplit[0])
                          startmins.append(timesplit[1])
                          startsecs.append(timesplit[2])   
                  if row==3:
                      duration.append(col)
                  if row==32:
                      pi.append(col.replace('\n',''))           
                  if row == 59:
                      row=0
                      
      row = row+1      
          
                      
   # FOR loop END
               
   # close the file
   f.close()
   
   # return values to main program 
   return source, ra, dec, year, month, day, starthrs, startmins, startsecs , duration, pi, flag,row,s, col

#################
#  MAIN PROGRAM #
#################
if __name__=='__main__':
   _nargs = len(sys.argv)
   if _nargs == 1:
      file = raw_input("Enter the name of the INTEGRAL webfile:  ")
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
   output = open(outfile+'_INTEGRALoutput','w')   
   source, ra, dec, year, month, day, starthrs, startmins, startsecs , duration, pi, flag,row,s,col = readfile(file)
   
   for k in range(len(source)):

       startdate.append(datetime.date(int(year[k]), int(month[k]), int(day[k])))  
       
       # Determine the RA (hh:mm:ss) from the inputs
       rasplit = str(ra[k]).split(':')
       RAhrs.append(rasplit[0])
       RAmins.append(rasplit[1])
       RAsecs.append(round(float(rasplit[2]),1))
       
       # Determine the DEC (sign & deg:':") from the inputs
       decsplit = str(dec[k]).split(':')
       DECdegs = abs(float(decsplit[0]))
       if float(decsplit[0]) < 0 :
           DECsign.append(str('-'))
       else :
           DECsign.append(str('+'))           
       DECdeg.append(int(DECdegs))
       DECarcmins.append(decsplit[1])
       DECarcsecs.append(round(float(decsplit[2]),1))
            
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
                
   listintegral = open('listintegral','w')
   targets = open('integral_targets','w')
   gtis = open('integral_gti','w')   

   listlist = []
   targetlist = []               
   
# outputs for Steve Potters IDL routines 
   for k in range(len(source)):
       non = 0
       nontargets = source[k].split(' ')
       if nontargets[0] == 'GPS':
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
           print('INTEGRAL', file=output)
           print(startgjd[k], file=output)
           print(endgjd[k], file=output)
           print(pi[k], file=output)
           
           if len(listlist)==0 or (source[k] not in listlist):
               print(source[k],'\t',RAhrs[k],RAmins[k],int(float(RAsecs[k])),str(DECsign[k])+str(DECdeg[k]),DECarcmins[k],int(float(DECarcsecs[k])), file=listintegral) 
               listlist.append(source[k])
           
           
           if (startGTI[k] >= observationdatenoon and startGTI[k] <= observationdatemnoon) or (endGTI[k] >= observationdatenoon and endGTI[k] <= observationdatemnoon) or (startGTI[k] <= observationdatenoon and endGTI[k] >= observationdatemnoon):           
# OUTPUT for SALTvisibility.py routine to determine SALT observability windows
               if len(targetlist)==0 or (source[k] not in targetlist):
                   print(source[k],'\t',RAhrs[k],RAmins[k],RAsecs[k],'\t',str(DECsign[k])+str(DECdeg[k]),DECarcmins[k],DECarcsecs[k],'\t','2000', file=targets)
                   targetlist.append(source[k])
# OUTPUT for GTIvsSALT.py routine to determine overlaps
               print(source[k],'\t',str(startGTI[k]).replace('-',':').replace(' ',':'),'\t',str(endGTI[k]).replace('-',':').replace(' ',':'),'\t',duration[k],'\t','INTEGRAL', file=gtis)
