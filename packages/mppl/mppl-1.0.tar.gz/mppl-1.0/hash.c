/*
   Hash table routines.  To simplify the interface with Fortran,
   addresses are kept entirely within this file.  The objects exchanged
   with Fortran are "folded indices".  This is very simple minded.
   The hash table is viewed as a 2D array.  The row R of a given object is
   just its usual hash index, in [0,HASHSIZE-1].  The column index C is
   its position in the linked list originating on that row, [0,CMAX-1],
   where CMAX is the longest such list taken over the entire hash table.
   Given R and C, the folded index of an item is F = C*HASHSIZE + R.

   Given F, compute C = F/HASHSIZE and R = F%HASHSIZE.
 */
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include "mppl.h"

#define HASHSIZE 501
#define rowno(F) ((F)%HASHSIZE)
#define colno(F) ((F)/HASHSIZE)
#define foldedindex(R,C) ((C)*HASHSIZE + (R))

typedef int Integer;
typedef struct macrostruct {
    int deflen;
    int namlen;
    int supchar;
    char *namptr;
    char *defptr;
    struct macrostruct *nextdef;
}  Macro;

static Macro *hshtab[HASHSIZE];
static int casesen;

/* Fortran external names */
#define Dumpdf  FF_ID(dumpdf, DUMPDF)
#define Lookup  FF_ID(lookup, LOOKUP)
#define Putdef  FF_ID(putdef, PUTDEF)
#define Readdef FF_ID(readdef, READDEF)
#define Dumpa   FF_ID(dumpa, DUMPA)
#define Finish  FF_ID(finish, FINISH)
#define Instal  FF_ID(instal, INSTAL)
#define Notsen  FF_ID(notsen, NOTSEN)
#define Setsen  FF_ID(setsen, SETSEN)
#define Tabini  FF_ID(tabini, TABINI)
#define Unstal  FF_ID(unstal, UNSTAL)
#define Setsup FF_ID(setsup, SETSUP)
#define Getsup FF_ID(getsup, GETSUP)

Integer Dumpdf (Integer *lname, Integer name[]);
Integer Lookup (Integer *leng, Integer name[]);
Integer Putdef (Integer *fi, Integer *ev, Integer *ep, Integer *evalsize);
Integer Readdef (Integer *idp, F77_string val);
void Dumpa (void);
void Finish (Integer *i);
void Instal (Integer name[], Integer *lname, Integer defn[], Integer *ldefn);
void Notsen (void);
void Setsen (void);
void Tabini (void);
void Unstal (Integer name[],Integer *lname);

static Macro *aof(int q);
static int hash(Integer s[], int n);
static void dump1(Macro *x);

static int hash(Integer s[], int n)
{
    int i,j;

    if(casesen) {
	for(i=0,j=0;i<n; j+=(int)s[i++])
	    ;
    } else {
	char c;
	for(i=0,j=0;i<n; i++) {
	    c = s[i];
	    if(islower(c)) c=toupper(c);
	    j+= (int) c;
	}
    }
    return(j%HASHSIZE);
}

void Tabini(void)
{
    int i;
    for(i = 0; i<HASHSIZE; i++)
	hshtab[i] = (Macro *) NULL;
}

static Macro *aof(Integer q)
{
    int k=0;
    Macro *p;

    if( -1 == q ) return 0;
    p=hshtab[rowno(q)];
    while( p && (colno(q)>k++) ){ p=p->nextdef; }
    return p;
}

/* install a name and defn, which are in integer form */
void Instal (Integer name[], Integer *lname, Integer defn[], Integer *ldefn)
{
    int i,hsh;
    Macro *knext,*k;
    Macro *m;
    char *x;

    m= aof(Lookup (lname,name));
    if(m != (Macro *) NULL) {   /* redefinition */
	free(m->defptr);
	m->defptr = (char *) malloc((size_t)((*ldefn)+1));
	m->deflen = *ldefn;
	x = m->defptr;
	for(i=0;i< *ldefn;i++)
	    x[i] = (char) defn[i];
	x[*ldefn]='\0';
	return;
	}
    m = (Macro *) malloc(sizeof(Macro));
    m->nextdef = (Macro *)NULL;
    m->namlen = *lname;
    m->deflen = *ldefn;
    m->namptr = (char *) malloc((size_t)((*lname)+1));
    m->defptr = (char *) malloc((size_t)((*ldefn)+1));
    m->supchar = 0;
    x = m->namptr;
    for(i=0;i< *lname;i++) {
	x[i] = (char) name[i];
    }
    x[*lname]='\0';
    x = m->defptr;
    for(i=0;i< *ldefn;i++)
	x[i] = (char) defn[i];
    x[*ldefn]='\0';
    hsh = hash(name,*lname);
    knext = hshtab[hsh];
    if(knext == (Macro *)NULL) {
	hshtab[hsh] = m;
	return;
    }
    k = knext;
    knext = k->nextdef;
    while(knext != (Macro *) NULL) {
	k = knext;
	knext = knext->nextdef;
    }
    k->nextdef = m;
}

Integer Setsup(Integer *fi, Integer *supchar)
{
    Macro *m;
    m= aof(*fi);
    if(m != (Macro *) NULL) {
        m->supchar = *supchar;
    }
    return 0;
}

Integer Getsup(Integer *fi, Integer *supchar)
{
    Macro *m;
    m= aof(*fi);
    if(m != (Macro *) NULL) {
        *supchar = m->supchar;
    }
    return 0;
}

Integer Lookup (Integer *leng, Integer name[])
{
    int j = hash(name,*leng);
    Macro *m;
    int	k = 0;
    int found = 0;

    m = hshtab[j];
    while( m && !found ) {
	int i = 0;
	char *x = m->namptr;
	if(m->namlen != *leng){
	    m = m->nextdef;
	    k++;
	    continue;
	}
	if(casesen){
	    while(i< *leng){
		if( x[i] != (char) name[i]) break;
		i++;
	    }
	}else{
	    char c,d;
	    while(i< *leng){
		c = (char) name[i];
		if(islower(c)) c=toupper(c);
		d = x[i];
		if(islower(d)) d=toupper(d);
		if( c != d) break;
		i++;
	    }
	}
	if(i == *leng) found = 1;
	m = m->nextdef;
	k++;
    }
    if(found){ return(foldedindex(j,k-1)); }
    return(-1);
}

Integer Putdef (Integer *fi, Integer *ev, Integer *ep, Integer *evalsize)
{
    /* put definition from table onto ev */
    Macro *m;
    Integer epnew;
    int i,n,base;
    char * x;

    m = aof(*fi);
    n = m->deflen;
    epnew = *ep + n;
    if(epnew > *evalsize) {
	return((Integer)1);
    }
    x = m->defptr;
    base = (*ep)-1;  /* ep is 1-origin pointer into ev */
    for( i=0; i< n; i++)
	ev[base + i] = (Integer) x[i];
    *ep = epnew;
    return((Integer)0);
}

void Unstal (Integer name[],Integer *lname)
{
    int j;
    Macro *knext,*k;
    Macro *m;

    m=aof(Lookup (lname,name));
    if(m != (Macro *) NULL) {
	free(m->namptr);
	free(m->defptr);
	j = hash(name, *lname);
	if (hshtab[j] == m) {
	    hshtab[j] = m->nextdef;
	    free( (char *) m);
	}
	else {
	    knext=hshtab[j];
	    k = knext;
	    knext = k->nextdef;
	    while(knext != m) {
		k = knext;
		knext = knext->nextdef;
	    }
	    k->nextdef = knext->nextdef;
	}
    }
}

void Dumpa (void)
{
    /* dump all definitions */
    int jj;
    int nmacros, nused;
    Macro *k;
    nused=0;
    nmacros=0;
    for(jj=0;jj<HASHSIZE;jj++) {
	if(hshtab[jj] != (Macro *) NULL) {
	    nused++;
	    k = hshtab[jj];
	    dump1(k);
	    nmacros++;
	    k = hshtab[jj]->nextdef;
	    while(k != (Macro *) NULL) {
		dump1(k);
		nmacros++;
		k = k->nextdef;
	    }
	}
    }
    (void)fprintf(stderr,
		  "%d macros using %d hash-table slots of %d\n",
		  nmacros,nused,HASHSIZE);

    if(nmacros==0) return;
    (void)fprintf(stderr,"Average depth %f\n",nmacros/((float)nused));
}

Integer Dumpdf (Integer *lname, Integer name[])
{
    Macro *x = aof(Lookup (lname,name));
    if(x){
	dump1(x);
	return((Integer) 0);
    }
    return((Integer) 1);
}

static void dump1(Macro *x)
{
    int i;
    char c;

    (void) fprintf(stderr,"Name: %s\n",x->namptr);
    (void) fprintf(stderr,"Definition:");
    if(x->deflen >= 68) (void) fprintf(stderr,"\n");
    for(i=0; i<(x->deflen);i++) {
	c=x->defptr[i];
	if( c=='\n') putc(c,stderr);
	else if(! isprint(c)) c='?';
	(void) putc(c,stderr);
    }
    putc('\n',stderr);
}

void Setsen (void) { casesen = 1; }
void Notsen (void) { casesen = 0; }
void Finish (Integer *i) { exit(*i); }

/*
   Given a pointer into the hash table, read a definition, storing
   the string value in "val".  Return the length of val.  Supposed
   to be called only when we know there's something to read.
*/
Integer Readdef (Integer *idp, F77_string val)
{
    Macro *dp = aof(*idp);
    strncpy(SC_F77_C_STRING(val),dp->defptr,dp->deflen);
    return((Integer)dp->deflen);
}
