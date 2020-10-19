C===========================================================================
C
C	program: ephem2.for
C
C	purpose: calculates day/hr ephemeris
C
C===========================================================================
C
	implicit real*8 (a-h,o-z)
	character*80 str,dte,tel(4)*8,atel(4)*20
	integer*4 ix(10),isite(8),idate(6),ipos(7),isdt(3),
     +idt(3),ira(3),idc(3)
	real*8 dec(100),han(100),hap(100)
	data isite/-1,32,22,46,-1,20,48,36/
	data tel /'hor-1.9','hor-1.0','hor-0.7','hor-0.5'/
	data atel/'1.9-m Giraffe','1.0-m DandiCam','0.75-m IRP',
     +'0.5-m MP' /
C
c	open(unit=2,file='/tmp/strpos.html',status='unknown')
c	write(2,2010)
c2010	format('<html>'/'<head>'/'<title>Star position</title>'/
c     +'</head>'/'<body><pre>'/)

1	write(*,1010)
1010	FORMAT('Enter date (eg 23/3/1983): ',$)
	read(*,1020) str
C
	dte = str
C
1020	format(a)
	do i=1,3
	 ix(i)=idt(i)
	end do
C
	call redn(str,ix,isg,l)
C
	if(l.gt.1) then
	 do i=1,3
	  idt(i)=ix(i)
	 end do
	 idate(1)=ix(3)
	 idate(2)=ix(2)
	 idate(3)=ix(1)
	 epin=idate(1)+float(idate(2))/12.0+float(idate(3))/365.25
	end if
C
2	write(*,1040)
1040	FORMAT('Right Ascension? ',$)
	read(*,1020) str
	IF(STR(1:1).EQ.'A') GOTO 1
	call redn(str,ix,isg,l)
	if(l.gt.1) then
	 do i=1,3
	  ira(i)=ix(i)
	 end do
	 ipos(1)=ix(1)
	 ipos(2)=ix(2)
	 ipos(3)=ix(3)
	end if
C
	write(*,1050)
1050	FORMAT('Declination?    ',$)
	read(*,1020) str
	IF(STR(1:1).EQ.'A') GOTO 2
	call redn(str,ix,isg,l)
	if(l.gt.1) then
	 do i=1,3
	  idc(i)=ix(i)
	 end do
	 if(isg.lt.0) idc(1)=-idc(1)
	 ipos(4)=isg
	 ipos(5)=ix(1)
	 ipos(6)=ix(2)
	 ipos(7)=ix(3)
	 end if
C
	k = lnblnk(dte)
	if(ipos(4).ge.0) then
	 write(2,2030) dte(1:k),(ipos(i),i=1,3),(ipos(i),i=5,7)
2030	 format('<center><h3>   Date: ',a,'     RA: ',i2.2,':',i2.2,
     +':',i2.2,'     Dec:  +',i2.2,':',i2.2,':',i2.2,'</h3>')
	else
	 write(2,2031) dte(1:k),(ipos(i),i=1,3),(ipos(i),i=5,7)
2031	 format('<center><h3>   Date: ',a,'     RA: ',i2.2,':',i2.2,
     +':',i2.2,'     Dec:  -',i2.2,':',i2.2,':',i2.2,'</h3>')
	endif
	write(*,1060) epin
1060	FORMAT('Epoch (CR for',F8.2,')? ',$)
	read(*,1020) str
	call redn(str,ix,isg,l)
	if(l.ge.1) epin=ix(1)+float(ix(2))/60.0
	epot=epin
C
	idate(5) = 0
	idate(6) = 0
	write(*,'(''Telescope? '',$)')
	read(*,*) itel
	call horizon(tel(itel),dec,han,hap,ntel)
C
	write(2,2032) atel(itel)
2032	format('<h3>',a,'</h3></center>'//
     +'SAST is the South African Standard Time, SIDT the local
     + sidereal time, HJD the'/'heliocentric Julian date, AirMass is 
     + the air mass (sec(z)), MoonAlt, SunAlt'/'the altitudes of the 
     + moon and sun (degrees), Alt is the altitude of the star'/
     +'above the horizon and Hor is the altitude above the dome
     + horizon (degrees).'/)

C
	phi = -0.25d0
	sdt = 0.0
	kd = idate(3)
	idate(3) = kd + 1
	idate(4) = 0
	call djulian(idate, T)
	call moon(T, alpha, delta, phs, phi, sdt, altmoon)
	idate(3) = kd
C
	write(2,9001) phs
9001	format('<h3>Moon phase = ',f8.3,'</h3>'//
     +'   SAST      SIDT          HJD     AirMass MoonAlt
     +  SunAlt     Alt     Hor')
C
	kd = idate(3)
	i = 14	
	do ii = 0,23
	 i = i + 1
	 if(i.gt.23) then
	  i = 0
	  idate(3) = kd + 1
	 endif
	 idate(4) = i
	 do jj = 0,59,1
	  idate(5) = jj
	  call ephem(isite,idate,ipos,epin,epot,isdt,gjd,dt,dv,am,scz,
     +sunalt,alt,ha,phi,dc,sdt)
	  hjd=gjd+dt

C
	  call djulian(idate, T)
C
	  call moon(T, alpha, delta, phs, phi, sdt, altmoon)
C
	  dal = alt
	  if(ntel.gt.0) a1 = althor(dc,ha,dec,han,hap,ntel,phi)
	  dal = alt - a1
C
	  is = i + 2
	  if(is.gt.23) is = is - 24
	  if(am.gt.99.0) am = 99
	  if(sunalt.lt.0.0.and.am.gt.0.0)
     + write(*,2000) is,jj,isdt,hjd,gjd,dt,sunalt,alt,altmoon
2000	FORMAT(i3.2,':',i2.2,':00',2x,i2.2,':',i2.2,':',i2.2,
     +f15.5,f15.5,1x,f6.4,3f8.1)
c     +f15.5,f8.3,4f8.1)
	 enddo
	enddo

C
	write(2,2040)
2040	format('</pre>'/'</body>'/'</html>')
	close(2)
	end
C
C===========================================================================
C
C	program: ephemeris
C
C	purpose: subroutine calculates heliocentric time and velocity
C		corrections and ephemeris for sun and moon
C
C	calling sequence:
C
C	call ephem(isite,idate,ipos,epin,epot,isdt,gjd,dt,dv,am,scz,alt)
C
C		isite(8)	-	a matrix containing the following
C		isite(1) - sign of lattitude of site
C		isite(2) - degree of lattitude of site
C		isite(3) - minute of lattitude of site
C		isite(4) - second of lattitude of site
C		isite(5) - sign of longitude of site
C		isite(6) - degree of longitude of site
C		isite(7) - minute of longitude of site
C		isite(8) - second of longitude of site
C
C		idate(6)	-	a matrix containing the following:
C
C		idate(1) - year of observation (e.g. 1980)
C		idate(2) - month of observation
C		idate(3) - day of observation
C		time in u.t:
C		idate(4) - hour of observation
C		idate(5) - minute of observation
C		idate(6) - second of observation
C
C		ipos(7)		-	a matrix containing the following
C
C		ipos(1) - hour of ra
C		ipos(2) - minute of ra
C		ipos(3) - second of ra
C		ipos(4) - sign of dec
C		ipos(5) - degree of dec
C		ipos(6) - minute of dec
C		ipos(7) - second of dec
C
C		epin	-	the input epoch (eg. 1950.0)
C		epot	-	the output epoch (eg. 1982.53)
C
C		isdt(1)	- hour of local sidt
C		isdt(2) - minute of local sidt
C		isdt(3) - second of local sidt
C
C		gjd	-	the geocentric julian date
C		dt	-	the heliocentric correction for gjd
C		dv	- 	the heliocentric velocity correction
C		am	-	the air mass
C
C==========================================================================
C
	subroutine ephem(isite,idate,ipos,epin,epot,isdt,gjd,dt,
     +dv,am,scz,sunalt,alt,ha,phi,dec,sdt)
	implicit real*8 (a-h,o-z)
	integer*4 isite(8),idate(6),ipos(7),isdt(3)
	parameter  (frad=4.8481368d-06, r2deg = 57.29578)
C
C	calcilate julian day number jd:
C
	iyr=idate(1)
	mon=idate(2)+1
	if(idate(2).le.2) then
	iyr=idate(1)-1
	mon=idate(2)+13
	end if
C
	jd=(36525*iyr)/100+(306001*mon)/10000+idate(3)+1720981
C
C	calculates fractional part of jd to form gjd
C
	jut=3600*idate(4)+60*idate(5)+idate(6)
	fjd=jut/86400.0d00+0.50d00
	gjd=jd+fjd
C
C	calculate no of julian centuries since 1900.0
	t=((jd-2415020)+0.50d0)/36525.0d0
C
C	calculate mean siderial time at 0hr ut on date of observation
	sdt0=23925.836d0+t*(8640184.542d0+0.0929*t)
	sdt0=dmod(sdt0,86400d0)
	if(sdt0.lt.0.0d0) sdt0=86400.0+sdt0
C	reduction for longitude
	long=3600*isite(6)+60*isite(7)+isite(8)
	if(isite(5).lt.0) long=-long
	sdt=sdt0+1.8252728d-04*long
C	conversion to local mean solar time
	lmsot=jut-long/15
	sdt=sdt+1.0027379093d0*lmsot
	sdt=dmod(sdt,86400d0)
	if(sdt.lt.0.0d0) sdt=sdt+86400.0d0
	isdt(1)=sdt/3600.0d0
	isdt(2)=(sdt-3600.0d0*isdt(1))/60.0d0
	isdt(3)=sdt-3600.0d0*isdt(1)-60.0*isdt(2)
C
C	calculates solar ephemeris:
C
C	geometric mean longitude:
	gmls=1006908.04d0+t*(129602768.13+1.089*t)
	gmls=dmod(gmls,1296000.0d0)
	if(gmls.lt.0.0d0) gmls=gmls+1296000.0d0
C	mean longitude of perigee:
	pmls=1012395.0d0+t*(6189.03+1.63*t)
	pmls=dmod(pmls,1296000.0d0)
	if(pmls.lt.0.0d0) pmls=pmls+1296000.0d0
C	eccentricity:
	ecs=0.01675104-t*(4.18d-05+1.26d-07*t)
C	obliquity of ecliptic
	eps=84428.26-t*(46.845+t*(0.0059-0.00181*t))
	ceps=dcos(frad*eps)
	seps=dsin(frad*eps)
C
C	solves keplers equation for earth orbit:
C
	anm=frad*(gmls-pmls)
	x=anm
100	e=anm+ecs*dsin(x)
	if(dabs(e-x).lt.1.0d-7) goto 110
	x=e
	goto 100
C
110	se=dsqrt(1.00d0+ecs)*dsin(0.50d0*e)
	ce=dsqrt(1.00d0-ecs)*dcos(0.50d0*e)
	anm=2.00d0*datan2(se,ce)
	tlon=anm/frad+pmls
	tlon=dmod(tlon,1296000.0d0)
	if(tlon.lt.0.0d0) tlon=tlon+1296000.0d0
	tls=frad*tlon
C
C	Tlon is the true longitude of sun in arc seconds.
C	calculate radius vector:
	ras=1.00d0-ecs*dcos(e)
C
C	SUNDEC is sun's Dec (radians), SUNRA = sun's RA (radians)
C
	ctl = cos(tls)
	stl = sin(tls)
	sundec = dasin(seps*stl)
	sdec = dsin(sundec)
	cdec = dcos(sundec)
	csa = ctl/dcos(sundec)
	ssa = ceps*stl*csa/ctl
	sunra = datan2(ssa,csa)
	hasun = 7.272205d-5*sdt - sunra
C
	lts=3600*isite(2)+60*isite(3)+isite(4)
	if(isite(1).lt.0) lts=-lts
	phi=frad*lts
C
	csz = dsin(phi)*sdec+dcos(phi)*cdec*dcos(hasun)
C
	sunalt = r2deg*asin(csz)
C
C	precession
C
C	calculate precesional constants:
	t0=0.01d0*(epin-1900.0d0)
	t1=0.01d0*(epot-epin)
	zt=t1*((2304.25d0+1.396d0*t0)+t1*(0.302d0+0.018d0*t1))
	z=zt+0.791*t1*t1
	th=t1*((2004.682d0-0.853d0*t0)-t1*(0.426d0+0.042d0*t1))
C	transform ra, dec to radians
	ira=3600*ipos(1)+60*ipos(2)+ipos(3)
	idc=3600*ipos(5)+60*ipos(6)+ipos(7)
	if(ipos(4).lt.0) idc=-idc
	ra=15.0d0*frad*ira
	dec=frad*idc
	cra=dcos(ra)
	sra=dsin(ra)
	cdc=dcos(dec)
	sdc=dsin(dec)
C
	zt=frad*zt
	z=frad*z
	th=frad*th
	tht=dtan(0.50d0*th)
	q=dsin(th)*(dtan(dec)+tht*dcos(ra+zt))
	ta=q*dsin(ra+zt)/(1.0d0-q*dcos(ra+zt))
	dta=datan(ta)
	dra=zt+z+dta
C	in secs of time:
	ira=ira+dra/(15.0d0*frad)
C	now for dec:
	td=tht*dcos(ra+zt+0.50d0*dta)/dcos(0.50d0*dta)
	ddc=2.0d0*datan(td)
	idc=idc+ddc/frad
C	now convert:
	if(ira.gt.86400) ira=ira-86400
	if(ira.lt.0) ira=ira+86400
	ipos(4)=1
	if(idc.lt.0) ipos(4)=-1
	idc=iabs(idc)
	if(idc.gt.324000) idc=648000-idc
	ipos(1)=ira/3600
	ipos(2)=(ira-3600*ipos(1))/60
	ipos(3)=ira-3600*ipos(1)-60*ipos(2)
	ipos(5)=idc/3600
	ipos(6)=(idc-3600*ipos(5))/60
	ipos(7)=idc-3600*ipos(5)-60*ipos(6)
C
C
C	convert ra, dec to celestial lat, long:
C
	ra=15.0d0*frad*ira
	dec=frad*idc
	if(ipos(4).lt.0) dec=-dec
	sra=dsin(ra)
	cra=dcos(ra)
	sdc=dsin(dec)
	cdc=dcos(dec)
	snb=sdc*ceps-cdc*seps*sra
	csb=sqrt(1.0d0-snb*snb)
	snl=(sdc*seps+cdc*ceps*sra)/csb
	csl=cdc*cra/csb
	slg=datan2(snl,csl)
	slt=datan(snb/csb)
C
C	heliocentric time correction
	dt=-0.0057755d0*ras*csb*dcos(tls-slg)
C
C	heliocentric velocity calculation
C
C	Earth's motion round the sun:
	tani=ecs*dsin(anm)/(1.0d0+ecs*dcos(anm))
	ync=datan(tani)
	va=29.7893d0*(1.0d0+ecs*dcos(anm))/dcos(ync)
	dv1=-va*dsin(slg-tls+ync)*csb
C
C	Earth's rotation:
	h = sdt-ira
	if(h.gt.43200.0) h = h - 86400.0
	if(h.lt.-43200.0) h = h + 86400.0
C
	ha = 15.0d0*frad*h
	shra = dsin(ha)
	chra = dcos(ha)
	dv2=-0.470d0*shra*cdc*dcos(phi)
C
C	Mean longitude of moon:
	bml=973563.69d0+1732564379.0d0*t
	bml=dmod(bml,1296000.0d0)
C	Moon's orbital motion:
	dv3=-0.010d0*dsin(slg-frad*bml)*csb
C
	dv=dv1+dv2+dv3
C
C	air mass
C
	csz=dsin(phi)*sdc+dcos(phi)*cdc*chra
	scz=1.0d0/csz
	am=scz*(1.0-0.0012*(scz*scz-1.0))
	alt = r2deg*asin(csz)
	return
	end
C
C===========================================================================
C
C	program: redn.for
C
C	purpose: reads a character string and decodes numeric field
C
C	input: string str
C
C	output: n is no of numbers
C               ix(n) contains dp numbers
C	isg=-1 if negative, =1 if positive =0 if meaningless
C
	subroutine redn(str,ix,isg,l)
	implicit real*8 (a-h,o-z)
	dimension nv(80),ix(10)
	character*80 str
C
	mns=0
	npl=0
	do i=1,80
	IF(STR(I:I).EQ.'-') THEN
	mns=mns+1
	STR(I:I)=' '
	end if
	IF(STR(I:I).EQ.'+') THEN
	npl=npl+1
	STR(I:I)=' '
	end if
	nv(i)=1
	IF(STR(I:I).LT.'0'.OR.STR(I:I).GT.'9') NV(I)=0
	end do
C
	j=mns+npl
	if(j.gt.1) goto 99
	isg=1
	if(mns.ne.0) isg=-1
	do i=1,10
	ix(i)=0
	end do
	l=0
	is=0
C
	kd=0
	ks=1
	do 2 i=1,80
	if(nv(i).eq.1) then
	ks=0
	j=iand(ichar(str(i:i)),127)-48
	kd=10*kd
	is=10*is+j
	goto 2
	end if
	if(ks.eq.1) goto 2
	l=l+1
	if(kd.ne.0) then
	is=60*is/kd
	kd=0
	end if
	ix(l)=is
	ks=1
	is=0
	IF(STR(I:I).EQ.'.') KD=1
2	continue
C
	return
99	isg=0
	return
	end
C
C============================================================================
C
C			HORIZON
C
C============================================================================
C
	subroutine horizon(tel,dec,han,hap,n)
	implicit real*8 (a-h,o-z)
	character*(*) tel
	dimension dec(1),han(1),hap(1)
	parameter  (r2deg = 57.29578d0, h2r = 0.26179939d0)
C
c	open(unit=3,file='/usr/local/data/'//tel,status='old')
        open(unit=3,file='hor-1.9',status='old')
C
	n = 0
1	read(3,*,end=2) d,hn,hp
	n = n + 1
	dec(n) = d/r2deg
	han(n) = h2r*hn
	hap(n) = h2r*hp
	goto 1
C
2	close(3)
	return
	end
C
C============================================================================
C
C			ALTHOR
C
C============================================================================
C
	function althor(dc,ha,dec,han,hap,ntel,phi)
	implicit real*8 (a-h,o-z)
	real*8 dec(100),han(100),hap(100),y2(100)
	parameter  (r2deg=57.29578d0, h2r=0.26179939d0,pi=3.1416d0)
C
	yp1 = 2.0e+31
	yp2 = 2.0e+31
	if(ha.lt.0.0) then
	 call spline(dec,han,ntel,yp1,ypn,y2)
	 call splint(dec,han,y2,ntel,dc,h)
	else
	 call spline(dec,hap,ntel,yp1,ypn,y2)
	 call splint(dec,hap,y2,ntel,dc,h)
	endif
C
	if(dabs(h).gt.pi) then
	 althor = 0.0
	else
	 csz=dsin(phi)*sin(dc)+dcos(phi)*cos(dc)*dcos(h)
	 althor = r2deg*asin(csz)
	endif
C
	return
	end
C	
C============================================================================
C
C			SPLINE
C
C============================================================================
C
      SUBROUTINE spline(x,y,n,yp1,ypn,y2)
      implicit real*8 (a-h,o-z)
      INTEGER n,NMAX
      REAL*8 yp1,ypn,x(n),y(n),y2(n)
      PARAMETER (NMAX=500)
      INTEGER i,k
      REAL*8 p,qn,sig,un,u(NMAX)
      if (yp1.gt..99e30) then
        y2(1)=0.
        u(1)=0.
      else
        y2(1)=-0.5
        u(1)=(3./(x(2)-x(1)))*((y(2)-y(1))/(x(2)-x(1))-yp1)
      endif
      do 11 i=2,n-1
        sig=(x(i)-x(i-1))/(x(i+1)-x(i-1))
        p=sig*y2(i-1)+2.
        y2(i)=(sig-1.)/p
        u(i)=(6.*((y(i+1)-y(i))/(x(i+
     *1)-x(i))-(y(i)-y(i-1))/(x(i)-x(i-1)))/(x(i+1)-x(i-1))-sig*
     *u(i-1))/p
11    continue
      if (ypn.gt..99e30) then
        qn=0.
        un=0.
      else
        qn=0.5
        un=(3./(x(n)-x(n-1)))*(ypn-(y(n)-y(n-1))/(x(n)-x(n-1)))
      endif
      y2(n)=(un-qn*u(n-1))/(qn*y2(n-1)+1.)
      do 12 k=n-1,1,-1
        y2(k)=y2(k)*y2(k+1)+u(k)
12    continue
      return
      END
C  (C) Copr. 1986-92 Numerical Recipes Software m!1.
C
C============================================================================
C
C			SPLINT
C
C============================================================================
C
      SUBROUTINE splint(xa,ya,y2a,n,x,y)
      implicit real*8 (a-h,o-z)
      INTEGER n
      REAL*8 x,y,xa(n),y2a(n),ya(n)
      INTEGER k,khi,klo
      REAL*8 a,b,h
      klo=1
      khi=n
1     if (khi-klo.gt.1) then
        k=(khi+klo)/2
        if(xa(k).gt.x)then
          khi=k
        else
          klo=k
        endif
      goto 1
      endif
      h=xa(khi)-xa(klo)
      if (h.eq.0.) write(*,*) 'bad xa input in splint'
      a=(xa(khi)-x)/h
      b=(x-xa(klo))/h
      y=a*ya(klo)+b*ya(khi)+((a**3-a)*y2a(klo)+(b**3-b)*y2a(khi))*(h**
     *2)/6.
      return
      END
C  (C) Copr. 1986-92 Numerical Recipes Software m!1.
C
C============================================================================
C
C			RTODEG
C
C	Converts radians to DD MM SS
C
C============================================================================
C
	subroutine rtodeg(ang, str)
	implicit real*8 (a-h,o-z)
	character str*80
	parameter (frad = 0.017453293d0)
C
	deg = ang/frad
C
	d = dabs(deg)
	kd = d
	amn = 60.0d0*(d - kd)
	m = amn
	is = 60.0d0*(amn - m) + 0.5d0
C
	if(deg.lt.0.0d0) kd = -kd
C
	write(str,1010)	kd,m,is
1010	format(i3.2,':',i2.2,':',i2.2)
	return
	end
C
C============================================================================
C
C			MOON
C
C	Given the centuries since JD2000, returns the RA (alpha) and 
C	Dec (delta) of the moon (radians)
C
C============================================================================
C
	subroutine moon(T, alpha, delta, phs, phi, sdt, altmoon)
	implicit real*8 (a-h,o-z)
	parameter (frad = 0.017453293d0, twopi = 6.2831853d0)
	parameter  (r2deg = 57.29578)
C
	a0 = 218.32d0 + 481267.883d0*T
	a1 = dsin(frad*(134.9d0 + 477198.85d0*T))
	a2 = dsin(frad*(259.2d0 - 413335.38d0*T))
	a3 = dsin(frad*(235.7d0 + 890534.23d0*T))
	a4 = dsin(frad*(269.9d0 + 954397.70d0*T))
	a5 = dsin(frad*(357.5d0 +  35999.05d0*T))
	a6 = dsin(frad*(186.6d0 + 966404.05d0*T))
C
	alam = frad*(a0+6.29d0*a1-1.27d0*a2+0.66d0*a3+0.21d0*a4
     + -0.19*a5-0.11*a6)		
C
	do while (alam.gt.twopi)
	 alam = alam - twopi
	enddo
C
	do while (alam.lt.0.0d0)
	 alam = alam + twopi
	enddo
C
	b1 = dsin(frad*( 93.3d0 + 483202.03d0*T))
	b2 = dsin(frad*(228.2d0 + 960400.87d0*T))
	b3 = dsin(frad*(318.3d0 +   6003.18d0*T))
	b4 = dsin(frad*(217.6d0 - 407332.20d0*T))
C
	beta = frad*(5.13d0*b1+0.28d0*b2-0.28d0*b3-0.17d0*b4)
C
	sl = dsin(alam)
	cl = dcos(alam)
	sb = dsin(beta)
	cb = dcos(beta)
C
	al = cb*cl
	am = 0.9175d0*cb*sl - 0.3978d0*sb
	an = 0.3978d0*cb*sl + 0.9175d0*sb
C
	alpha = datan2(am,al)
	if(alpha.lt.0.0d0) alpha = twopi + alpha
	delta = dasin(an)
C
C	Sun lingitude
	d = 36525.0d0*T
	sunl = frad*(280.460d0 + 0.9856474*d)
C
	phs = (alam - sunl)/twopi
	if (phs.lt.-0.5d0) phs = phs + 1.0d0
	if (phs.gt. 0.5d0) phs = phs - 1.0d0
C
	h = 7.272205d-5*sdt - alpha
	csz = dsin(phi)*sin(delta)+dcos(phi)*cos(delta)*dcos(h)
	altmoon = r2deg*asin(csz)
C
	return
	end
C
C============================================================================
C
C			DJULIAN
C
C	Returns Julian day number from date
C
C		idate(1) - year of observation (e.g. 1980)
C		idate(2) - month of observation
C		idate(3) - day of observation
C		time in u.t:
C		idate(4) - hour of observation
C		idate(5) - minute of observation
C		idate(6) - second of observation
C
C============================================================================
C
	subroutine djulian(idate, T)
	implicit real*8 (a-h, o-z)
	integer*4 idate(6)
C
	iyr=idate(1)
	mon=idate(2)+1
C
	if(idate(2).le.2) then
	 iyr=idate(1)-1
	 mon=idate(2)+13
	end if
C
	jd=(36525*iyr)/100+(306001*mon)/10000+idate(3)+1720981
C
C	Calculates fractional part of JD to form GJD
C
	jut=3600*idate(4)+60*idate(5)+idate(6)
	fjd=jut/86400.0d00+0.50d00
	gjd=jd+fjd
C
C	Calculate no of Julian centuries since 2000.0
	T = ((gjd-2451545)+0.50d0)/36525.0d0
C
	return
	end
C
