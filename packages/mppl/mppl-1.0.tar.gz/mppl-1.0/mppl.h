/*
 * Following code largely follows that given in pact/score/scstd.h.
 * Thanks, guys!
 */

#ifdef ANSI_F77
# define FF_ID(x, X)  X
#endif

#ifdef _AIX
# define FF_ID(x, X)  x
#endif

#ifdef __hpux
# define FF_ID(x, X)  x
#endif

#ifdef _UNICOS
# define FF_ID(x, X)  X
# define FF_EXTERN
#endif

#ifndef FF_ID
# define FF_ID(x, X)  x ## _
#endif

#ifndef FCB_ID
# define FCB_ID(x, X) FF_ID(x, X)
#endif

#ifndef FF_EXTERN
# define FF_EXTERN extern
#endif

/* String handling macros */

#ifdef _UNICOS

# ifndef __cplusplus
#  include <fortran.h>

typedef _fcd F77_string;

#  define SC_F77_C_STRING(_f) _fcdtocp((_f))
#  define SC_C_F77_STRING(_c) _cptofcd((_c), ((_c) ? strlen((_c)) : 0))

# else /* __cplusplus */

typedef char *F77_string;

#  define SC_F77_C_STRING(_f) ((char *) _f)
#  define SC_C_F77_STRING(_c) ((char *) _c)

# endif /* not __cplusplus */

#else /* not UNICOS */

typedef char *F77_string;

#define SC_F77_C_STRING(_f) ((char *) _f)
#define SC_C_F77_STRING(_c) ((char *) _c)

#endif /* UNICOS */

#define SC_FORTRAN_STR_C(c_string, f_string, n_chars)                        \
   {strncpy(c_string, SC_F77_C_STRING(f_string), n_chars);                   \
    c_string[n_chars] = '\0';}
