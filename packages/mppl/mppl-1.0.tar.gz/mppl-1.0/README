README for mppl, August, 2002.
See mppl.m for author information, and examples of mppl coding.
See mppl.1 for general documentation (Unix man page format).
See mppl.tex for Latex user manual.
see mpplslides.pdf for new Fortran 90 feature coverage.
See test/README for more information about testing, and mppl examples.
See PORTING for more on using mppl to adapt your codes to new platforms.

To make mppl:
    ./init.sh	 # Bourne-shell script, constructs init0.f and makefile.
    make	 # Builds mppl, assuming init.sh ran without errors.
    make check	 # Runs several regression tests.
    make install # Tells you how to install your new mppl.

You'll need a Fortran compiler, a C compiler, and lex.  Make sure all
these are found in your PATH environment variable.  If you have troubles,
inspect the setting of the various parameters as set by init.sh, and
placed into the makefile and init0.f.

To make mppl on entirely new system, say system XXX, you need to do this:

Find the Fortran and C compilers, and lex.  Make sure they're properly
in your PATH.

Run "uname -s".  This will tell you the operating system name, called
"osnam" in init.sh.  Suppose it returned XXX.

Add a function "set_XXX" to init.sh, and set any of the various parameters
as required to compile successfully.

NOTE: If you change mppl.m, you'll need to rebuild mppl.f.  (Naturally,
you first need a working copy of mppl to do this:)

    ./mppl mppl.m > mppl.f

We have tested:

AIX [345]
HP-UX 10.20, 11
IRIX 6.x
IRIX64 6.x
Linux 2.[24].x with pgf77 and g77
Tru64 4.0, 5.1
SunOS -- both SunOS 4 and SunOS 5 (Solaris)
UNICOS 10 -- J90 and SV1 hardware


Authors:
Paul F. Dubois, Lee Busby, Peter Willmann, Janet Takemoto, Lee Taylor
     Lawrence Livermore National Laboratory.

Please let us know if there is a problem.
basis-support@llnl.gov
