  	PROGRAM LOADFILE
  	IMPLICIT NONE
  	INTEGER I

  	REAL*8 EPOCH,PERIOD,DPERIOD,EPERROR,PERERROR,CYC,THECYC,ECLIPSE
  	REAL*8 THEDAY


c 1st september 2005 is jd 2463615

        READ (*,*) PERIOD
c        PERIOD = 0.06051635D0
        CYC = 0.0D0
c        PERERROR = 1.0D-07
c       2452969.322093

        IF (PERIOD .NE. 0) THEN


        READ (*,*) EPOCH
        EPOCH=EPOCH-50000.0D0  !subtract the big number
c        EPOCH = 2969.322093D0 
        EPERROR = 9.0D-06

        READ (*,*) THEDAY
        THEDAY = THEDAY - 2450000D0 !subtract the big number

        READ (*,*) DPERIOD

        THECYC=CYC
C        DO 30 I = 10000, 100000

        DO WHILE ( (EPOCH + (THECYC * PERIOD)+(THECYC*THECYC*DPERIOD))
     &           .LT. (THEDAY-2) )
c           WRITE(*,*) THECYC
           THECYC = THECYC + 1.0D0
        ENDDO


        DO WHILE ( (EPOCH + (THECYC * PERIOD)+(THECYC*THECYC*DPERIOD))
     &            .LT. (THEDAY+2) )
            ECLIPSE = EPOCH + (THECYC * PERIOD)+(THECYC*THECYC*DPERIOD)
          WRITE (*,20) EPOCH +(THECYC * PERIOD)+(THECYC*THECYC*DPERIOD)
     &                 ,THECYC
          THECYC = THECYC + 1.0D0
        ENDDO
          


C 30     CONTINUE

c        WRITE (*,*) THECYC
  20    FORMAT(F13.8,1X,F8.0)


        ENDIF

  	STOP
   	END
