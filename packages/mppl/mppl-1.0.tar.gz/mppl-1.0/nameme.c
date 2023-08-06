#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#include "mppl.h"
#include "scon.h"

static int findname(char *p);
static void pathsplit(char **pv,char *path);
static void copyto(char *d,char *s,int n);

#define Nameme0 FF_ID(nameme0, NAMEME0)
#define Cpathvars FCB_ID(cpathvars, CPATHVARS)
#define Ipathvars FCB_ID(ipathvars, IPATHVARS)

typedef struct {
    char a0[FILENAMESIZE];
    char rn[FILENAMESIZE];
    char rp[FILENAMESIZE];
} cpath_t;
typedef struct {
    int l1,l2,l3;
} ipath_t;
FF_EXTERN cpath_t Cpathvars;
FF_EXTERN ipath_t Ipathvars;
#define argv0    (Cpathvars.a0)
#define realname (Cpathvars.rn)
#define realpath (Cpathvars.rp)
#define len1     (Ipathvars.l1)
#define len2     (Ipathvars.l2)
#define len3     (Ipathvars.l3)

/*
  Return a program's "realname" and "realpath".  The "argv0" argument
  is typically argv[0].  The function skips over any symbolic links
  on the way to the final name of the executable.  It uses the PATH
  environment variable to find the executable if "argv0" is not an
  absolute pathname.  After the final pathname to the executable is
  decided upon, "realname" is set to the last component of the pathname,
  and "realpath" to its prefix.
  This particular version is designed to be called from Fortran.
*/
void Nameme0(void)
{
    char *getenv(),*cp,*pv0[256],**pv,path[1024];

    pathsplit(pv0,getenv("PATH"));
    argv0[len1] = '\0';
    if(strchr(argv0,'/') == 0){ /* We have a relative pathname */
	for(pv = pv0;*pv;pv++){
	    sprintf(path,"%s/%s",*pv,argv0);
	    if(findname(path) == 0) break;
	}
    }else{ /* We have an absolute pathname */
	strcpy(path,argv0);
	(void) findname(path);
    }

    for (pv = pv0;*pv;pv++)
	free(*pv);

    cp = strrchr(path,'/');
    copyto(realname,1+cp, len2);
    *cp = '\0';
    copyto(realpath, (*path == '\0') ? "/" : path, len3);
}

static void copyto(char *d,char *s,int n)
{
#define min(a,b) ((a)<(b))?a:b
    (void)memcpy(d,s,min(strlen(s),n));
}

/*
  Given a colon-separated list of path components in "path", generate
  a vector of path components.  Null components are returned as '.'.
  The returned vector is null terminated.
*/
static void pathsplit(char **pv,char *path)
{
    int nc;
    char *p = path, *p2;

    while(*p != '\0'){
	if(*p == ':'){
	    if(p==path || *(p+1) == ':' || *(p+1) == '\0'){ /* Null entry */
		*pv = (char *)malloc(2);
		strcpy(*pv,".");
		pv++;
		p++;
	    }else{
		p2 = ++p;
		while(*p2 != ':' && *p2 != '\0') ++p2;
		nc = (p2-p) + 1;
		*pv = (char *)malloc(p2-p+1+1);
		strncpy(*pv,p,nc);
		(*pv)[nc-1] = '\0';
		pv++;
		p = p2;
	    }
	}else{
	    p2 = p;
	    while(*p2 != ':' && *p2 != '\0') ++p2;
	    nc = (p2-p) + 1;
	    *pv = (char *)malloc(p2-p+1+1);
	    strncpy(*pv,p,nc);
	    (*pv)[nc-1] = '\0';
	    pv++;
	    p = p2;
	}
    }
    *pv = (char *)NULL;
}

#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
/*
  Given a pathname, determine if it is a symbolic link.  If so,
  continue searching to the ultimate terminus - there may be
  more than one link.  Use the error value to determine when the
  terminus is reached, and to determine if the pathname really
  exists.  Then stat it to determine whether it's executable.
  Return 0 for an executable, errno otherwise.  Note that 'p'
  *must* have at least one '/' character - it does by construction
  in this program.  The contents of the array pointed to by 'p'
  are changed to the actual pathname if findname is successful.
*/
static int findname(char *p)
{
    int n;
    char buf[1024],*cp;
    extern int errno;
    struct stat sbuf;

    while((n = readlink(p,buf,1024)) > 0){
	if(buf[0] == '/'){ /* Link is an absolute path */
	    strncpy(p,buf,n);
	    p[n] = '\0';
	}else{ /* Link is relative to its directory; make it absolute */
	    cp = 1 + strrchr(p,'/');
	    strncpy(cp,buf,n);
	    cp[n] = '\0';
	}
    }

/* SGI machines return ENXIO instead of EINVAL Dubois 11/92 */
    if(errno == EINVAL || errno == ENXIO){
	if((stat(p,&sbuf) == 0) && S_ISREG(sbuf.st_mode)){
	    return(access(p,X_OK));
	}
    }
    return(errno ? errno : -1);
}
