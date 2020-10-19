/***********************************************************************

to compile type:
cc -g -fno-inline -Wall -o  sort_objects.exe sort_objects.c -lm
***********************************************************************/
#define     LINT_ARGS

#include    <ctype.h>
#include    <math.h>
#include    <stdio.h>
#include    <stdlib.h>
#include    <string.h>

//#include    "array.h"
//#include    "astro.h"
//#include    "numerx.h"

// pole
// 0 00 00
// -89 59 59
// 2000
// 1
// 1
// 0
// 0
// none
// 0
// 0
// none

int     main(argc, argv)

  int     argc;
  char    *argv[];
{
  char                recin[100] ,bigarr[5000][100],today_file[100],today_file1[2][100];
  char                current_name[100],current_sat[100];
  int                 no_visits=0,i,line_no=0,j,no_targs=0;
  int                 obj_line_done[5000] , start=0, loop=0, to_file=0;
  FILE                *fptr,*fptr1;


  //  if((argc < 2) || (argc > 6)) {
  //    fprintf(stderr, "Usage: sort_object filename\n");
  //    exit(-1);
  //  }


  // open file
  //  for(i = 1; i < argc; i ++) {
  //      sscanf(argv[i], "%s", fnam);
  //      if((fptr = fopen(fnam, "r")) == NULL) {
  //        fprintf(stderr, "Error: Cannot open input file\n");
  //        exit(-1);
  //      }
  //  }



  // open file conataining todays filename
  if((fptr1 = fopen("Chan_XMM_Suz_Int_fname", "r")) == NULL) {
    fprintf(stderr, "Error: Cannot open input file\n");
    exit(-1);
  }
    line_no=0;

    while( !feof(fptr1) ) { 
      if(fgets(today_file, sizeof(today_file), fptr1) == NULL) continue;
      strncpy(today_file1[line_no],today_file,strlen(today_file)-1);
      line_no=line_no+1;
      //      printf("here %li\n",strlen(today_file1[0]));
    }
      fclose(fptr1);

  //    printf("here1 %s\n",today_file);
    //now actually open todays filename
      //            strcpy(today_file, "Chan_XMM_Suz_Int_fname");
      //            strcpy(today_file,&today_file[0] );
      if((fptr = fopen(today_file1[0], "r")) == NULL) {
        fprintf(stderr, "Error: Cannot open input file %s\n",today_file1[0]);
        exit(-1);
      }

      //    printf("here2\n");  

    //---------------------------


  // read data from todays file
    line_no=0;
  while( !feof(fptr) ) { // read every line into bigarr
    if(fgets(recin, sizeof(recin), fptr) == NULL) continue;
    strcpy(bigarr[line_no], recin) ;
    line_no = line_no + 1;
    //    printf("here4\n");    
  }


  //    printf("here3\n");    
  no_visits = (line_no - 1) /12; // this is NOT number of targets
  fclose(fptr);

  //----------------------------------------------------------------------------------
  // this next loop is ran twice ... first just counts nmber of objects then 2nd time actually prints everything
  // first loop is also printed to temproy file which is then read back in on the second loop

  for(to_file = 0; to_file < 2; to_file ++) { 

    // set array elements to zero
    loop=0;
    //    all_done=0;
    no_targs=0;
    start=0;
    if (to_file == 1) line_no=0;
    for(i = 0; i < 5000; i ++) {
      obj_line_done[i] = 0 ;
    }
    //    printf("here5\n");    

    if (to_file == 1) { // if this is the 2nd loop then read the tempory file back in
      // open file
      //      for(i = 1; i < argc; i ++) {
	if((fptr = fopen("tempory", "r")) == NULL) {
	  fprintf(stderr, "Error: Cannot open input file\n");
	  exit(-1);
	}
	//      }
      while( !feof(fptr) ) { // read every line into bigarr
	if(fgets(recin, sizeof(recin), fptr) == NULL) continue;
	strcpy(bigarr[line_no], recin) ;
	line_no = line_no + 1;
      }
      no_visits = (line_no - 1) /12; // this is NOT number of targets
      fclose(fptr);
    }




    if (to_file == 0){ // first loop will write sorted data to a tempory file ... 
      if((fptr = fopen("tempory", "w")) == NULL) {
	fprintf(stderr, "Error: Cannot open input file\n");
	exit(-1);
      }
    }
    
    
    //    for(i = 0; i < 13; i ++) { // print the first "pole" target
      if (to_file == 0) {
	//	fprintf(fptr,"%s\n",bigarr[i] );// first loop will write sorted data to a tempory file ... 
	fprintf(fptr,"%s\n","pole");
	fprintf(fptr,"%s\n","0 00 00");
	fprintf(fptr,"%s\n","-89 59 59");
	fprintf(fptr,"%s\n","2000");
	fprintf(fptr,"%s\n","1");
	fprintf(fptr,"%s\n","1");
	fprintf(fptr,"%s\n","0");
	fprintf(fptr,"%s\n","0");
	fprintf(fptr,"%s\n","none");
	fprintf(fptr,"%s\n","0");
	fprintf(fptr,"%s\n","0");
	fprintf(fptr,"%s\n","none");

      }
      //      if (to_file == 1) { 
      //	//	printf("%s",bigarr[i] );// 2nd loop will print data to command line
      //	printf("%s\n","pole");
      //	printf("%s\n","0 00 00");
      //	printf("%s\n","-89 59 59");
      //	printf("%s\n","2000");
      //	printf("%s\n","1");
      //	printf("%s\n","1");
      //	printf("%s\n","0");
      //	printf("%s\n","0");
      //	printf("%s\n","none");
      //	printf("%s\n","0");
      //	printf("%s\n","0");
      //	printf("%s\n","none");

      //      }
      //    }
    obj_line_done[1] = 1 ;
    
    
    while (start < line_no) {
      //      all_done = 1;
      strcpy(current_name, bigarr[start]) ; // current_name is the current target name being compared
      strcpy(current_sat, bigarr[start+8]) ; // current_name is the current target name being compared
      //           if (to_file == 1) printf("SAT= %i %s\n",start,current_sat);

      for(i = (start); i < line_no; i=i+12) {
	if ((loop == 0) &&  strncmp(bigarr[i],bigarr[i-12] ,strlen(bigarr[i])) != 0) no_targs=no_targs+1;
	
	if ((strncmp(bigarr[i],current_name ,strlen(current_name)) == 0) && (obj_line_done[i] ==0) && 
	    (strncmp(bigarr[i+8],current_sat , strlen(current_sat)) == 0)) { // compare targ and sat names
	  for(j = i; j<(i+12); j ++) {
	    if (to_file == 0) fprintf(fptr,"%s",bigarr[j] );
	    if (to_file == 1) printf("%s",bigarr[j]);
	  }
	  obj_line_done[i] = 1 ;	  
	}
      } // end for
      
      loop = 1;
      start=start+12;
      //      if (obj_line_done[i] == 0) all_done=0 ;	  
      

    } // end while
    
    //      if (to_file == 0) fprintf(fptr,"%s",bigarr[i] );
      if (to_file == 1) printf("%i\n",no_targs );
      fclose(fptr);      

  } //to_file loop
  
  exit(0);
}
