#!/bin/sh

set -- `uname -srm`
osnam=${OSNAM:-$1}
osrel=${OSREL:-$2}
osarch=${OSARCH:-$3}
# Need a valid identifier for later eval.  Convert funny stuff to underscore.
osid=`echo ${OSNAM:-$1} | sed 's/[-.]/_/g'`

# default values for init0.f
stdin=5 stdout=6 stderr=0 # (Fortran unit numbers, not file descriptors.)
intsize=4 realsize=4 wordsize=32

# default values for makefile
fc=gfortran fflags= fopt=-O fdef= finc= flinc=
cc=cc  cflags= copt=-O cdef= cinc= clinc=
mppl=mppl mflags= mdef= minc=
lex=lex lexflags=
loadflags= loadlibs=
debug=

# Set up functions for the various systems.
set_Linux()
{
  if [ $osarch = "alpha" ] ; then
    system=LINUXA
  else
    system=LINUX  
    fc=pgf77
    lexflags=-l
    lexflags=
    fc=gfortran
  fi
}

set_Darwin()
{
    system=OSX  
    lexflags=-l
    lexflags=
    fc=gfortran
}

# values for killeen.nersc.gov
set_sn9605()
{
  fc=f90
  fopt=-O2
  cflags="-DUNICOS -DJ90"
  system=UNICOS
  wordsize=64
  realsize=8
}

# values for seymour.nersc.gov
set_sn9602()
{
  fc=f90
  fopt=-O2
  cflags="-DUNICOS -DJ90"
  system=UNICOS
  wordsize=64
  realsize=8
}

set_HP_UX()
{
  stderr=7
  system=HP700
  cflags="-Ae +DAportable"
  fflags="+DAportable +U77"
  loadflags=+U77
}

set_OSF1()
{
  system=AXP
  fflags="-align dcommons -recursive -V"
  loadflags=-call_shared
}

set_SunOS()
{
  OIFS="$IFS" IFS=.
  set -- $osrel
  if [ $1 = 5 ]
  then
    system=SOL
    fflags=-stackvar
  else
    system=SUN4
    cc=acc
  fi
  IFS="$OIFS"
}

set_IRIX()
{
  system=SGI
  fflags=-mips2
}

set_IRIX64()
{
  system=IRIX64
  fflags="-woff 2290"
  cflags="-common -woff 1167"
}

set_AIX()
{
  system=RS6000
  fflags="-qfixed -qnosave"
}

# Function to write the init0 Fortran subroutine for mppl.
wrt_init0()
{
  cat <<EOF
c This file was written by the init.sh script.  Change that, not this.

      call aampp
      end

      subroutine init0(stdin,stdout,stderr,intsize,realsize,wordsize,
     &system)
      integer stdin,stdout,stderr,intsize,realsize,wordsize
      character *(*) system
      stdin = $stdin
      stdout = $stdout
      stderr = $stderr
      intsize = $intsize
      realsize = $realsize
      wordsize = $wordsize
      system = "$system"
      end
EOF
}

# Write the flags portion of the makefile.  Note that environment
# variables get the final say.
wrt_mflags()
{
  cat <<EOF
DEBUG = ${DEBUG:-$debug}

FC = ${FC:-$fc}
FFLAGS = ${FFLAGS:-$fflags}
FOPT = ${FOPT:-$fopt}
FDEF = ${FDEF:-$fdef}
FINC = ${FINC:-$finc}
FLINC = ${FLINC:-$flinc}

CC = ${CC:-$cc}
CFLAGS = ${CFLAGS:-$cflags}
COPT = ${COPT:-$copt}
CDEF = ${CDEF:-$cdef}
CINC = ${CINC:-$cinc}
CLINC = ${CLINC:-$clinc}

LOADFLAGS = ${LOADFLAGS:-$loadflags}
LOADLIBS = ${LOADLIBS:-$loadlibs}

MPPL = ${MPPL:-$mppl}
MFLAGS = ${MFLAGS:-$mflags}
MDEF = ${MDEF:-$mdef}
MINC = ${MINC:-$minc}

LEX = ${LEX:-$lex}
LEXFLAGS = ${LEXFLAGS:-$lexflags}

MINUSN = ${MINUSN}
CESC = ${CESC}
EOF
}

# MAIN
MINUSN= CESC=\"\\c\"
set -- `echo "\c"`
[ "$1" = "\c" ] && { MINUSN=-n ; CESC= ; }

eval set_$osid || { echo "No setup function found for $osnam"; exit 1; }
wrt_init0 > init0.f
wrt_mflags > makefile
cat makeskel >> makefile
