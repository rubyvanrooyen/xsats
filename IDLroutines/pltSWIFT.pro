;---opens file containing ras and decs of stars
loop=0
;openr,2,'SATs.list' ; i think this is the only change
;openr,2,'swiftoutputhalf' ; i think this is the only change
;openr,2,'swiftoutput' ; i think this is the only change
;openr,2,'testoutput' ; i think this is the only change
openr,2,'SWIFT_today' ; i think this is the only change
no_objects=strarr(1)
no_visits=strarr(1)
WHILE NOT EOF(2) DO BEGIN ; no_objects is printed at end of file .. therefore have to read it all in first
readf,2,no_objects
print,no_objects
endwhile
close,2

openr,2,'SWIFT_today' ; now have to re-read the file back in
;readf,2,no_visits ; 

sizey=double(no_objects)*1.  ;.. ps vert size of whole plot
;stargap=0.5 ;(67) gap between each star .... (total no of stars) * stargap should be just less than sizey
;stargap=0.9 ;(38) gap between each star .... (total no of stars) * stargap should be just less than sizey
stargap=25.95 * (double(no_objects-1)^(-0.932))
;stargap=0.177 ; (206) for 50 or more ish
;sizey=no_objects*stargap ;.. ps vert size of whole plot

print,sizey,stargap*no_objects
;end

starpos=0.;  a fiddle...  initial value for bottom of plot
eclptick = 1.0 ; size of vertical eclipse tick mark
timemark = 1.0 ; vert positin of eclipse time above eclipse mark
timesize = 1.0 ; size of eclipse time text

if (!d.name eq "PS") then begin
;  device,/color,/portrait,bit=8,xsize=30,ysize=sizey  ; YSIZE has to be adjusted with targtet distance below
;sizex = 30
;if sizey gt 30 then sizex = sizey
  device,/color,/portrait,bit=8,xsize=60,ysize=sizey  ; YSIZE has to be adjusted with targtet distance below
  colr=0
  loadct,13
endif else begin
  colr=0
  DEVICE, DECOMPOSE = 0
endelse
;loadct,38

;Nova LMC 2009

oldname = ''
oldRA = ''
namesize = 1.2
thk = 4

 seed=1001L
date=strarr(1)
print,'Enter a date (eg 23/3/1983):'
openr,4,'today_date'
readf,4,date
close,4


;read,date
RA=strarr(1)
;print,'Right Ascension?
;read,RA
decl=strarr(1)
;print,'Declination?
;read,decl
Epoch=strarr(1)
;print,'Epoch
;read,Epoch
Tel=strarr(1)
;print,'Telescope? 1 for 1.9m
;read,Tel
no_objects=strarr(1)
name=strarr(1)
period=strarr(1)
periodepch=strarr(1)

SAT_name=strarr(1)
pi_name=strarr(1)
SAT_start=strarr(1)
SAT_end=strarr(1)






;-------- this is a rather contrived way of getting the HJD for the
;         given date, which then gets passed to masterephem.f

RA = '20 20 20'
decl='-20 20 20'
epoch=2000
tel=1
CMD='echo -ne " ' + string(date) + '\n' + string(RA) + '\n' + string(decl) + '\n' + string(Epoch) + '\n' + string(Tel) + '\n' + '" | ./track.exe > temp.dat '
spawn, CMD

CMD='tail -n 1 temp.dat > theHJD'
spawn, CMD

junkline=dblarr(8)
openr,4,'theHJD'
readf,4,junkline
close,4
print,junkline(2) ; the HJD of this date
;------------------------------------------------------------------------




WHILE NOT EOF(2) DO BEGIN

starpos=starpos+stargap   ; DISTANCE BETWEEN EACH TARGET

readf,2,name
;readf,2,date
readf,2,RA
readf,2,decl
readf,2,Epoch
readf,2,period
readf,2,periodepch
readf,2,dperiod
readf,2,len
readf,2,sat_name
readf,2,SAT_start
readf,2,SAT_end
readf,2,pi_name
;hour=fix(strmid(SAT_start_end,3,2)) 
;readf,2,Tel
;print,name,RA,decl,Epoch
Tel=1

temp=fix(strmid(decl,0,3))

IF (temp(0) gt -91) THEN BEGIN
;IF (temp(0) lt -40) THEN BEGIN
;IF (temp(0) ge 0) THEN BEGIN
;IF (temp(0) lt -0) AND (temp(0) ge -40) THEN BEGIN


oops=0
; calculates eclipse times and opens file of eclipse times

CMD='echo -ne " ' + string(period) + '\n' + string(periodepch) + '\n'  + string(junkline(2)) + '\n' + string(dperiod) + '\n'+' " | ./masterephem.exe > eclipsetimes.dat '
spawn, CMD

print,CMD



 eclipses=dblarr(2)
 eclipsesall=dblarr(10000)
 ecls=0

openr,3,"eclipsetimes.dat",error=oops
edata=0
if oops ne -250 then begin
 edata=1
 print,name
WHILE NOT EOF(3) DO BEGIN
 readf,3,eclipses
 eclipsesall(ecls) = eclipses(0) ; these eclipse times are in HJD
 ecls=ecls+1
ENDWHILE
endif
close,3 




;-------posstr does all calculations for the track of an object

CMD='echo -ne " ' + string(date) + '\n' + string(RA) + '\n' + string(decl) + '\n' + string(Epoch) + '\n' + string(Tel) + '\n' + '" | ./track.exe > temp.dat '

spawn, CMD


bins=999
junk=strarr(4)
pol=dblarr(8,bins)
flux=dblarr(3,bins)
junk1=strarr(1)
pol1=dblarr(8)

;---- gets number of lines in temp.dat ie number of star times,coords etc---
cnt=0
openr,1,'temp.dat'
 readf,1,junk1
WHILE NOT EOF(1) DO BEGIN
 readf,1,pol1
 cnt=cnt+1
ENDWHILE
close,1 

print,'file size = ',cnt

if cnt gt 0 then begin

;---opens temp.dat again and reads in all the data--------------

pol=dblarr(8,cnt)
openr,1,'temp.dat'
 readf,1,junk1
 readf,1,pol
close,1 

polstr=strarr(cnt) ; read it into a string array aswell so we can access the sast times which are in 11:11:11 format
openr,1,'temp.dat'
 readf,1,junk1
 readf,1,polstr
close,1 

; pol(3,*) has the helio correction, so subtract this from HJD (
; pol(2,*) ) to get
; GJD = geocentric .. .this has to be done seperately for each object

;pol(2,*) = pol(2,*) - pol(3,*)
hjdcorr = pol(4,1)
print,hjdcorr
;pol(2,*) = pol(3,*)

!p.charsize=1.0
!p.multi=[0,0,1]

bignum=long(pol(2,0))
bignum1=2450000.0


;set_xy,0.15,0.75,40,90.
maxy=37
!y.tickname = " "
!y.ticks = 1


;------------------------------------------

if loop lt 1 then begin
;------ does the pole just to get some time numbers

nels=size((pol),/N_ELEMENTS)/8
maxX = pol(3,nels-1)-bignum
print,'maxX = ',maxX
;set_xy,0.1,maxX+0.01,0.,maxy
set_xy,-0.5,maxX+0.5,0.,maxy

 pol(6,*)=1000
; hjd=nint(pol(2,0:0))
print,polstr(3,0)
 plot,pol(3,*)-bignum,pol(6,*)+900,psym=-3,ystyle=1,xstyle=1,xtitle="GJD - "+strmid(polstr(3),20,8),charsize=1.1



; put yellow where moon is   ... SAST array is actually in GJD
; nels=size((pol),/N_ELEMENTS)/8
; FOR I=0,nels-2,5 do begin  ; do the moon

;   IF (pol(7,I) gt 0.0) then begin
;    SAST=dblarr(2,2)
;    SAST(0,0)=pol(3,I)-bignum
;    SAST(0,1)=pol(3,I)-bignum
;    SAST(1,0)=0.
;    SAST(1,1)=stargap
;    oplot,SAST(0,*),SAST(1,*),color=225,thick=15
;   ENDIF

; ENDFOR


moon=strarr(365)
openr,7,'moon2009.dat'
readf,7,moon
close,7
mels=size((moon),/N_ELEMENTS)/1
;FOR I=0,mels-2 do begin  ; do the moon
;  if strmid(moon(I),0,7) eq strmid(date,0,7) then begin ; only first 7 characters are compared to avoid complication on end
;          xyouts,0.0,stargap/2.,"frac moon=",/data,charsize=1.2
;          xyouts,0.1,stargap/2.,strmid(moon(I),13,7),/data,charsize=1.2
;  endif
;ENDFOR
; pirint SAST and plot some vertical dashed lines on the hours

    xyouts,0.,maxy+0.2,"SAST",/data
    xyouts,-0.45,maxy+0.2,"SWIFT",/data,charsize=1.7
    xyouts,-0.3,maxy+0.1,date,/data,charsize=1.7


 FOR I=0,nels-2 do begin   ; print the SAST times
   if pol(0,I+1) gt pol(0,I) or (pol(0,I+1) eq 0 and  pol(0,I) eq 23) then begin
    xyouts,pol(3,I+1)-bignum,maxy+0.2,STRTRIM(fix(pol(0,I+1)),2),/data
    SAST=dblarr(2,2)
    SAST(0,0)=pol(3,I+1)-bignum ; put on gjd axis
    SAST(0,1)=pol(3,I+1)-bignum
    SAST(1,0)=0.
    SAST(1,1)=900.
    oplot,SAST(0,*),SAST(1,*),linestyle=2,color=0
   ENDIF
 ENDFOR




;---to get and plot -12 degs---------------

 FOR I=1,nels-1 do begin
   IF (pol(5,I-1) eq -12.0) then begin
    deg12a=dblarr(2,2)
    deg12a(0,0)=pol(3,I)-bignum
    deg12a(0,1)=pol(3,I)-bignum
    deg12a(1,0)=0.
    deg12a(1,1)=900.
;    oplot,deg12a(0,*),deg12a(1,*),linestyle=2
;    xyouts,deg12a(0,0),-2,'sun@-12',/data
   ENDIF
;---not VERY exact but close enough
   IF (pol(5,I-1) gt -12.0) and (pol(5,I) lt -12.0) then begin
    deg12a=dblarr(2,2)
    deg12a(0,0)=((pol(3,I-1)+pol(3,I))/2.0)-bignum
    deg12a(0,1)=((pol(3,I-1)+pol(3,I))/2.0)-bignum
    deg12a(1,0)=0.
    deg12a(1,1)=900.
;    oplot,deg12a(0,*),deg12a(1,*),linestyle=2
;    xyouts,deg12a(0,0),85,'-12degs',/data
   ENDIF
   IF (pol(5,I-1) lt -12.0) and (pol(5,I) gt -12.0) then begin
    deg12a=dblarr(2,2)
    deg12a(0,0)=((pol(3,I-1)+pol(3,I))/2.0)-bignum
    deg12a(0,1)=((pol(3,I-1)+pol(3,I))/2.0)-bignum
    deg12a(1,0)=0.
    deg12a(1,1)=900.
;    oplot,deg12a(0,*),deg12a(1,*),linestyle=2
;    xyouts,deg12a(0,0),85,'-12degs',/data   
   ENDIF
 ENDFOR


;---to get and plot sun on horizon---------------

    deg12a=dblarr(2,2)
    deg12a(0,0)=pol(3,0)-bignum
    deg12a(0,1)=pol(3,0)-bignum
    deg12a(1,0)=0.
    deg12a(1,1)=900.
    oplot,deg12a(0,*),deg12a(1,*),thick=4
    deg12a(0,0)=pol(3,nels-1)-bignum
    deg12a(0,1)=pol(3,nels-1)-bignum
    oplot,deg12a(0,*),deg12a(1,*),thick=4












;---------to plot all the curves----

 endif else begin


;if strmid(name,0,1) eq '*' then begin
;    colr = 150
;endif else begin
    colr = 0
;endelse
satcol=0
if SAT_name eq "SWIFT" then satcol= 100
if SAT_name eq "RXTE" then satcol= 250
if SAT_name eq "CHANDRA" then satcol= 50

;if ( (name ne oldname) or (RA ne oldRA) ) then begin
if ( (name ne oldname)  ) then begin
;-------plot sataellite vis window
    SAST=dblarr(2,2)
    SAST(0,0)=double(SAT_start)-bignum
    SAST(0,1)=double(SAT_end)-bignum
    SAST(1,0)=starpos
    SAST(1,1)=starpos
    oplot,SAST(0,*),SAST(1,*),color=satcol,thick=14
print,'xxxxxxxxxxx',double(SAT_start)-bignum,double(SAT_end)-bignum
;--------------------------------------
;endif else if ( (name eq oldname) and (RA eq oldRA) ) then begin
endif else if ( (name eq oldname) ) then begin
    SAST=dblarr(2,2)
    SAST(0,0)=double(SAT_start)-bignum
    SAST(0,1)=double(SAT_end)-bignum
    SAST(1,0)=starpos-stargap
    SAST(1,1)=starpos-stargap
    oplot,SAST(0,*),SAST(1,*),color=satcol,thick=14
print,'xxxxxxxxxxx',double(SAT_start)-bignum,double(SAT_end)-bignum

endif

 thk=4

;if name ne oldname then begin
;if ( (name eq oldname) and (RA eq oldRA) ) then starpos = starpos  - stargap
if ( (name eq oldname) ) then starpos = starpos  - stargap


pol(7,*)=starpos

 endarr=size((pol),/N_ELEMENTS)/8
    xyouts,-0.3,starpos,name,/data,color=colr,charsize=namesize
    xyouts,-0.5,starpos,pi_name,/data,color=colr,charsize=namesize

;  print times of end and begin tracks
print,"  geocentric JD     SAST     SIDT  <br>"
in = 0
for plotloop = 0,endarr-2 do begin

 if (pol(6,plotloop) ge 47 and  pol(6,plotloop) le 59) then begin
         if in eq 0 then begin
             geojd = strtrim  ( (pol(3,plotloop)-2400000),2)
             print, "BEGIN " ,geojd,"    " ,strmid(polstr(plotloop),0,6),"  ", strmid(polstr(plotloop),9,10)," <br>",pol(3,plotloop:plotloop+1)-bignum
             xyouts,pol(2,plotloop)-bignum-0.03,starpos,strmid(polstr(plotloop),0,6),charsize=0.9,color=12
         endif

  oplot,pol(3,plotloop:plotloop+1)-bignum,pol(7,plotloop:plotloop+1),psym=-3,color=colr,thick=thk   ; plot the actual track

  in = 1
 endif


;   if  (strmid(name,0,1) eq '*') then begin
;     oplot,pol(3,plotloop:plotloop+1)-bignum,pol(7,plotloop:plotloop+1),psym=-3,color=colr,thick=thk
;   endif
 

         if in eq 1 and (pol(6,plotloop) lt 47 or  pol(6,plotloop) gt 59) then begin 
             geojd = strtrim  ( (pol(3,plotloop)-2400000),2)
             print, "END   " ,geojd,"    " ,strmid(polstr(plotloop),0,6),"  ", strmid(polstr(plotloop),9,10)," <br>"
             in = 0
             xyouts,pol(2,plotloop)-bignum,starpos,strmid(polstr(plotloop),0,6),charsize=0.9,color=12
         endif

     endfor


; endif ;name

;rxj649-07

;if name eq "*RX J0649.8-0737*" then begin


; put |||||| at already observed data








if len ne 0 then colr = 128
if len eq 0 then colr = 0


;if ( (name eq oldname) and (RA eq oldRA)) then begin
if ( (name eq oldname)) then begin
;starpos = starpos  - stargap

vert=dblarr(2,2)

;len=0.003
;put a | at the exact (1 min)  time position of an eclipse 
eclipsesall(*) = eclipsesall(*) - hjdcorr ;-- convert hjd eclipse times to geocentric
for pt = 0,cnt-6 do begin
 if edata eq 1 then begin
  for round = 0,ecls do begin
   if eclipsesall(round) ge ((pol(3,pt)-bignum1)-len) and eclipsesall(round) le ((pol(3,pt+1)-bignum1)+len) then begin
       if pol(6,pt) ge 47 and  pol(6,pt) le 59  then begin
       ycoord = starpos
       vert(0,0) = pol(3,pt)-bignum
       vert(0,1) = pol(3,pt)-bignum
       vert(1,0) = starpos
       vert(1,1) = starpos+eclptick
       oplot,vert(0,*), vert(1,*),psym=-3,color=colr,thick=4
;       xyouts,pol(3,pt)-bignum,ycoord+1.5,strmid(polstr(pt),0,6),charsize=1.4
;       geojd = strtrim  ( (pol(3,pt)-2400000),2)
;       print, "ECLIPSE " ,geojd,"  " ,strmid(polstr(pt),0,6),"  ", strmid(polstr(pt),9,10)," <br>"
       endif
   endif
  endfor
 endif
endfor

endif ; name


;put eclipse time at tick mark
vert=dblarr(2,2)
;len=0.00
if name ne oldname then begin
eclipsesall(*) = eclipsesall(*) - hjdcorr ;-- convert hjd eclipse times to geocentric
for pt = 0,cnt-6 do begin
 if edata eq 1 then begin
  for round = 0,ecls do begin
;   if eclipsesall(round) ge (pol(3,pt)-bignum1) and eclipsesall(round) le (pol(3,pt+1)-bignum1) then begin
   if eclipsesall(round) ge ((pol(3,pt)-bignum1)-len) and eclipsesall(round) le ((pol(3,pt+1)-bignum1)+len) then begin
       if pol(6,pt) ge 47 and  pol(6,pt) le 59  then begin
       ycoord = starpos
       vert(0,0) = pol(3,pt)-bignum
       vert(0,1) = pol(3,pt)-bignum
       vert(1,0) = starpos
       vert(1,1) = starpos+timemark
       oplot,vert(0,*), vert(1,*),psym=-3,color=colr,thick=4
        if len eq 0 then begin
         xyouts,pol(3,pt)-bignum,ycoord+0.8,strmid(polstr(pt),0,6),charsize=timesize
         geojd = strtrim  ( (pol(3,pt)-2400000),2)
         print, "ECLIPSE " ,geojd,"  " ,strmid(polstr(pt),0,6),"  ", strmid(polstr(pt),9,10)," <br>"
        endif
       endif
   endif
  endfor
 endif
endfor
endif
oldname = name
oldRA = RA
DONE=0


DONE=0



endelse


;----------------------------------------
loop=loop+1
;wait,1
endif
ENDIF
print,"  "
ENDWHILE
close,2 
end


