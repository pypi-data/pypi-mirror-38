#include "scon.h"
#include "mppl.h"

#define Scon FF_ID(scon, SCON)
typedef int Integer;

/*
 * The need to isolate certain size definitions into one place has
 * led to a strategy of defining them in scon.h, then having
 * mppl call this function to define the same manifest constant for
 * use in MPPL sources.
 */
Integer Scon(Integer *desired_type)
{
    switch (*desired_type){
	case 1: return (Integer) VARNAMESIZE;
	case 2: return (Integer) MPPL_MAXINLEV;
	case 3: return (Integer) MPPL_MAXCARD;
	case 4: return (Integer) FILENAMESIZE;
	default: return (Integer)0;
    }
}
