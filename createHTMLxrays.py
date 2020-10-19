#! /usr/bin/env python

#################################################################################################
#           Generate the HTML for the website on which all information is displayed             #
#################################################################################################

import sys

#################################################################################################
# Function to read a file containing the list of targets to be observed by the X-ray satellites #
#################################################################################################
def readfile(inputfile, sourceid, sourcetype, sourcename):
   """Read in the input file per line and returns list of strings to main program """
   # Try to open the file and return an error if this fails
   try:
      f = open(inputfile,'r')
   except IOError:
      print('Failed to open '+file)
      print(inputfile, file=missfiles)
      return None

   filenamelist = []
   idname = []
 
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
   # FOR loop END
     
   entries = len(filenamelist)
   for j in range(entries): 
       for l in range(len(sourceid)):
           # Every even filename is a sourcename, and odd ones are coordinates
           count = 0
           for k in range(j):
               if str(filenamelist[j]) == str(filenamelist[k]):
                   count = count + 1
       
           if str(filenamelist[j]).replace('%2B','+').rstrip(' ') == str(sourceid[l].rstrip(' ')) and count < 1 :      
               ############################################################
               # Create the appropriate SIMBAD link using the Identifier  #
               ############################################################ 
               identifier = str(filenamelist[int(j)])   
               # format:  http://simbad.u-strasbg.fr/simbad/sim-id?output.format=ASCII&Ident=hd 1
               # FORMAT: <a href = "http://simbad.u-strasbg.fr/simbad/sim-id?Ident=4U1957%2B11 ">4U1957+11</a>
               print('<tr><th><a href = '+'"http://simbad.u-strasbg.fr/simbad/sim-id?Ident='+identifier+'">'+str(idname[int(j)])+'</a>', file=scriptHTML)
 
               ############################################################
               # Create the appropriate SIMBAD link using the Coordinates #
               ############################################################ 
               coords = str(filenamelist[int(j+1)])
               coord = (coords.replace('%2B','+')).lstrip(' ').split(' ')
               ra = coord[0] + ' ' + coord[1]+ ' ' + coord[2]
               dec = coord[3] + ' ' + coord[4]+ ' ' + coord[5]
               coordstring = ra+';'+dec
               # format:  http://simbad.u-strasbg.fr/simbad/sim-coo?output.format=HTML&Coord=12 30 +10 20&Radius=10&Radius.unit=arcmin
               print('<th><a href = '+'"http://simbad.u-strasbg.fr/simbad/sim-coo?output.format=HTML&Coord='+coords+'&Radius=2&Radius.unit=arcmin">'+coordstring+'</a>', file=scriptHTML)

               ################################################################################
               # Create SkyView link using the Coordinates to facilitate making finding chart #
               ################################################################################
               # format:  http://skyview.gsfc.nasa.gov/cgi-bin/runquery.pl?Interface=quick&Position=161.264962,%20-59.684517&SURVEY=dss2r
               print('<th><a href = '+'"http://skyview.gsfc.nasa.gov/cgi-bin/runquery.pl?Interface=quick&Position='+coords+'&SURVEY=Digitized+Sky+Survey&Size=0.167">'+'DSS image'+'</a>', file=scriptHTML)
               print('<th>'+sourcetype[l], file=scriptHTML)
               print('<th>'+sourcename[l], file=scriptHTML)
               print('<th>'+sourceid[l], file=scriptHTML)  
                  
   # close the file
   f.close()
   
   # return values to main program 
   return filenamelist, count

####################
##################
#  MAIN PROGRAM  #
##################
####################

if __name__=='__main__':
   _nargs = len(sys.argv)
   if _nargs == 1:
      day = raw_input("Which date ? (CCYYMMDD):  ")
   else:
      day = sys.argv[1]

   ########################
   # Determine latest GRB #
   ########################         
   grbID = []
   grbRA = []
   grbDEC = []
   grbCHART = []
         
   try:
      GRB = open('listGRB','r')
      g = GRB.readlines()
      if len(g) > 0:
      # FOR loop START
         for n in range(len(g)):
            # read in each line and split the string into a list of entries
            col = g[n].split(' \t ')
            while col.count('\n')>=1: 
               col.remove('\n')
            while col.count('')>=1: 
               col.remove('')      
            grbID.append(col[0].strip('\n'))
            grbRA.append(col[1].strip('\n'))
            grbDEC.append(col[2].strip('\n'))
            if len(col) > 3:
               grbCHART.append(col[3].strip('\n'))
            else:
               grbCHART.append('No Chart Available')         
      else:
         grbID.append('Not Available')
         grbRA.append('Not Available')
         grbDEC.append('Not Available')
         grbCHART.append('Not Available')
   except IOError:
         grbID.append('Not Available')
         grbRA.append('Not Available')
         grbDEC.append('Not Available')
         grbCHART.append('Not Available')

   ###################
   # Get SIMBADtypes #
   ###################         
   SIMBADtypes = open('SIMBADtypes','r')
   sourceid = []
   sourcetype = []
   sourcename = []
   
   s = SIMBADtypes.readlines() 
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
         sourceid.append(col[0].strip('\n'))
         sourcetype.append(col[1].strip('\n')) 
         if len(col)>= 3:          
            sourcename.append(col[2].strip('\n'))    
         else:
            sourcename.append('-')

      #########################
      # Open the output files #
      ######################### 
      scriptHTML = open('Xrays.html','w')
      missfiles = open('missfiles','w')
            
   ##########################################
   # Create HTML code INcluding SIMBAD info #
   ##########################################
      print('<html>', file=scriptHTML)
      print('<head>', file=scriptHTML)
      print('<body bgcolor=white>', file=scriptHTML)
      print('<center>', file=scriptHTML)
      print('<tr><a href = "http://www.saao.ac.za/~marissa/Xrays_day0.html">today</a>&nbsp;&nbsp;<a href = "http://www.saao.ac.za/~marissa/Xrays_day1.html">today+1</a>&nbsp;&nbsp;<a href = "http://www.saao.ac.za/~marissa/Xrays_day2.html">today+2</a>&nbsp;&nbsp;<a href = "http://www.saao.ac.za/~marissa/Xrays_day3.html">today+3</a>&nbsp;&nbsp;<a href = "http://www.saao.ac.za/~marissa/Xrays_day4.html">today+4</a>&nbsp;&nbsp;<a href = "http://www.saao.ac.za/~marissa/Xrays_day5.html">today+5</a>&nbsp;&nbsp;<a href = "http://www.saao.ac.za/~marissa/Xrays_day6.html">today+6</a>&nbsp;&nbsp;<p>', file=scriptHTML)
      print('<H1>Latest Gamma-Ray Burster</H1>', file=scriptHTML)

      print('<TABLE border="1" cellspacing="2">', file=scriptHTML)       
      print('<tr><th>&nbsp;SWIFT Trigger&nbsp;&nbsp;<th>&nbsp;RA&nbsp;&nbsp;<th>&nbsp;DEC&nbsp;<th>&nbsp;Field&nbsp;<th>&nbsp;Finder&nbsp;', file=scriptHTML)
      
      print('<tr><th><a href = '+'"http://gcn.gsfc.nasa.gov/other/'+grbID[0]+'">'+str(grbID[0])+'</a>', file=scriptHTML)
      print('<th>'+grbRA[0], file=scriptHTML)
      print('<th>'+grbDEC[0], file=scriptHTML)    
      if str(grbID[0])[0:6] == str(grbCHART[0])[14:20] :
          print('<th><a href = '+'"http://gcn.gsfc.nasa.gov/'+grbCHART[0]+'">'+str('JPEG')+'</a>', file=scriptHTML)
      else:
          print('<th>'+'not available', file=scriptHTML)     
      if grbRA[0]== 'Not Available' and grbDEC[0]== 'Not Available':
          print('<th>'+'not available', file=scriptHTML)
      else:    
          print('<th><a href = '+'"http://skyview.gsfc.nasa.gov/cgi-bin/runquery.pl?Interface=quick&Position='+grbRA[0]+' '+grbDEC[0].replace('+','%2B')+'&SURVEY=Digitized+Sky+Survey&Size=0.167">'+'10x10 DSS image'+'</a>', file=scriptHTML)
      print('</TABLE>' , file=scriptHTML)
      
      print('<H1>Xray satellite targets</H1>', file=scriptHTML)
      print('<H3>P.I. &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp  Target &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp   Black bars indicate possible SALT observation windows (SAST)</H3>', file=scriptHTML)
      print('<img src="Xray/'+day+'_NICERtoday.jpg"><p> <br>', file=scriptHTML)
      print('<img src="Xray/'+day+'_SWIFTtoday.jpg"><p> <br>', file=scriptHTML)
      print('<img src="Xray/'+day+'_Chan_XMM_suz_Int_today.jpg"><p> <br>', file=scriptHTML)
      print('</center>', file=scriptHTML)
      print('<TABLE border="1" cellspacing="2">', file=scriptHTML)
      print('<H1>List of all targets contained in the plots</H1>', file=scriptHTML)
      print('<tr><th><H2>&nbsp;TARGET&nbsp;name&nbsp;</H2><th><H2>&nbsp;Pointing &nbsp;Coordinates&nbsp;</H2><th><H2>&nbsp;Finder&nbsp;Chart&nbsp;</H2><th><H2>&nbsp;SIMBAD&nbsp;type&nbsp;</H2><th><H2>&nbsp;Name&nbsp;</H2><th><H2>&nbsp;SIMBAD&nbsp;ID&nbsp;</H2>', file=scriptHTML)
      print('<tr><th>&nbsp;(SIMBAD-link)&nbsp;<H3>&nbsp;</H3><th>&nbsp;(SIMBAD-link)&nbsp;<H3>&nbsp;[RA&nbsp;;&nbsp;DEC]&nbsp;</H3><th>&nbsp;(SkyViewQuery-link)&nbsp; <H3>&nbsp;(10x10&nbsp;arcmin)&nbsp;</H3><th>&nbsp;<th>&nbsp;<th>&nbsp;', file=scriptHTML)
      filenamelist,count = readfile('listall', sourceid, sourcetype, sourcename)     
      print('</TABLE>' , file=scriptHTML)
      print('<H2>Useful links:</H2><p>', file=scriptHTML)
      print('<tr><a href = "http://heasarc.gsfc.nasa.gov/docs/archive.html">HEASARC archives</a><p>', file=scriptHTML)
      print('<tr><a href = "http://irsa.ipac.caltech.edu/applications/DUST">Caltec IRSA DUST extinction calculator</a><p>', file=scriptHTML)
      print('<tr><a href = "http://gcn.gsfc.nasa.gov/swift_grbs.html">Swift Gamma Ray Burster ToO info</a><p>', file=scriptHTML)
      print('<H2>Links to the Online Schedules:</H2><p>', file=scriptHTML)
      print('<tr><a href = "https://www.swift.psu.edu/operations/obsSchedule.php">SWIFT</a><p>', file=scriptHTML)
      print('<tr><a href = "http://asc.harvard.edu/target_lists/stscheds/index.html">CHANDRA</a><p>', file=scriptHTML)
      print('<tr><a href = "https://www.cosmos.esa.int/web/xmm-newton/short-term-schedule">XMM-Newton</a><p>', file=scriptHTML)
      print('<tr><a href = "https://www.cosmos.esa.int/web/integral/schedule-information">INTEGRAL</a><p>', file=scriptHTML)
      print('<tr><a href = "https://heasarc.gsfc.nasa.gov/docs/nicer/schedule/nicer_sts_current.html">NICER</a><p>', file=scriptHTML)
      print('<tr><a href = "http://www.srl.caltech.edu/NuSTAR_Public/NuSTAROperationSite/Schedule.php">NuSTAR</a><p>', file=scriptHTML)
      print('<center>', file=scriptHTML)
      print('<H5>Plots generated using IDL code supplied by Stephen Potter</H5>', file=scriptHTML)
      print('<H5>Website generated by Marissa Kotze</H5>', file=scriptHTML)
      print('<H5>email : marissa@saao.ac.za</H5>', file=scriptHTML)
      print('</center>', file=scriptHTML)
      print('</body>', file=scriptHTML)
      print('</html>', file=scriptHTML)  
      missfiles.close()
      
   ##########################################
   # Create HTML code EXcluding SIMBAD info #
   ##########################################  
   else:
      scriptHTML = open('Xrays.html','w')
      missfiles = open('missfiles','w')
      print('<html>', file=scriptHTML)
      print('<head>', file=scriptHTML)
      print('<body bgcolor=white>', file=scriptHTML)
      print('<center>', file=scriptHTML)
      print('<tr><a href = "http://www.saao.ac.za/~marissa/Xrays_day0.html">today</a>&nbsp;&nbsp;<a href = "http://www.saao.ac.za/~marissa/Xrays_day1.html">today+1</a>&nbsp;&nbsp;<a href = "http://www.saao.ac.za/~marissa/Xrays_day2.html">today+2</a>&nbsp;&nbsp;<a href = "http://www.saao.ac.za/~marissa/Xrays_day3.html">today+3</a>&nbsp;&nbsp;<a href = "http://www.saao.ac.za/~marissa/Xrays_day4.html">today+4</a>&nbsp;&nbsp;<a href = "http://www.saao.ac.za/~marissa/Xrays_day5.html">today+5</a>&nbsp;&nbsp;<a href = "http://www.saao.ac.za/~marissa/Xrays_day6.html">today+6</a>&nbsp;&nbsp;<p>', file=scriptHTML)
      print('<H1>Xray satellite targets</H1>', file=scriptHTML)
      print('<H3>P.I. &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp  Target &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp   Black bars indicate possible SALT observation windows (SAST)</H3>', file=scriptHTML)
      print('<img src="Xray/'+day+'_NICERtoday.jpg"><p> <br>', file=scriptHTML)
      print('<img src="Xray/'+day+'_SWIFTtoday.jpg"><p> <br>', file=scriptHTML)
      print('<img src="Xray/'+day+'_Chan_XMM_suz_Int_today.jpg"><p> <br>', file=scriptHTML)
      print('</center>', file=scriptHTML)
      print('<H2>Useful links:</H2><p>', file=scriptHTML)
      print('<tr><a href = "http://heasarc.gsfc.nasa.gov/docs/archive.html">HEASARC archives</a><p>', file=scriptHTML)
      print('<tr><a href = "http://irsa.ipac.caltech.edu/applications/DUST">Caltec IRSA DUST extinction calculator</a><p>', file=scriptHTML)
      print('<tr><a href = "http://gcn.gsfc.nasa.gov/swift_grbs.html">Swift Gamma Ray Burster ToO info</a><p>' , file=scriptHTML)
      print('<H2>Links to the Online Schedules:</H2><p>', file=scriptHTML)
      print('<tr><a href = "https://www.swift.psu.edu/operations/obsSchedule.php">SWIFT</a><p>', file=scriptHTML)
      print('<tr><a href = "http://asc.harvard.edu/target_lists/stscheds/index.html">CHANDRA</a><p>', file=scriptHTML)
      print('<tr><a href = "https://www.cosmos.esa.int/web/xmm-newton/short-term-schedule">XMM-Newton</a><p>', file=scriptHTML)
      print('<tr><a href = "https://www.cosmos.esa.int/web/integral/schedule-information">INTEGRAL</a><p>', file=scriptHTML)
      print('<tr><a href = "https://heasarc.gsfc.nasa.gov/docs/nicer/schedule/nicer_sts_current.html">NICER</a><p>', file=scriptHTML)
      print('<tr><a href = "http://www.srl.caltech.edu/NuSTAR_Public/NuSTAROperationSite/Schedule.php">NuSTAR</a><p>', file=scriptHTML) 
      print('<center>', file=scriptHTML)
      print('<H5>Plots generated using IDL code supplied by Stephen Potter</H5>', file=scriptHTML)
      print('<H5>Website generated by Marissa Kotze</H5>', file=scriptHTML)
      print('<H5>email : marissa@saao.ac.za</H5>', file=scriptHTML)
      print('</center>', file=scriptHTML)
      print('</body>', file=scriptHTML)
      print('</html>', file=scriptHTML)     
   
      ####################################################################################################################
      # Ensure the website Xrays.html does NOT update if the INTERNET was down (all list* will not exist in that case)   #
      ####################################################################################################################

      miss = open('missfiles','r')
      test = miss.readlines()
      print(len(test))
      if len(test) == 1:
          os.remove('Xrays.html')
