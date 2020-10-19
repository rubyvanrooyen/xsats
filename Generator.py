#! /usr/bin/env python

import sys
import datetime
import calendar


#################
#  MAIN PROGRAM #
#################
oneday = datetime.timedelta(days=1)
observationdate = datetime.date.today()
observationdatem = observationdate + oneday
missiondays = observationdate - datetime.date(observationdate.year,1,1)
missiondaysm = observationdatem - datetime.date(observationdatem.year,1,1)
missionyear = observationdate.year
missionyearm = observationdatem.year
missionmonth = observationdate.month
missionmonthm = observationdatem.month
day = observationdate.day
daym = observationdatem.day
missionday = missiondays.days + 1
missiondaym = missiondaysm.days + 1

# Open the output files                     
output = open('shell_script','w')   
print('#! /bin/bash', file=output)
clean = open('clean','w')   
print('#! /bin/bash', file=clean)


###########
#  SWIFT  #
###########

if day<10:    
    if missionmonth<10:
        swiftpage1 = str(missionyear) +'-'+'0'+ str(missionmonth) +'-'+'0'+str(day)
    else:
        swiftpage1 = str(missionyear) +'-'+ str(missionmonth) +'-'+'0'+str(day)    
else:
    if missionmonth<10:
        swiftpage1 = str(missionyear) +'-'+'0'+ str(missionmonth) +'-'+str(day)
    else:    
        swiftpage1 = str(missionyear) +'-'+ str(missionmonth) +'-'+ str(day)
    
if daym<10:
    if missionmonthm<10:
        swiftpage2 = str(missionyearm) +'-'+'0'+ str(missionmonthm) +'-'+'0'+str(daym)
    else:
        swiftpage2 = str(missionyearm) +'-'+ str(missionmonthm) +'-'+'0'+str(daym)    
else:
    if missionmonthm<10:
        swiftpage2 = str(missionyearm) +'-'+'0'+ str(missionmonthm) +'-'+str(daym)
    else:    
        swiftpage2 = str(missionyearm) +'-'+ str(missionmonthm) +'-'+ str(daym)

print('wget --no-check-certificate https://www.swift.psu.edu/operations/obsSchedule.php?d='+swiftpage1 , file=output)
print('wget --no-check-certificate https://www.swift.psu.edu/operations/obsSchedule.php?d='+swiftpage2 , file=output)
print('cat '+ 'obsSchedule.php?d=* > swift', file=output)
        

############
# CHANDRA  #
############

print('wget --no-check-certificate http://asc.harvard.edu/target_lists/stscheds/index.html', file=output)
print('cat index.html > chandra', file=output)
CHANDRAday = observationdate - datetime.date(observationdate.year,1,1)
print('CHANDRA day (since 1 Jan) :  '+str(CHANDRAday.days+1))


############
#  XMM     #
############

XMMrevolution0 = datetime.date(2000,1,6) 
XMMrevolution = int((observationdate - XMMrevolution0).days/1.986441616)
print('XMM revolution :  '+str(XMMrevolution))
print('wget --no-check-certificate "http://xmm2.esac.esa.int/cgi-bin/obs_search/selectobs?revn='+str(XMMrevolution-1)+'"', file=output)
print('wget --no-check-certificate "http://xmm2.esac.esa.int/cgi-bin/obs_search/selectobs?revn='+str(XMMrevolution)+'"', file=output)
print('wget --no-check-certificate "http://xmm2.esac.esa.int/cgi-bin/obs_search/selectobs?revn='+str(XMMrevolution+1)+'"', file=output)
print('wget --no-check-certificate "http://xmm2.esac.esa.int/cgi-bin/obs_search/selectobs?revn='+str(XMMrevolution+2)+'"', file=output)
print('wget --no-check-certificate "http://xmm2.esac.esa.int/cgi-bin/obs_search/selectobs?revn='+str(XMMrevolution+3)+'"', file=output)
print('wget --no-check-certificate "http://xmm2.esac.esa.int/cgi-bin/obs_search/selectobs?revn='+str(XMMrevolution+4)+'"', file=output)
print('cat '+'"selectobs?revn="* > xmm', file=output)


#################
#  INTEGRAL     #
#################

INTEGRALrevolution0 = datetime.date(2002,11,15) 
INTEGRALrevolution = int((observationdate - INTEGRALrevolution0).days/2.877579737)
print('INTEGRAL revolution :  '+str(INTEGRALrevolution))
string1 = 'schedule.html?action=schedule&startRevno='+str(INTEGRALrevolution-1)+'&endRevno='+str(INTEGRALrevolution-1)
string2 = 'schedule.html?action=schedule&startRevno='+str(INTEGRALrevolution+0)+'&endRevno='+str(INTEGRALrevolution+0)
string3 = 'schedule.html?action=schedule&startRevno='+str(INTEGRALrevolution+1)+'&endRevno='+str(INTEGRALrevolution+1)
string4 = 'schedule.html?action=schedule&startRevno='+str(INTEGRALrevolution+2)+'&endRevno='+str(INTEGRALrevolution+2)
string5 = 'schedule.html?action=schedule&startRevno='+str(INTEGRALrevolution+3)+'&endRevno='+str(INTEGRALrevolution+3)
string6 = 'schedule.html?action=schedule&startRevno='+str(INTEGRALrevolution+4)+'&endRevno='+str(INTEGRALrevolution+4)
string7 = 'schedule.html?action=schedule&startRevno='+str(INTEGRALrevolution+5)+'&endRevno='+str(INTEGRALrevolution+5)
print('wget --no-check-certificate "http://integral.esac.esa.int/isocweb/'+string1+'"', file=output)
print('wget --no-check-certificate "http://integral.esac.esa.int/isocweb/'+string2+'"', file=output)
print('wget --no-check-certificate "http://integral.esac.esa.int/isocweb/'+string3+'"', file=output)
print('wget --no-check-certificate "http://integral.esac.esa.int/isocweb/'+string4+'"', file=output)
print('wget --no-check-certificate "http://integral.esac.esa.int/isocweb/'+string5+'"', file=output)
print('wget --no-check-certificate "http://integral.esac.esa.int/isocweb/'+string6+'"', file=output)
print('wget --no-check-certificate "http://integral.esac.esa.int/isocweb/'+string7+'"', file=output)
print('cat "schedule.html?action=schedule&startRevno="* > integral', file=output)


###############
#  NICER      #
###############

print('wget --no-check-certificate https://heasarc.gsfc.nasa.gov/docs/nicer/schedule/nicer_sts_current.html', file=output)
print('cat nicer_sts_current.html > nicer', file=output)


############
# NUSTAR   #
############

print('wget --no-check-certificate http://www.srl.caltech.edu/NuSTAR_Public/NuSTAROperationSite/Schedule.php', file=output)
print('cat Schedule.php > nustar', file=output)


#################################
#  Gamma Ray Burster Alerts     #
#################################

print('wget --no-check-certificate http://gcn.gsfc.nasa.gov/swift_grbs.html', file=output)

print('../readGRBwebdata.py', file=output)


########################################################
#  Copy Potter's IDL routines to working directory     #
########################################################

print('cp ../IDLroutines/* .', file=output)


############################
# Set up the SHELL script  #
############################
    
for i in range(7):
    
    obsdate = observationdate + datetime.timedelta(days=i)
    projectiondate = obsdate + datetime.timedelta(days=1)
    
    #################################################################
    #  PYTHON interpretive programs that read data from html files  #
    #################################################################
    print('../readSWIFTwebdata.py swift '+ str(obsdate), file=output)
    print('../readCHANDRAwebdata.py chandra ' + str(obsdate), file=output)
    print('../readXMMwebdata.py xmm ' + str(obsdate), file=output)
    print('../readINTEGRALwebdata.py integral ' + str(obsdate), file=output)
    print('../readNICERwebdata.py nicer ' + str(obsdate), file=output)
    print('../readNUSTARwebdata.py nustar ' + str(obsdate), file=output)

    ###############################################################################
    # Determine the names of the output files and put 4 of the satelites together #
    ############################################################################### 
    if int(obsdate.month)>=10 and int(obsdate.day)>=10:
        outfile = str(obsdate.year)+str(obsdate.month)+str(obsdate.day)   
    else:
        if int(obsdate.month)<10 and int(obsdate.day)>=10:
           outfile = str(obsdate.year)+'0'+str(obsdate.month)+str(obsdate.day)
        if int(obsdate.day)<10 and int(obsdate.month)>=10:
           outfile = str(obsdate.year)+str(obsdate.month)+'0'+str(obsdate.day)
        if int(obsdate.month)<10 and int(obsdate.day)<10:
           outfile = str(obsdate.year)+'0'+str(obsdate.month)+'0'+str(obsdate.day)   
           
    if i == 0:
        DateOfOrigin = outfile               
   
    rxteoutput = outfile+'_RXTEoutput'   
    swiftoutput = outfile+'_SWIFToutput'
    chandraoutput = outfile+'_CHANDRAoutput'   
    xmmoutput = outfile+'_XMMoutput'
    integraloutput = outfile+'_INTEGRALoutput'    
    niceroutput = outfile+'_NICERoutput'
    nustaroutput = outfile+'_NUSTARoutput'
    print('cat '+chandraoutput+' '+xmmoutput+' '+integraloutput+' '+nustaroutput+' > '+outfile+'_Chan_XMM_Suz_Int', file=output)  

    combifile = open('Chan_XMM_Suz_Int_fname_'+outfile,'w')
    rxtefile = open('RXTEoutput_fname_'+outfile,'w')
    swiftfile = open('SWIFToutput_fname_'+outfile,'w') 
    print(outfile+'_Chan_XMM_Suz_Int', file=combifile)
    print('\n', file=combifile)
    #(re-use the now-redundant RXTE plot for NICER)
    print(niceroutput, file=rxtefile)
    print('\n', file=rxtefile)
    print(swiftoutput, file=swiftfile)
    print('\n', file=swiftfile)
    print('cp '+ 'Chan_XMM_Suz_Int_fname_'+outfile + ' ' + 'Chan_XMM_Suz_Int_fname', file=output)
    print('cp '+ 'RXTEoutput_fname_'+outfile + ' ' + 'RXTEoutput_fname', file=output)
    print('cp '+ 'SWIFToutput_fname_'+outfile + ' ' + 'SWIFToutput_fname', file=output)

    todaydate = open('today_date_'+outfile,'w')
    print(str(obsdate.day)+'/'+str(obsdate.month)+'/'+str(obsdate.year), file=todaydate)
    print('\n', file=todaydate)
    print('cp '+ 'today_date_'+outfile + ' ' + 'today_date', file=output)
    
    print('./runtoday', file=output)
    
    print('cp Chan_XMM_suz_Int_today.jpg ' + 'today+'+str(i)+ '_Chan_XMM_suz_Int_today.jpg', file=output)
    print('cp RXTEtoday.jpg ' + 'today+'+str(i)+ '_NICERtoday.jpg' , file=output)      
    print('cp SWIFTtoday.jpg ' + 'today+'+str(i)+ '_SWIFTtoday.jpg', file=output)
    
    print('cat listswift listchandra listxmm listintegral listnicer listnustar> listall', file=output)
    print('cp listall ' + outfile+ '_listall'    , file=output)
    print('cat swift_targets chandra_targets xmm_targets integral_targets nicer_targets nustar_targets > targets', file=output)
    print('cp targets ' + outfile+ '_targets', file=output)
    print('cat swift_gti chandra_gti xmm_gti integral_gti nicer_gti nustar_gti > gti', file=output)
    print('cp gti ' + outfile+ '_gti', file=output)
    print('../retrieveSIMBADdata.py', file=output)
    print('chmod a+x scriptWGET', file=output)
    print('./scriptWGET' , file=output)
    print('../readSIMBADdata.py', file=output)
    print('cp SIMBADtypes SIMBADtypes_'+ outfile, file=output)  
    
    print('../createHTMLxrays.py ' + 'today+'+str(i), file=output)
    print('../SALTvisibility.py '+outfile+'_targets '+str(projectiondate.year)+' '+str(projectiondate.month)+' '+str(projectiondate.day), file=output)
    print('chmod a+x ./script', file=output)
    print('./script', file=output)
    print('../readSALTvisibility_MoonPhase.py '+str(projectiondate.year)+' '+str(projectiondate.month)+' '+str(projectiondate.day)+' 0.5', file=output)
    print('rm inputfile*', file=output)
    print('rm outputfile*', file=output)
    print('cp results '+ outfile + '_salt', file=output)

    print('../GTIvsSALT.py '+ outfile+ '_gti '+ outfile+ '_salt'+' 0', file=output)
    print('cp overlaps Overlaps_'+ outfile, file=output)
    
    print('../FilteredOverlapAlert.py '+ outfile+ '_gti '+ outfile+ '_salt'+' 0.25', file=output) 
    print('cp OverlapAlertInfo OverlapAlertInfo_'+ outfile, file=output)
    print('chmod a+x ./OverlapEMAIL', file=output)
    print('./OverlapEMAIL', file=output)
            
    print('cp Xrays.html ' + 'Xrays_day'+str(i)+'.html', file=output)
    
print('cp Xrays_day0.html Xrays.html' , file=output)

##################################################################
# COPY the plots to the website where it is publically available #
#                               AND                              #         
# CLEAN the WORKING DIRECTORY AND SAVE ALL RESULTS IN A FOLDER   #
##################################################################

print('mkdir ../XSATSresults/'+DateOfOrigin, file=clean)
print('rm *.ps', file=clean)
print('mv * ../XSATSresults/'+DateOfOrigin, file=clean)
#print('cp ../XSATScode/* .', file=clean)
print('cd ../XSATSresults/'+DateOfOrigin+'/', file=clean)
print('mkdir Xray', file=clean)
print('cd Xray', file=clean)
print('mv ../*jpg .', file=clean)
#print('rm saao.jpg', file=clean)
print('mv ../'+DateOfOrigin+'_* .', file=clean)
print('cd ../../../XSATS', file=clean)
#print('/usr/bin/rsync -aP '+DateOfOrigin+'_plots/ webgen.saao.ac.za:/home/marissa/public_html/Xray/'+DateOfOrigin+'_plots/', file=clean)
