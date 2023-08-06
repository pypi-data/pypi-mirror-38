%{
/*
   Nextline.l is a lex routine which reads Mppl input and converts
   Fortran 90 literal constants to Fortran 77 syntax.  For historical
   reasons, it passes input back to mppl one line at a time.
*/
#include <ctype.h>
#include "scon.h"
#include "mppl.h"

typedef int Integer;

#define CTLVARS FCB_ID(ctlvars, CTLVARS)
#define CINBUF FCB_ID(cinbuf, CINBUF)

#if defined(__osf__) || defined(__hpux)
    typedef unsigned char yytext_t;
#else
    typedef char yytext_t;
#endif

#if defined(sun) && !defined(__SVR4)
int yywrap(){return 1;}
#else
int yywrap(void){return 1;}
#endif

/* Keep the loader happy - some lexes stick in a reference to main(), but
   we're calling this stuff from Fortran, and it shows up as an
   unsatisfied reference without the following stub. */
#if defined(__hpux)
static int main(){}
#endif

/* Array of FILE pointers - the Fortran code believes it is handling
   Fortran unit identifiers, but in fact it gets file descriptors,
   which are used to index this array of FILE pointers.  Strictly
   speaking, we should only need MPPL_MAXINLEV+3 elements, but fileno()
   on UNICOS 8 doesn't return contiguous integers.
*/
static FILE *fpa[99];  /* this could probably be [FOPEN_MAX] */
#ifdef FLEX_SCANNER
static YY_BUFFER_STATE include_stack[99];
static int include_stack_ptr = 0;
#endif

/* Following two structs map common blocks from Fortran */
typedef struct {
    Integer lexwarn,
	realsize,
	intsize,
	wordsize,
	inlev,
	finerr,
	nodblquo,
	yyline[MPPL_MAXINLEV];
} ctlvars_t;
FF_EXTERN ctlvars_t CTLVARS;

typedef struct {
    yytext_t cbuf[MPPL_MAXCARD];
} cinbuf_t;
FF_EXTERN cinbuf_t CINBUF;

/* Some short names for particular structure elements */
#define Errcnt CTLVARS.finerr
#define Nodblq CTLVARS.nodblquo
#define Linenum (1+CTLVARS.yyline[CTLVARS.inlev-1])
#define Cbuf CINBUF.cbuf

/* Macros used repeatedly in yylex */
#define Cp		(void)strcpy(cbp,(char *)yytext);cbp+=strlen(yytext)
#define Write(a,b)	(void)sprintf((char *)cbp,a,b);cbp+=strlen(cbp)

/* Functions called by yylex */
static char *modflt(Integer size,Integer wordsize);
static char *modint(Integer size,Integer wordsize);
static void dosquote(void);
static void dodquote(void);

/* Global variables */
static char filename[FILENAMESIZE]; /* The current input filename */
static yytext_t *cbp; /* Pointer onto the string buffer passed from Fortran */

%}

%Start Im
%k 2000

sign	([+-])
dec	([0-9]+[.][0-9]*)
frac	([.][0-9]+)
exp	([dDeE]{sign}?[0-9]+)
LitFlt	({sign}?(([0-9]+{exp})|(({dec}|{frac}){exp}?)))
LitInt	({sign}?[0-9]+)

Relop	"."([a-zA-Z]{2,7})"."
W	([ \t])
FldDesc	([0-9]*[pP]*[0-9]*[dDeEfFgGiI][0-9]+"."[0-9]+)
Name	([a-zA-Z_][a-zA-Z0-9_]*)

S1	("1"|"Size1")
S2	("2"|"Size2")
S4	("4"|"Size4")
S8	("8"|"Size8")
S16	("16"|"Size16")

Implicit	([iI][mM][pP][lL][iI][cC][iI][tT])
None		([nN][oO][nN][eE])
Real		([rR][eE][aA][lL])
Integer		([iI][nN][tT][eE][gG][eE][rR])
Complex		([cC][oO][mM][pP][lL][eE][xX])

%%

^[cC*#!].*\n		|
^{W}*include.*\n	|
{W}*#.*\n		|
{W}*!.*\n		|
\n			{ Cp;BEGIN 0;return(1); }

^{W}+{Implicit}		{ Cp;BEGIN Im; }
<Im>{None}		{ Cp; }
<Im>{Real}"*"   	{ Cp; }
<Im>{Real}{W}*"("{W}*[S148]	{ Cp; }
<Im>{Real}			{ Cp;Write("(%d)",CTLVARS.realsize); }
<Im>{Integer}"*"   	{ Cp; }
<Im>{Integer}{W}*"("{W}*[S248]	{ Cp; }
<Im>{Integer}			{ Cp;Write("(%d)",CTLVARS.intsize); }
<Im>{Complex}"*"   	{ Cp; }
<Im>{Complex}{W}*"("{W}*[S148]	{ Cp; }
<Im>{Complex}			{ Cp;Write("(%d)",CTLVARS.realsize); }

\"[^"\n]*\"		{ dodquote(); }
\'[^'\n]*\'		{ dosquote(); }
{sign}?[0-9]+{Relop}	|
{Relop}/[0-9]+		|
{FldDesc}		|
{Name}			{ Cp; }

{LitFlt}_{S4}		{ Write("%s",modflt(4,CTLVARS.wordsize)); }
{LitFlt}_{S8}		{ Write("%s",modflt(8,CTLVARS.wordsize)); }
{LitFlt}_{S16}		{ Write("%s",modflt(16,CTLVARS.wordsize)); }
{LitFlt}		{ Write("%s",modflt(CTLVARS.realsize,CTLVARS.wordsize)); }

{LitInt}_{S2}		{ Write("%s",modint(2,CTLVARS.wordsize)); }
{LitInt}_{S4}		{ Write("%s",modint(4,CTLVARS.wordsize)); }
{LitInt}_{S8}		{ Write("%s",modint(8,CTLVARS.wordsize)); }
{LitInt}		{ Write("%s",modint(CTLVARS.intsize,CTLVARS.wordsize)); }

.			{ *cbp++ = *yytext; }

%% /* END LEXICAL ANALYZER */


/*
    Read input until a newline is seen, copying from yytext into Cbuf.
    Translate literals as you go.  Return -1 in lcbuf for EOF, otherwise
    lcbuf is the linelength, less any trailing whitespace.
*/
#define Nextline FF_ID(nextline, NEXTLINE)
Integer Nextline (Integer *optnum)
{
    extern yytext_t *cbp;
    extern FILE *yyin;
    Integer lcbuf;
    char *s;

    cbp = Cbuf;
    lcbuf = 0;

    if (*optnum == 1) {
       if(yylex()){
	   while(isspace(*--cbp)) {}
   	   lcbuf = 1 + cbp - Cbuf;
       }else{
           lcbuf = -1;
       }
    } else {
       s = fgets(Cbuf, MPPL_MAXCARD, yyin);
       if (s == NULL) {
          lcbuf = -1;
       } else {
          /* don't include the newline */
          lcbuf = strlen(Cbuf) - 1;
       }
    }
    return(lcbuf);
}

/*
    Open the named file.  Return the file descriptor in fd if
    successful.  Store away the FILE pointer and reset yyin to
    the new file.
*/
#define Filopn FF_ID(filopn, FILOPN)
void Filopn (fd,ierr,lname,name)
Integer *fd, *ierr, *lname;
F77_string name;
{
    extern FILE *yyin;
    FILE *fp, *fopen();
    extern char filename[];
    char s[FILENAMESIZE];

    *ierr = -1;
    SC_FORTRAN_STR_C(s,name,*lname);
    if(strcmp(s,"-") == 0){ /* stdin, don't really open it */
	*ierr = 0;
	*fd = 0;
	fpa[*fd] = stdin;
	yyin = stdin;
	(void)strcpy(filename,"STDIN");
    }else if((fp = fopen(s,"r")) != NULL){
	*ierr = 0;
	*fd = fileno(fp);
	fpa[*fd] = fp;
	yyin = fp;
	(void)strcpy(filename,s);
    }
#ifdef FLEX_SCANNER
    if(0 == *ierr){
        include_stack[include_stack_ptr++] = YY_CURRENT_BUFFER;
        yy_switch_to_buffer( yy_create_buffer( yyin,  YY_BUF_SIZE ));
    }
#endif
}

/* Close any file except stdin. */
#define Filcls FF_ID(filcls, FILCLS)
void Filcls (fd)
Integer *fd;
{

    if(*fd)fclose(fpa[*fd]);
#ifdef FLEX_SCANNER
    yy_delete_buffer( YY_CURRENT_BUFFER );
#endif
}

/*
    Reset yyin and filename to the previously opened file.
    This function is usually called at the end of
    "include zzyyy" statements.
*/
#define Popyin FF_ID(popyin, POPYIN)
void Popyin (fd,lname,name)
Integer *fd, *lname;
F77_string name;
{
    extern FILE *yyin;
    extern char filename[];

    yyin = fpa[*fd];
    SC_FORTRAN_STR_C(filename,name,*lname);
#ifdef FLEX_SCANNER
    yy_switch_to_buffer( include_stack[--include_stack_ptr] );
#endif
}

/* Modify floating point literal constants appropriately. */
static char *modflt(Integer size,Integer wordsize)
{
	char *underscore = NULL, *expletter = NULL;
	static yytext_t s[128];
        char *t;

        s[0] = '\016';  /* NUMBER from mppl.i */
        s[1] = ' ';
        t = (char *) s + 2;
	(void)strcpy(t,(char *)yytext);
	/* Locate exponent letter and underscore, if present */
        for(; *t != '\0'; t++) {
	    if (isalpha(*t)) {
                expletter = t;
            } else if (*t == '_'){
		underscore = t;
		break;
	    }
	}
#if 0
	Integer i;
	for(i=0; i<yyleng; i++){
	    if(isalpha(s[i])) expletter = (char *) (s + i);
	    if(s[i] == '_'){
		underscore = (char *) (s + i);
		break;
	    }
	}
#endif
	/* First handle constants with 'd' exponent letter */
	if((expletter != NULL) && (*expletter == 'd' || *expletter == 'D')){
	    if(underscore != NULL){
		fprintf(stderr,
                "%s:%d: >>> %s <<< Use 'e' exponent letter instead\n",
		filename,Linenum,yytext);
		++Errcnt;
	    }else if(CTLVARS.lexwarn)
	        fprintf(stderr,
                "%s:%d: Constant size may vary >>> %s <<< Use '_Size' suffix\n",
		filename,Linenum,yytext);
            s[1] = strlen(s)-2;
	    return((char *) s);
	}

	/* Now the remaining constants */

	/* Whack off "_Size" suffix, if present */
	if(underscore != NULL) *underscore = '\0';

	switch(size){
	case 4:
	    /* Nothing to do */
	    break;
	case 8:
	    if(wordsize < 64)
	        if(expletter == NULL) strcat(s,"d0");
	        else *expletter = 'd';
	    break;
	case 16:
	    if(wordsize < 64 && CTLVARS.lexwarn)
		fprintf(stderr,
                "%s:%d: Size16 not available, using Size8 >>> %s <<<\n",
		filename,Linenum,yytext);
	    if(expletter == NULL) strcat(s,"d0");
	    else *expletter = 'd';
	    break;
	default:
	    fprintf(stderr,"%s:%d >>> %s <<< Unknown Size Specifier\n",
	    filename,Linenum,yytext);
	    ++Errcnt;
	    break;
	}

        s[1] = strlen(s)-2;
	return((char *) s);
}

/* Modify integer literal constants appropriately. */
static char *modint(Integer size,Integer wordsize)
{
	char *underscore = NULL;
        char *t;
	static yytext_t s[128];

	(void)strcpy(s,(char *)yytext);
	/* Locate underscore, if present */
	for(t = (char *) s; *t != '\0'; t++){
	    if(*t == '_'){
		underscore = t;
		break;
	    }
	}

	/* Whack off "_Size" suffix, if present */
	if(underscore != NULL) *underscore = '\0';

	switch(size){
	case 2:
	    /* Nothing to do */
	    break;
	case 4:
	    /* Also nothing to do */
	    break;
	case 8:
	    if(wordsize < 64 && CTLVARS.lexwarn)
		fprintf(stderr,
                "%s:%d: Size8 not available, using Size4 >>> %s <<<\n",
		filename,Linenum,yytext);
	    break;
	default:
	    fprintf(stderr,
	    "%s:%d >>> %s <<< Unknown Size Specifier\n",
	    filename,Linenum,yytext);
	    ++Errcnt;
	    break;
	}
	return((char *) s);
}

/*
   Change double-quoted things to single-quoted things for Fortran.
   Yytext has a double-quoted string in it.  Internal single quotes
   get doubled; double quotes are converted to single.
*/
static void dodquote(void)
{
    extern yytext_t *cbp;
    yytext_t *yp;

    if(!Nodblq){
	Cp;
	return;
    }
    for(yp=yytext;*yp;yp++){
	switch(*yp){
	case '\"': *cbp++ = '\''; break;
	case '\'': *cbp++ = '\''; *cbp++ = '\''; break;
	default: *cbp++ = *yp;
	}
    }
}

/*
   Change single-quoted things to single-quoted things for Fortran.
   (They may have double quotes in the interior of the string,
   which get changed to a pair of single quotes.)
*/
static void dosquote(void)
{
    extern yytext_t *cbp;
    yytext_t *yp;

    if(!Nodblq){
	Cp;
	return;
    }
    for(yp=yytext;*yp;yp++){
	switch(*yp){
	case '\"': *cbp++ = '\''; *cbp++ = '\''; break;
	default: *cbp++ = *yp;
	}
    }
}
