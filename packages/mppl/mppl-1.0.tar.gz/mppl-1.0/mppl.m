# Mppl was written by Paul F. Dubois, Lee Busby, Peter Willmann, and
# Janet Takemoto at Lawrence Livermore National Laboratory.
# All files in the Basis system are Copyright 1994-2002, by the Regents of
# the University of California.  All rights reserved.
# See "Copyright" for complete legal notice.
      
include mppl.i
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine aampp
      
c     external getarg, iargc
      integer i, iargc, jcd, idone
      character*128 argv(200)
      integer arg1, argc, firstfile
      Filename basisv
      logical obckeep, bv
      integer lnb
      external lnb
      
include_irset
include_fname
include_cfile
include_ctlvars
include_stdunits
include_pathvars
      
      call init0(stdin,stdout,stderr,intsize,realsize,wordsize,system)
      call init
      call tabini
      
      idone  = 0 
      finerr = 0
      nodblquo = 0
      lexwarn = NO
      ireset = .false.
      rreset = .false.
      
# There is a chicken and egg problem in setting intsize, realsize, and
# wordsize.  They need to be set before reading any input which contains
# literal integers or floating point constants, but you need to read
# "mppl.sys" in order to (properly) set wordsize.  Then that value of
# wordsize is used to set the default values for intsize and realsize for
# a given SYSTEM (which may have been set with a "-t" option).  However,
# the user may have set values for intsize and realsize by the command line
# options "-i" or "-r", so we need to check for that before (re)setting the
# wordsize-based defaults.  The upshot is that we compile in provisional
# values for intsize, realsize, and wordsize, check the command line for any
# changes to intsize or realsize, and use those while reading "mppl.sys".
# Finally, we use the wordsize read in to reset intsize or realsize,
# if they weren't set on the command line.  Given this order of events,
# it would be foolhardy to put any floating point literals in "mppl.sys".
#
#       1) Set provisional values in init0 for intsize, realsize, wordsize.
#       2) Check command line - may reset SYSTEM.
#       3) Read mppl.sys - sets WORDSIZE as function of SYSTEM.
#       4) Reread command line to over-ride default MACHINE or COMPILER.
#       5) Set intsize, realsize per wordsize unless given on command line.
#       6) Read mppl.std.
#       7) Read mppl.BASIS.
#       8) Process remaining input files.
#
# Intsize, realsize, wordsize changes after step 5 will produce
# undefined behavior.
      
      arg1 = 1
      argc = iargc()
      call getarg(arg1-1,argv0)
      do i = arg1, argc
         call getarg(i,argv(i))
      enddo
      
      bckeep = .true.
      for (i=arg1,argv(i)(1:1) == '-' & argv(i) <> '-',i=i+1)
          call setopt(argv(i)(2:))
      endfor
      firstfile = i
      obckeep = bckeep
      call init1
      
      realname = " "
      realpath = " "
      len1 = lnb(argv0)
      len2 = len(realname)
      len3 = len(realpath)
      call nameme0()
      jcd = lnb(realpath)
      sys=realpath(1:jcd)//"/mppl.sys"
      std=realpath(1:jcd)//"/mppl.std"
      basis=realpath(1:jcd)//"/mppl.BASIS"
      basisv=realpath(1:jcd)//"/BASIS_VERSION"
      
# These must be called after casesen is set ( -u )
      call bltin
      if (optmacro == YES) then
         call sharedconstants
         call cnstal('SYSTEM',system(1:lnb(system)))
# Turn off blank and comment line output while processing startup files.
         bckeep = .false.
         call dofile(sys)
# Reprocess the option list to over-ride defaults just read in.
         for (i=arg1,argv(i)(1:1) == '-' & argv(i) <> '-',i=i+1)
             call setopt(argv(i)(2:))
         endfor
#        endif
         
# Set intsize and realsize to final values.
         if (~ireset) intsize = 4
         call getwdsz(wordsize)
         if (~rreset)then
            if (wordsize < 64)then
               realsize = 4
            else
               realsize = 8
            endif
         endif
         call setsize('IntSize',intsize)
         call setsize('RealSize',realsize)
         
#        if (optmacro == YES) then
         if (optnum == YES) call dofile(std)
         if (basis <> " ") then
            call dofile(basis)
            inquire(file=basisv, exist=bv)
            if (bv) call dofile(basisv)
         endif
      endif
      
# Process remaining arguments as input files.
      bckeep = obckeep
      do i = firstfile, argc
         call dofile(argv(i))
      enddo
      if (firstfile > argc) call dofile(TTY)
      call finish(finerr)
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine wrline(unit,msg,n)
      integer n,unit
      character*(*) msg
      write(unit,100) msg(1:n)
 100  format(a)
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine rem(msg,n)
      character*(*) msg
include_stdunits
      integer n
      write(stderr,100) msg(1:n)
 100  format(1x,a)
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# ZPAKCHRZ - translate the integer string representation in AIN to
#          - a character representation in SOUT
      
      function zpakchrz(sout,lsout, ain,n)
      integer zpakchrz
      character*(*) sout
      integer ain(*), n, i, lsout
      
      zpakchrz = min(lsout, n)
      
      do i = 1, zpakchrz
         sout(i:i) = char(ain(i))
      enddo
      
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine bltin
# install names and defns of define, ifelse, etc... in table
include_cfile
      character*1 ceos
      character*2 c
      
      ceos=char(EOS)
      
      c=char(ESCAPE)
      
      c(2:) = char(DEFTYPE)
      call cnstal('mppl_define',c)
      
      c(2:) = char(IFELSETYPE)
      call cnstal('mppl_ifelse',c)
      
      c(2:)=char(IMMEDIATETYPE)
      call cnstal('mppl_Immediate',c)
      
      if (optmacro == YES) then
         call cnstal('Prolog','#Prolog')
#         call cnstal('Prolog',cchar//'Prolog')
         
         c(2:) = char(DEFTYPE)
         call cnstal('define',c)
         
         c(2:) = char(SMODTYPE)
         call cnstal('Module',c)
         
         c(2:) = char(IFDEFTYPE)
         call cnstal('ifdef',c)
         
         c(2:) = char(IFELSETYPE)
         call cnstal('ifelse',c)
         
         c(2:) =char(ERRPRINTTYPE)
         call cnstal('Errprint',c)
         
         c(2:) =char(INFOPRINTTYPE)
         call cnstal('Infoprint',c)
         
         c(2:)=char(DUMPDEFTYPE)
         call cnstal('Dumpdef',c)
         
         c(2:)=char(EVALUATETYPE)
         call cnstal('Evaluate',c)
         
         c(2:)=char(IMMEDIATETYPE)
         call cnstal('Immediate',c)
         
         c(2:)=char(SINCLUDE)
         call cnstal('include',c)
         
         c(2:)=char(UNDEFINETYPE)
         call cnstal('Undefine',c)
         
         c(2:)=char(REMARKTYPE)
         call cnstal('Remark',c)
         
      endif
      
      if (optlang .eq. LANG_F77) then
         
         c(2:)=char(SDO)
         call cnstal('do',c)
         
         c(2:)=char(SENDDO)
         call cnstal('enddo',c)
         
         c(2:)=char(SNEXT)
         call cnstal('next',c//' $1')
         
         c(2:)=char(SBREAK)
         call cnstal('break',c//' $1')
         
         c(2:)=char(MPROGRAM)
         call cnstal('program',c)
         
         c(2:)=char(MSUBROUTINE)
         call cnstal('subroutine',c)
         
         c(2:)=char(MFUNCTION)
         call cnstal('function',c)
         
         c(2:)=char(MEND)
         call cnstal('end',c)
         
         c(2:)=char(MRETURN)
         call cnstal('return',c//'mppl_ifelse($1,,,([$1]))')
         
         c(2:)=char(SWHILE)
         call cnstal('while',c//'mppl_ifelse($1,,,[mppl_Immediate([c while($1)])])([$1])')
         
         c(2:)=char(SENDWHILE)
         call cnstal('endwhile',c)
         
         c(2:)=char(SUNTIL)
         call cnstal('until',c//'mppl_ifelse($1,,,[mppl_Immediate([c until($1)])])([$1])')
         
         c(2:)=char(SIF)
         call cnstal('if',c//'([$1])')
         
         c(2:)=char(SELSE)
         call cnstal('else',c)
         
         c(2:)=char(SELSEIF)
         call cnstal('elseif',c//'([$1])')
         
         c(2:)=char(SENDIF)
         call cnstal('endif',c)
         
         c(2:)=char(STHEN)
         call cnstal('then',c)
         
         c(2:)=char(SSELECT)
         call cnstal('select',c//'mppl_ifelse($1,,, = $1)')
         
         c(2:)=char(SCASE)
         call cnstal('case',c//'$1')
         
         c(2:)=char(SDEFAULT)
         call cnstal('default',c//'$1')
         
         c(2:)=char(SESELECT)
         call cnstal('endselect',c)
         
         c(2:)=char(SFOR)
         call cnstal('for',c//'mppl_ifelse([$2],,,'//\
         '[mppl_Immediate([c -- for([$*])])[$1];go to @1;do;[$3];@1 if(.not.([$2])) break])')
         
         c(2:)=char(SEFOR)
         call cnstal('endfor',c)
         
         c(2:)=char(SBLOCK)
         call cnstal('block',c)
         
         c(2:)=char(MINTERFACE)
         call cnstal('interface',c)
         
      else if (optlang .eq. LANG_F90) then
         
         c(2:)=char(SDO90)
         call cnstal('do',c)
         
         c(2:)=char(SENDDO)
         call cnstal('enddo',c)
         
         c(2:)=char(SNEXT90)
         call cnstal('next',c//' $1')
         
         c(2:)=char(SBREAK90)
         call cnstal('break',c//' $1')
         
         c(2:)=char(MPROGRAM)
         call cnstal('program',c)
         
         c(2:)=char(MSUBROUTINE)
         call cnstal('subroutine',c)
         
         c(2:)=char(MFUNCTION)
         call cnstal('function',c)
         
         c(2:)=char(MEND)
         call cnstal('end',c)
         
         c(2:)=char(MRETURN)
         call cnstal('return',c//'mppl_ifelse($1,,,([$1]))')
         
         c(2:)=char(SWHILE90)
         call cnstal('while',c//'([$1])')
         
         c(2:)=char(SENDWHILE90)
         call cnstal('endwhile',c)
         
         c(2:)=char(SUNTIL90)
         call cnstal('until',c//'([$1])')
         
         c(2:)=char(SIF)
         call cnstal('if',c//'([$1])')
         
         c(2:)=char(SELSE)
         call cnstal('else',c)
         
         c(2:)=char(SELSEIF)
         call cnstal('elseif',c//'([$1])')
         
         c(2:)=char(SENDIF)
         call cnstal('endif',c)
         
         c(2:)=char(STHEN)
         call cnstal('then',c)
         
         c(2:)=char(SSELECT90)
         call cnstal('select',c//'mppl_ifelse($1,,, $1)')
         
         c(2:)=char(SCASE90)
         call cnstal('case',c//'$1')
         
         c(2:)=char(SDEFAULT90)
         call cnstal('default',c//'$1')
         
         c(2:)=char(SESELECT90)
         call cnstal('endselect',c)
         
         c(2:)=char(SFOR)
         call cnstal('for',c//
     &        'mppl_define([mppl_foriter],[$3])'   //
     &        'mppl_ifelse([$1],,,[$1]'//ceos//')' //
     &        'mppl_ifelse([$2],,,do while ([$2]))')
         
         c(2:)=char(SENDDO)
         call cnstal('endfor',c)
         
         c(2:)=char(SBLOCK)
         call cnstal('block',c)
         
         c(2:)=char(MINTERFACE)
         call cnstal('interface',c)

      else if (optmacro == YES) then
         # Define macros that enable us to define Module

         c(2:)=char(MPROGRAM)
         call cnstal('program',c)
         
         c(2:)=char(MSUBROUTINE)
         call cnstal('subroutine',c)
         
         c(2:)=char(MFUNCTION)
         call cnstal('function',c)
         
         c(2:)=char(MEND)
         call cnstal('end',c)
         
         c(2:)=char(SBLOCK)
         call cnstal('block',c)
         
         c(2:)=char(MINTERFACE)
         call cnstal('interface',c)

         if (optpretty == YES) then
            c(2:)=char(SDOI)
            call cnstal('do',c)
         
            c(2:)=char(SENDDO)
            call cnstal('enddo',c)
         
#            c(2:)=char(SLOOPI)
#            call cnstal('while',c)
         
#            c(2:)=char(SLOOPD)
#            call cnstal('endwhile',c)
         
#            c(2:)=char(SUNTIL)
#            call cnstal('until',c)
         
            c(2:)=char(SIF)
            call cnstal('if',c//'([$1])')
         
            c(2:)=char(SELSE)
            call cnstal('else',c)
         
            c(2:)=char(SELSEIF)
            call cnstal('elseif',c//'([$1])')
         
            c(2:)=char(STHEN)
            call cnstal('then',c)
         
            c(2:)=char(SENDIF)
            call cnstal('endif',c)
         
            c(2:)=char(SSELECTI)
            call cnstal('select',c)

#           case (1)   |   case default         
            c(2:)=char(SCASEI)
            call cnstal('case',c//'mppl_ifelse($1,,, ([$*]))')
         
#            c(2:)=char(SDEFAULTI)
#            call cnstal('default',c)
         
            c(2:)=char(SESELECT90)
            call cnstal('endselect',c)
         
#            c(2:)=char(SFOR)
#            call cnstal('for',c//' ([$*])')
         
#            c(2:)=char(SEFOR)
#            call cnstal('endfor',c)
         
         endif
         
      endif
      
      if (optalloc == YES) then
         c(2:)=char(MALLOCATE)
         call cnstal('allocate',c//'([$*])')

         c(2:)=char(MDEALLOCATE)
         call cnstal('deallocate',c//'([$*])')

         c(2:)=char(MSHAPE)
         call cnstal('Shape',c//'([$*])')
      endif

      c(2:) = char(SSETSUP)
      call cnstal('Setsuppress',c)

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine sharedconstants
# Install definitions for some basis and mppl constants.  It is convenient
# to do this here, because these constants receive their fundamental
# definition in scon.h.  They are also known and required by various
# C source routines.
      character *32 s
      integer scon, fnb
      external scon, fnb
      
      write(s,'(i8)') scon(1)
      call cnstal('VARNAMESIZE',s(fnb(s):))
      
      write(s,'(i8)') scon(2)
      call cnstal('MPPL_MAXINLEV',s(fnb(s):))
      
      write(s,'(i8)') scon(3)
      call cnstal('MPPL_MAXCARD',s(fnb(s):))
      
      write(s,'(i8)') scon(4)
      call cnstal('FILENAMESIZE',s(fnb(s):))
      
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      function fnb(s)
# Return the index of the first non-blank character in s.
      integer fnb
      character *(*) s
      fnb = 1
      while( (s(fnb:fnb) = ' ') & (fnb < len(s)) )
         fnb = fnb+1
      endwhile
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine cnstal(cname,cdef)
#install a definition, character string
#maximum lengths for name and defn 32 and 256 THIS ROUTINE ONLY
      integer name(32),def(256),i,lnb
      external lnb
      character*(*) cname,cdef
      integer lname,ldef
#
      lname = len(cname)
      ldef  = lnb(cdef)
      if (lname > 32 | ldef > 256)
         call oops('cnstal: name or defn too long')
      do i=1,lname
         name(i) = ichar(cname(i:i))
      enddo
      do i=1,ldef
         def(i) = ichar(cdef(i:i))
      enddo
      call instal(name,lname,def,ldef)
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine cpbstr(str)
#pushes back character string str
      character*(*) str
      integer i,n
      
      n = len(str)
      do i=n,1,-1
         call putbak(ichar(str(i:i)))
      enddo
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine tostr(out, token, ltoken)
      
      character*(*) out
      integer token(*), ltoken
      integer i
#      if (ltoken > len(out)) error
      out = " "
      do i=1,ltoken
         out(i:i) = char(token(i))
      enddo
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine doblock
include_cfile
include_cstat
      integer t,gnbtok
      external gnbtok
#
      call outtab(0,0)
      call putqs('block ')
      t = gnbtok(token,ltoken)
      call putchr(token,ltoken)
      if (ltoken == 4) then
# look for 'data' in lower or upper case
         if ((token(1)==100 | token(1) == 68) &
         (token(2)== 97 | token(2) == 65) &
         (token(3)==116 | token(3) == 84) &
         (token(4)== 97 | token(4) == 65) ) then
# next should be the module name
         call putqs(' ')
         t = gnbtok(token,ltoken)
         call putchr(token,ltoken)
         if (ltoken >  32)
            call warn('block module name too long')
         ltoken = min(ltoken,32)
         modtype(ifacelev) = SBLOCK
         call setmod(token,ltoken)
      endif
      endif
      call eatup(0)
      return
      end
#
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      function docond()
# evaluate and put out conditional
# translate >, >=, <,<=,~, ~=, <>, = or ==, ~ , ~=, &, |
# argument is a dummy, not used
# returns 0 if o.k., 1 otherwise
      integer docond
      character*(MAXTOK) oper
      integer t,nlev,loper,wswid
      integer gtok,gnbtokw
      external gtok,gnbtokw
include_cstat
include_cfile
      t = gnbtokw(token,ltoken,wswid)
      if ( t <> LPAREN) then
         call warn('Missing condition.')
         return(1)
      endif
      wswid = 1
#      if (optpretty == YES) wswid = 1
      call outfil(wswid)
      call putqs('(')
      nlev = 1
      if (optrel == LANG_F77) then
         while(nlev > 0)
            t = gtok(token,ltoken)
            if (t == LPAREN) then
               nlev = nlev + 1
               code(1) = LPAREN
               call putchr(code,1)
            elseif (t == RPAREN) then
               nlev = nlev - 1
               code(1) = RPAREN
               call putchr(code,1)
            elseif ( t == AMPERSAND ) then
               call putqs('.and.')
            elseif ( t == VBAR) then
               call putqs('.or.')
            elseif ( t == EQUALS) then
               call putqs('.eq.')
               t = gtok(token,ltoken)
# ok to have = or ==
               if ( t <> EQUALS) then
                  call pbstr(token,ltoken)
               endif
            elseif ( t == TILDE) then
               t = gtok(token,ltoken)
               if ( t <> EQUALS) then
                  call pbstr(token,ltoken)
                  call putqs('.not.')
               else
                  call putqs('.ne.')
               endif
            elseif ( t == LANGLE) then
               t = gtok(token,ltoken)
               if ( t == EQUALS) then
                  call putqs('.le.')
               elseif (t == RANGLE) then
                  call putqs('.ne.')
               else
                  call pbstr(token,ltoken)
                  call putqs('.lt.')
               endif
            elseif ( t == RANGLE) then
               t = gtok(token,ltoken)
               if ( t == EQUALS) then
                  call putqs('.ge.')
               elseif (t == LANGLE) then
                  call putqs('.ne.')
               else
                  call pbstr(token,ltoken)
                  call putqs('.gt.')
               endif
            elseif (t == COMMENT) then
               call endcomment(CBEFORE, 1, token, ltoken, 0)
               call outtab(0,0)
            elseif ( t == LINEFEED) then
               call conlin
            elseif ( t == NEWLINE) then
               call warn('Missing right parenthesis in condition.')
            else
               call putchr(token,ltoken)
            endif
         endwhile nlev > 0
      else if (optrel == LANG_F90) then
# F90 constructs
         while(nlev > 0)
            t = gtok(token,ltoken)
            if (t == LPAREN) then
               nlev = nlev + 1
               code(1) = LPAREN
               call putchr(code,1)
            elseif (t == RPAREN) then
               nlev = nlev - 1
               code(1) = RPAREN
               call putchr(code,1)
            elseif ( t == AMPERSAND ) then
               call putqs('.and.')
            elseif ( t == VBAR) then
               call putqs('.or.')
            elseif ( t == EQUALS) then
               call putqs('==')
               t = gtok(token,ltoken)
# ok to have = or ==
               if ( t <> EQUALS) then
                  call pbstr(token,ltoken)
               endif
            elseif ( t == TILDE) then
               t = gtok(token,ltoken)
               if ( t <> EQUALS) then
                  call pbstr(token,ltoken)
                  call putqs('.not.')
               else
                  call putqs('/=')
               endif
            elseif ( t == LANGLE) then
               t = gtok(token,ltoken)
               if ( t == EQUALS) then
                  call putqs('<=')
               elseif (t == RANGLE) then
                  call putqs('/=')
               else
                  call pbstr(token,ltoken)
                  call putqs('<')
               endif
            elseif ( t == RANGLE) then
               t = gtok(token,ltoken)
               if ( t == EQUALS) then
                  call putqs('>=')
               elseif (t == LANGLE) then
                  call putqs('/=')
               else
                  call pbstr(token,ltoken)
                  call putqs('>')
               endif
            elseif (t == LOGICAL) then
               call tostr(oper,token,ltoken)
               loper = ltoken
               if (oper == ".lt.") then
                  call putqs("<")
               else if (oper == ".le.") then
                  call putqs("<=")
               else if (oper == ".eq.") then
                  call putqs("==")
               else if (oper == ".ne.") then
                  call putqs("/=")
               else if (oper == ".gt.") then
                  call putqs(">")
               else if (oper == ".ge.") then
                  call putqs(">=")
               else
                  call putqs(oper(1:loper))
               endif
            elseif (t == COMMENT) then
               call endcomment(CBEFORE, 1, token, ltoken, 0)
               call outtab(0,0)
            elseif ( t == LINEFEED) then
               call conlin
            elseif ( t == NEWLINE) then
               call warn('Missing right parenthesis in condition.')
            else
               call putchr(token,ltoken)
            endif
         endwhile nlev > 0
      else if (optrel == LANG_IS_F90) then
         call oops("docond with LANG_IS_f90")
      endif
      return(0)
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine dodef(argstk,i,j)
#dodef -- install definition in table
      integer a1,a2,a3,argstk(1),i,j,jloc,k,ilo,ihi,lname
include_cmacro
include_cstat
include_ctype
      integer t,gettok
      external gettok
      if (j > i + 3) 
         call oops(' Wrong number of arguments in define.')
      jloc = j
 50   continue
# if called as a macro:
      a1 = argstk(i+2)
      a2 = argstk(i+3)
      if ( a2-a1 == 0 ) go to 100
      if ( jloc == i+3) then
         a3 = argstk(i+4)
      else
         a3 = a2
      endif
      do ilo = a1, a2-1 
         if (type(evalst(ilo))<>WHITE) break
      enddo
      do ihi = a2-1, a1, -1
         if (type(evalst(ihi))<>WHITE) break
      enddo
      lname = ihi -ilo + 1
      if (lname <=0) 
         call oops(' Empty name in define macro.')
      do k = ilo, ihi
         if (alphan(evalst(k))<>YES) 
         call oops(' Name not alphanumeric in define macro.')
      enddo 
      call instal(evalst(ilo),lname,evalst(a2),a3-a2)
      return
 100  continue #arguments not supplied, go get them
# note that this routine is called from eval called from gtok,
# so we can only use gettok , not gnbtok or gtok
      t = gettok(token,ltoken)
      if (t == WHITE)
         t = gettok(token,ltoken)
      if (t <> ALPHA)
         call oops('define not followed by name')
      do k=1,ltoken
         evalst(argstk(i+2)-1+k)=token(k)
      enddo
      argstk(i+3) = argstk(i+2) + ltoken
      argstk(i+4) = argstk(i+3)
      jloc = i + 3
# eatup rest of line as definition
      t = gettok(token,ltoken)
      if (t==WHITE)
         t=gettok(token,ltoken)
      while(t <> NEWLINE)
         if (t == COMMENT) break
         do k=1,ltoken
            evalst(argstk(i+4) - 1 + k) = token(k)
         enddo
         argstk(i+4) = argstk(i+4) + ltoken
         t = gettok(token,ltoken)
      endwhile
      go to 50
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# handles end, end do, end while, end if

      subroutine doend
      integer gnbtokw
      external gnbtokw
      integer t, wswid
      integer i23000
include_cfile
include_cstat

# sure, we've seen an end, but did they really mean it ?
      t = gnbtokw(token,ltoken,wswid)
      if (t == ALPHA) then
         call sendalpha
      elseif (t <> ESCAPE) then
         call sendmod(t, wswid)
      else
         select(token(2))
            case SDO, SDO90, SDOI:
               call sedo
            case SWHILE:
               call sewhile
            case SIF:
               call sendif
            case SFOR:
               call sefor
            case SSELECT:
               call seselect
            case SBLOCK, MSUBROUTINE, MFUNCTION, MPROGRAM:
               call sendmod(t,wswid)
            case MINTERFACE:
               call sendiface
            case SWHILE90:
               call sewhile90
            case SSELECT90, SSELECTI:
               call seselect90
            default:
               call warn('end followed by improper keyword')
         endselect
      endif
      
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine sendalpha
# This handles the case where select has been undefined.
# It will now be an ALPHA instead of SSELECT.
# also recognize 'end type'
      character*32 endmod
      integer lenmod, i
include_cstat
      
      endmod = ' '
      do i=1,ltoken
         endmod(i:i) = char(token(i))
      enddo
      lenmod = ltoken
      
      call outtab(0,0)
      
      if (endmod == 'module') then
# the trailing space is necessary if a name is given:  'end module foo'
         call putqs('end module ')
      else if (endmod == 'select') then
         call putqs('end select')
      else if (endmod == 'type') then
         call putqs('end type')
      else if (endmod == 'where') then
         call putqs('end where')
      else
         call warn('end followed by improper keyword')
      endif
      
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine sendmod(t,wswid)
# end a module (subroutine or function)
      
      integer gnbtokw
      external gnbtokw
      integer t, wswid
      integer ierr, i
      integer i23002
      integer lnb
      external lnb
      character*32 endname
include_cfile
include_cstat
      
      endname = ' '
      
      ierr = 0
      if (level <> 0) then
         call inform('do-block level not 0 at end.')
         ierr = 1
      elseif (iflevel <> 0) then
         call inform('if-block level not 0 at end.')
         ierr = 1
      elseif (sellev <> 0) then
         call inform('select statement level not 0 at end.')
         ierr = 1
      endif
      level = 0 ; iflevel = 0 ; sellev = 0
      
      call outtab(0,0)
      call putqs('end')
      
      if (token(1) == ESCAPE) then
         
         if (modtype(ifacelev) == token(2)) then
            if (token(2) == MFUNCTION) then
               call putqs(' function')
            else if (token(2) == MSUBROUTINE) then
               call putqs(' subroutine')
            else if (token(2) == MPROGRAM) then
               call putqs(' program')
            else if (token(2) == SBLOCK) then
               call putqs(' block data')
            endif
         else
            ierr = 1
            if (token(2) <> MFUNCTION) then
               call warn('Should be "end function"')
               call putqs(' function')
            else if (token(2) <> MSUBROUTINE) then
               call warn('Should be "end subroutine"')
               call putqs(' subroutine')
            else if (token(2) <> MPROGRAM) then
               call warn('Should be "end program"')
               call putqs(' program')
            else if (token(2) <> SBLOCK) then
               call warn('Should be "end block data"')
               call putqs(' block data')
            endif
         endif
         
         if (token(2) == SBLOCK) then
            t = gnbtokw(token,ltoken,wswid) # assume 'data'
         endif
         
# look for optional name
         t = gnbtokw(token,ltoken,wswid)
         if (t == ALPHA) then
            endname = ' '
            do i=1,ltoken
               endname(i:i) = char(token(i))
            enddo
            if (endname <> modname(ifacelev)) then
               call warn('Module name does not match')
               ierr = 1
            else
               call putqs(' ')
               call putqs(endname(1:ltoken))
            endif
            t = gnbtokw(token,ltoken,wswid)
         endif
      else if (optlang .eq. LANG_F90) then
         select (modtype(ifacelev))
            case MFUNCTION:   call putqs(' function ')
            case MSUBROUTINE: call putqs(' subroutine ')
            case MPROGRAM:    call putqs(' program ')
            case SBLOCK:      call putqs(' block data ')
         endselect
# GOTCHA - putting the subroutine name confuses the Guide90 compiler
#         if (modname(ifacelev) <> "?") 
#            call putqs(modname(ifacelev)(1:lnb(modname(ifacelev))))
      endif
      
      if (ifacelev == 0) then
         call setmod(QUESTION,1)
         modfun = YES
         modtype(ifacelev) = 0
# reset the label generator
         call reset
      endif
      if (t == COMMENT) then
         call endcomment(CBEFORE, 0, token, ltoken, wswid)
      else if (t == NEWLINE) then
         call outlin
      else if (ierr == 0) then
         call spit(CBEFORE)
      endif
      
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine doerrp(argstk,i,j)
      integer a1,a2,argstk(1),i,j,kk, iarg
      character*80 msg
include_cmacro
include_ctype
      do iarg = i + 2, j
         a1 = argstk(iarg)
         a2 = argstk(iarg+1)
         write(msg,'(80a)') (char(evalst(a1-1+kk)), kk=1, a2-a1)
         call warn(msg(1:a2-a1))
      enddo iarg
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine doinfop(argstk,i,j)
      integer a1,a2,argstk(1),i,j,kk, iarg
      character*80 msg
include_cmacro
include_ctype
      do iarg = i + 2, j
         a1 = argstk(iarg)
         a2 = argstk(iarg+1)
         write(msg,'(80a)') (char(evalst(a1-1+kk)), kk=1, a2-a1)
         call rem(msg,a2-a1)
      enddo iarg
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine dofile(fil)
      character*(*) fil
      integer gnbtok,gtok,toktoi,zpakchrz
      external gnbtok,gtok,toktoi,zpakchrz
      character*(MPPL_MAXCARD) msg
      integer t,blanks(5),i,k
      integer idoflg, kesc
      integer i23007
      integer initio
      external initio

include_idircom
include_cmacro
include_cargs
include_cstat
include_cfile
include_stdunits

      do i=1,5
         blanks(i) = BLANK
      enddo

      indpc  = 0
      indflg = 0
      
      if (initio(fil) == ERR) return

# reset the label counter
      call reset

# initialize the argument stack
      cp = 0
      ap = 1
      ep = 1

# count of square brackets
      nlb = 0

# do/while/if levels
      level = 0
      iflevel = 0
      dotype(0) = 0
      labn(0) = 0
      labb(0) = 0
      usen(0) = NO
      useb(0) = NO

# select stuff
      seltop = 0
      sellev = 0
      sellast = 1

# module name
      ifacelev = 0
      modtype(ifacelev) = 0
      call setmod(QUESTION,1)
      icontinue = 0

# idoflg = YES after seeing the label which terminates a regular do
      idoflg = NO

# process this file
# gtok returns the next token after expanding macros
# each for loop does one statement
      for (t=gtok(token,ltoken), t <> EOF , t=gtok(token,ltoken))

# if the previous statement was the end of a standard do statement...
          if (idoflg = YES) then
             call sedo
             idoflg = NO
          endif
          
          if (t == WHITE) then
             indpc = ltoken
             t = gtok(token,ltoken)
# Useful if multiple white space tokens appear, but this should only happen
# if a macro expands to white space, perhaps that should signal a problem
#             indpc = 0
#             while (t == WHITE)
#                indpc = indpc + ltoken
#                t = gtok(token,ltoken)
#             endwhile
          else
             if (indflg < 0) then
                indpc = indpc + indlev
                indflg = 0
             else if (indflg > 0)
                indpc = indflg
                indflg = 0
             else
                indpc = 0
             endif
          endif
      
# look for a label
          if ( t == DIGIT) then
             if (optpretty == YES) then
                call putchr(blanks,5-ltoken)
             else
                call outtab(0,0)
                indpc = indpc + ltoken
             endif
             call putchr(token,ltoken)
             if (dotype(level) == OLD) then
                if (labn(level) == toktoi(token,ltoken)) then
                   idoflg = YES
                endif
             endif
             t = gtok(token,ltoken)
             if (t == WHITE) then
                indpc = indpc + ltoken
                t = gtok(token,ltoken)
             endif
             call outtab(0,0)
          endif
      
# skip over any leading white space that may be inserted by macros.
# Another possible solution would be to remove leading and trailing white space
# from elseif bodies similar to the way it is remove from defines.
          while (t == WHITE)
             t = gtok(token,ltoken)
          endwhile
      
 1000     continue
          if ( t == ESCAPE) then
             select (token(2))
                case SBLOCK:
                   call doblock
                case SDO:
                   call sdo
                case SENDDO:
                   call sedo
                case SNEXT:
                   call snext
                case SBREAK:
                   call sbrks
                case SUNTIL:
                   call suntil
                case SWHILE:
                   call swhile
                case SENDWHILE:
                   call sewhile
                case SIF:
                   call sif
                case SELSEIF:
                   call selif
                case SELSE:
                   call selse
                case SENDIF:
                   call sendif

# MSUBROUTINE, MPROGRAM, MFUNCTION
# domod might need to be called by eatup to handle 'type function blahblah..'
# so domod does not do the eatup since it might get called by eatup
                case MSUBROUTINE, MPROGRAM, MFUNCTION:
                   call outtab(0,0)
                   kesc = token(2)
                   call domod(kesc)
                   call eatup(0)
                   call prolog
                case MEND:
                   call doend
                case MRETURN:
                   call doret(.false.)
                case SINCLUDE:
                   call doinc

# for -- discard marker character (used just to detect 'end for')
# rest of for accomplished with what was pushed back from arguments
                case SFOR:
                   t = gnbtok(token,ltoken)
                   go to 1000
                case SEFOR:
                   call sefor
                case SSELECT:
                   call sselect
                case SCASE, SDEFAULT:
                   kesc = token(2)
                   call scase(kesc)
                case SESELECT:
                   call seselect
                case MINTERFACE:
                   call doiface

# then (N. B. this only occurs if 'then' is illegally placed)
                case STHEN:
                   call warn("'then' is illegally placed in code")
                case SDO90:
                   call sdo90
                case SNEXT90:
                   call snext90
                case SBREAK90:
                   call sbrks90
                case SUNTIL90:
                   call suntil90
                case SWHILE90:
                   call swhile90
                case SENDWHILE90:
                   call sewhile90
                case SSELECT90:
                   call sselect90
                case SCASE90, SDEFAULT90:
                   kesc = token(2)
                   call scase90(kesc)
                case SESELECT90:
                   call seselect90

                case SDOI:
                   call sdop
                case SSELECTI:
                   call sselectp
                case SCASEI:
                   call scasep

                case OMPTYPE:
                   call doompdir
                case MALLOCATE:
                   call doalloc("Allocate")
                case MDEALLOCATE:
                   call doalloc("Deallocate")
                case MSHAPE:
                   call doshape
             endselect
          elseif (t == COL1C) then
             if (bckeep) then
                token(1) = cichar
                k = zpakchrz(msg, len(msg), token, ltoken - 1)
                call wrline(stdout, msg, k)
             endif
          elseif ( t== NEWLINE) then
             if (bckeep) then
                call outlin
             endif
          elseif ( t.eq. LINEFEED) then
             if (optpretty == NO) then
                call outfil(indpc)
             endif
          elseif ( t.eq. COMMENT) then
             if (bckeep) then
                call endcomment(CBEFORE, 0, token, ltoken, 0)
             endif
          else
             call outtab(0,0)    #get past label field
             call putchr(token,ltoken)
             call eatup(0)
          endif
      endfor loop on statements in this file

      if (level <> 0)
         call warn('do-block level not 0 at end of file.')

      if (iflevel <> 0)
         call warn('if-block level not 0 at end of file.')

      if (sellev <> 0)
         call warn('select statement level not 0 at end of file.')

      if ( modname(0) <> '?')
         call warn('Probably a missing end statement.')
      
# note, the file got closed by getlin
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine doif (argstk,i,j)
      integer argstk(1),i,j
      integer a1,a2,a3,a4,a5,i0,e1,e2,k,p,q
      save a1,a2,a3,a4,a5,i0,e1,e2,k,p,q
      logical match
      save match
include_cmacro
include_ctype
      i0 = i + 2
      if (i0 + 2 <= j) then
         a1 = argstk(i0+0)
         a2 = argstk(i0+1)
         a3 = argstk(i0+2)
         a4 = argstk(i0+3)
         e1 = a2 - 1
         e2 = a3 - 1
         while((a1 < a2) & (type(evalst(a1)) = WHITE))
            a1 = a1 + 1
         endwhile
         while((e1 >= a1) & (type(evalst(e1)) = WHITE))
            e1 = e1 - 1
         endwhile
         
         while((a2 < a3) & (type(evalst(a2)) = WHITE))
            a2 = a2 + 1
         endwhile
         while((e2 >= a2) & (type(evalst(e2)) = WHITE))
            e2 = e2 - 1
         endwhile
# At this point, a1 is the index of the first non-blank character of the
# first arg, e1 is the index of the last non-blank character of the first
# argument.  (Hence, if the argument is one character long, a1=e1.)  If
# the argument is null, (0 or more blank characters) then e1 = a1-1.
# Thus the length of the argument is always e1-a1+1, where null arguments
# have length = 0 by definition.  Similar statements apply for a2, e2.
         
# Argument 2 may be composed of several subexpressions, some of which
# may be null: "abc|xyz|" has 3 subexpressions, the last of which is null.
# Leading and trailing blanks are not significant, but embedded space is.
# p and q are used to point at the beginning and end of each subexpression
# in succession.  If a subexpression is null, then q = p-1.
         
         match = .false.
         do
            p = a2
            q = min(p,e2)
            while((q<e2) & (type(evalst(q)) <> VBAR))
               q = q + 1
            endwhile
            if ((q>=p) & (type(evalst(q)) = VBAR))then
               a2 = q + 1 # Move a2 to the beginning of the next subexpression
               q = q - 1
               while((q>=p) & (type(evalst(q)) = WHITE))
                  q = q - 1
               endwhile
               while((a2<=e2) & (type(evalst(a2)) = WHITE))
                  a2 = a2 + 1
               endwhile
            endif
            if (e1-a1 = q-p) then
               match = .true.
               do k = 0,e1-a1
                  if (evalst(a1+k) <> evalst(p+k)) match = .false.
               enddo
               if (match) break
            endif
            if (q = e2) break
         enddo
         
         if (match)then # Push back arg3
            call pbstr(evalst(a3),a4-a3)
         else # Push back arg4, if it's there
            if ( i0 + 3 <=j) then
               a5 = argstk(i0+4)
               call pbstr(evalst(a4),a5-a4)
            endif
         endif
      endif
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine doifdf(argstk,i,j)
      integer lookup
      external lookup
      integer a1,a2,a3,a4,e1,argstk(1),i,j, i0
include_ctype
include_cmacro
      i0=i+2
      if ( i0 + 1 >j)
         return
      a1= argstk(i0)
      a2= argstk(i0+1)
      a3= argstk(i0+2)
      while ((a1 < a2) & (type(evalst(a1)) = WHITE))
         a1 = a1 + 1
      endwhile
      e1 = a2-1
      while ((e1 > a1) & (type(evalst(e1)) = WHITE))
         e1 = e1 - 1
      endwhile
      e1 = e1 + 1
      if (lookup(e1-a1,evalst(a1))>= 0 ) then 
# arg1 IS defined
         call pbstr(evalst(a2),a3-a2)
      else
         if (i0+2 <=j) then          # it isn't
            a4 = argstk(i0+3)
            call pbstr(evalst(a3),a4-a3)
         endif
      endif
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine doimed(argstk,i,j)
# if argument exists, blast it out immediately to output file
      integer a1,a2,argstk(1),i,j,larg,iarg
      character*(MPPL_MAXCARD) msg
include_cmacro
include_ctype
include_cfile
include_stdunits
      integer zpakchrz, idummy
      external zpakchrz
      do iarg = i + 2, j
         a1 = argstk(iarg)
         a2 = argstk(iarg+1)
         larg = min(a2-a1,73)
         if (larg == 0) return
         idummy = zpakchrz(msg, len(msg), evalst(a1),larg)
         call wrline(stdout,msg,larg)
      enddo
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# if argument exists, blast it out as a comment to output file
      subroutine doremk(argstk,i,j)
      integer a1,a2,argstk(1),i,j,larg,iarg
      character*(MPPL_MAXCARD) msg
include_cmacro
include_ctype
include_cfile
include_stdunits
      integer zpakchrz, idummy
      external zpakchrz
      msg(1:1) = cchar
      do iarg = i + 2, j
         a1 = argstk(iarg)
         a2 = argstk(iarg+1)
         larg = min(a2-a1,73)
         if (larg == 0) return
         idummy = zpakchrz(msg(2:), len(msg), evalst(a1),larg)
         call wrline(stdout,msg,larg+1)
      enddo
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine doinc
# include file named in next token
      integer gtok, gnbtok, lnb
      external gtok, gnbtok, lnb
include_idircom
include_cfile
include_cstat
include_ctlvars
include_stdunits
      Filename fil
      character*Evaluate(2*FILENAMESIZE) ifil, tmpfil # Twice as long as a Filename.
      character*Evaluate(2*FILENAMESIZE) inccom
      integer t, i, j, ierr, iind, n, wswid
#
      fil = ' '
      n = len(fil)
      j = 0
      t=gnbtok(token,ltoken)
# check for quoted string
      if (t == QUOTE) then
         call outtab(0,0)
         call putqs('include ')
         call putchr(token,ltoken)
         call eatup(0)
         return
      endif
      
# save all tokens up to the newline
      wswid = 0
      do
         if (t == NEWLINE) then
            break
         else if (t == COMMENT) then
            call putchr(token,ltoken)
            call outlin
            break
         else if (t == WHITE) then
            wswid = ltoken
         else
            if (j + ltoken  > n) call oops('Filename too long in include')
            do i=1,ltoken
               fil(j+i:j+i) = char(token(i))
            enddo
            j = j + ltoken
         endif
         t=gtok(token,ltoken)
      enddo
         
# save current contents of pbbuf
      if (pbbuf(1) == COMMENT) then
         cbsav(inlev) = cbuf(1:lcbuf)
         lcsav(inlev) = lcbuf
      endif

      pblinl(inlev) = bp
      do i=1,bp
         pblins(i,inlev) = pbbuf(i)
      enddo

# arrange for input to come from the new file
      bp = 0
      if (inlev == MPPL_MAXINLEV) call oops('Includes nested too deeply')
      inlev = inlev + 1
      filnam(inlev) = fil
      yyline(inlev) = 0
      tmpfil = fil
      call filopn(iusin(inlev),ierr,lnb(tmpfil),tmpfil)
      if (ierr <> 0) then
         for (j = 1, j <= inclnum, j = j + 1)
             ifil = incldirs(j)
             iind = index(ifil," ") - 1
             if (ifil(iind:iind) <> dirsep) then
                iind = iind + 1
                ifil(iind:iind) = dirsep
             endif
             ifil = ifil(:iind) // filnam(inlev)
             tmpfil = ifil
             call filopn(iusin(inlev),ierr,lnb(tmpfil),tmpfil)
             if (ierr == 0) then
                inccom = cchar // '%%%%%-included-file:' // ifil(1:lnb(ifil))
                call wrline( stdout, inccom, index(inccom,' ')  )
                return
             endif
         endfor
         inlev = inlev - 1
         call oops('Could not open include file '//fil)
      endif

      inccom = cchar // '%%%%%-included-file:' // fil
      call wrline( stdout, inccom, index(inccom,' ')  )

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# Set the macro supression character.
# This will prevent the macro from being expanded if it is followed by a 
# specific character.
# This is useful to prevent 'real*8' from being expanded to 'doubleprecision*8'

      subroutine dosetsup(argstk,i,j)

      integer a1,a2,a3,e1,argstk(1),i,j, i0, addr
      integer lookup
      external lookup
include_ctype
include_cmacro
      i0=i+2
      if ( i0 + 1 >j)
         return
      a1= argstk(i0)
      a2= argstk(i0+1)
      a3= argstk(i0+2)
      while ((a1 < a2) & (type(evalst(a1)) = WHITE))
         a1 = a1 + 1
      endwhile
      e1 = a2-1
      while ((e1 > a1) & (type(evalst(e1)) = WHITE))
         e1 = e1 - 1
      endwhile
      e1 = e1 + 1
      addr = lookup(e1-a1,evalst(a1))
      if (addr >= 0 ) then 
# arg1 IS defined
         call setsup(addr, evalst(a2))
#       a3 - a2 should be 1
      endif

      return
      end

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# DOMOD - handles program,subroutine,function

      subroutine domod(td)
      integer td,gnbtok
      external gnbtok
      integer t

include_cfile
include_cstat
      
      if (ifacelev == 0) then
         if (modname(0) <> '?') then
            call warn('Nested subroutine, function or program.')
            return
         endif
         if (td == MFUNCTION) then
            modfun = YES
         else
            modfun = NO
         endif
      endif
      
      t = gnbtok(token,ltoken)
      if (t <> ALPHA) then
         call warn('subroutine,function, or program statement error.')
         return
      endif
      if (ltoken > 32) then
         call warn('Module name too long.')
         return
      endif
      call setmod(token,ltoken)
      modtype(ifacelev) = td
      
      if (td == MPROGRAM) then
         call putqs('program ')
      elseif (td == MSUBROUTINE) then
         call putqs('subroutine ')
      else
         call putqs('function ')
      endif
      call putchr(token,ltoken)
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine doiface
include_cstat
      call outtab(0,0)
      call putqs('interface ')
      ifacelev = ifacelev + 1
      
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine sendiface
include_cstat
      ifacelev = ifacelev - 1
      call outtab(0,0)
      call putqs('end interface')
      return
      end
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#
# ifstmt : logical .true. if the return is after an if statement.
#         In this case we must indent and add the trailing endif
# indent : indent column for if block.
#
      subroutine doret(ifstmt)
include_cstat
      logical ifstmt
      integer t, iblock
      integer gnbtokw,gtok,lnb
      external gnbtokw,gtok,lnb
      integer nlev, wswid
      
      t = gnbtokw(token,ltoken,wswid)
      if ( t == LPAREN) then    !return for function value
         if (modfun .eq. NO) then
            call warn('Attempt to return value from subroutine.')
            return
         endif
         if (ifstmt) then
            call putqs('then')
            call outlin
            iblock = 1
         else
            iblock = 0
         endif
         call outtab(0,iblock)
         call putqs(modname(0)(1:lnb(modname(0))))
         call putqs(' = ')
         nlev = 1
         do
            t = gnbtokw(token,ltoken,wswid)
            if (t == LPAREN) then
               nlev = nlev + 1
            elseif (t == RPAREN) then
               nlev = nlev - 1
               if (nlev .eq. 0) break
            elseif ( t == NEWLINE) then
               call warn('Missing right parenthesis.')
               return
            endif
            if (wswid > 0) call outfil(wswid)
            call putchr(token,ltoken)
         enddo
         call eatup(0)
         call outtab(0,iblock)
         call putqs('return')
         call outlin
         if (ifstmt) then
            iflevel = iflevel - 1
            call outtab(0,0)
            call putqs('endif')
            call outlin
            iflevel = iflevel + 1
         endif
      else                      !regular return statement
         call outtab(0,0)
         call putqs('return') # XXX - extra space for test suite
         if (t == COMMENT) then
            call endcomment(CBEFORE, 0, token, ltoken, 0)
         else if (t == NEWLINE) then
            call outlin
         else
            call putchr(token,ltoken)
            call eatup(0)
         endif
      endif
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------

# DOOMPDIR - handle the exceptions for an OMP directive

      subroutine doompdir

include_cstat
include_cfile
include_ctype

      integer gtok
      external gtok
      integer i, t, kesc, iblank, iprev, i23008

      call putqs(cchar)
      call putqs('$omp')
      do 
         t = gtok(token,ltoken)
         
         if (t == LINEFEED) then  # --nopretty
            call conlin
            indpc = 0
         else if (t == NEWLINE) then
# We've found the end of this directive, must look ahead for another.
# If we find it, and column 6 is non-white, then it is a continuation
# of this directive.
# We only allow blank lines between continued directives
            iblank = 0
            iprev = 0
            do
               t = gtok(token,ltoken)
               if (t <> NEWLINE & t <> LINEFEED) break
               iblank = iblank + 1
               iprev = t
            enddo
            if (t == ESCAPE & token(2) == OMPTYPE) then
               if (iprev == LINEFEED) then
                  if (optlang == LANG_F90 | optlang == LANG_IS_F90) then
                     call putqs(' &')
                  endif
                  call outlin
# Put out all the blank lines we found
                  do i=1,iblank
                     call outlin
                  enddo
                  call putqs(cchar)
                  call putqs('$omp')
                  next
               endif
            endif
            call outlin
# Put out all the blank lines we found
            do i=1,iblank
               call outlin
            enddo
            call pbstr(token,ltoken)
            break
         else if (t<> ESCAPE) then
            call putchr(token,ltoken)
         else
            kesc = token(2)
            select(kesc)
               case MEND:
                  call putqs('end')   

               case SDO, SDO90, SDOI:
                    call putqs('do')

               case SIF:
                    call putqs('if')

               case SFOR:
                    call putqs('for')

               case SDEFAULT, SDEFAULT90:
                    call putqs('default(')
                    t = gtok(token,ltoken)
                    call putchr(token,ltoken)
                    call putqs(')')

               case OMPTYPE:
# This is trigger by a continued omp directive
                   if (nonblk == YES) call conlin
# Reset lastpc since an omp directive starts at the begining of the line
                   lastpc = 0
                   call putqs(cchar)
                   call putqs('$omp')

               default:
                    call warn('Unexpected keyword in directive')
            endselect
         endif
      enddo
      return
      end

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#
# Process a f90 allocate statement of the form:
# allocation ::=  ALLOCATE ( allocate-shape-spec-list )
# allocate-shape-spec ::=  [ lower-bound : ] upper-bound
# Genrate a call to macro Allocate with arguments of
# lower-bound and upper-bound, where lower-bound is explicitly set to 1 if not
# present in the ALLOCATE.
#
# allocate(foo(10))  =>   name(foo,(10))
#
      subroutine doalloc(name)

include_cstat
      character*(*) name

      integer gnbtok
      external gnbtok
      integer t, iparen

      integer i, j, founde
      integer abuf(BUFSIZE), iabuf
      integer index(3,10), iindex
#    1 = start of name
#    2 = start of dimension
#    3 = end of dimension

      iparen = 0
      iabuf = 1
      iindex = 1
      founde = 0
      do
         t = gnbtok(token,ltoken)
         if (t == LPAREN) then
            iparen = iparen + 1
            abuf(iabuf) = LPAREN
            if (iparen == 1) then   # start of name
               index(1,iindex) = iabuf + 1
               index(2,iindex) = 0
               index(3,iindex) = 0
            else if (iparen == 2) then  # start of shape
               index(2,iindex) = iabuf
            endif
            iabuf = iabuf + 1
         else if (t == RPAREN) then
            abuf(iabuf) = RPAREN
            if (iparen == 1) then
               if (index(2,iindex) == 0) then  # no shape found
                  index(2,iindex) = iabuf
               endif
               if (founde <> 0) then
                  index(2,iindex) = iabuf - 1
               endif
            else if (iparen == 2) then
               index(3,iindex) = iabuf
            endif
            iabuf = iabuf + 1
            iparen = iparen - 1
            if (iparen == 0) break
         else if (t == COMMA) then
            abuf(iabuf) = COMMA
            iabuf = iabuf + 1
            if (iparen == 1) then
               if (index(2,iindex) == 0) then  # no shape found
                  index(2,iindex) = iabuf - 1
               endif
               iindex = iindex + 1
               index(1,iindex) = iabuf
               index(2,iindex) = 0
               index(3,iindex) = 0
            endif
         else if (t == EQUALS) then
            founde = iindex
            abuf(iabuf) = EQUALS
            iabuf = iabuf + 1
         else
            do i=1,ltoken
               abuf(iabuf) = token(i)
               iabuf = iabuf + 1
            enddo
         endif
      enddo

      if (founde > 0) iindex = iindex - 1

      do j = iindex, 1, -1
         call putbak(NEWLINE)
         call putbak(RPAREN)
         do i = index(3,j), index(2,j), -1
            call putbak(abuf(i))
         enddo
         if (index(3,j) <> 0) call putbak(COMMA) # no shape
         do i = index(2,j)-1, index(1,j), -1
            call putbak(abuf(i))
         enddo

         call cpbstr('(')
         call cpbstr(name)
#         call cpbstr('      Allocate(')
      enddo

      end

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#
# Process a f90 array shape
#
# (10)     =>   1,10
# (2:10)   =>   2,10
# (20,30)  => 1,20,1,30
#
      subroutine doshape()

include_cstat

      integer gnbtok
      external gnbtok
      integer t, iparen, istart

      integer abuf(BUFSIZE), iabuf, i

      iparen = 0
      iabuf = 1
      istart = 0
      do
         t = gnbtok(token,ltoken)
         if (t == LPAREN) then
            iparen = iparen + 1
            if (iparen == 2) then
               # assume lower limit is 1
               abuf(iabuf) = 49   ! '1'
               abuf(iabuf+1) = COMMA 
               iabuf = iabuf + 2
               istart = iabuf
            else if (iparen > 2) then
               abuf(iabuf) = LPAREN
               iabuf = iabuf + 1
            endif
         else if (t == RPAREN) then
            if (iparen > 2) then
               abuf(iabuf) = RPAREN
               iabuf = iabuf + 1
            endif
            iparen = iparen - 1
            if (iparen == 0) break
         else if (t == COMMA) then
            if (iparen == 2) then
               abuf(iabuf) = COMMA
               abuf(iabuf+1) = 49   ! '1'
               abuf(iabuf+2) = COMMA 
               iabuf = iabuf + 3
               istart = iabuf
            endif
         else if (t == COLON) then
            if (iparen == 2) then
               # get rid of the assumed lower limit of 1
               do i = istart, iabuf
                  abuf(i-2) = abuf(i)
               enddo
               iabuf = iabuf - 2
               abuf(iabuf) = COMMA
               iabuf = iabuf + 1
            endif
         else
            do i=1,ltoken
               abuf(iabuf) = token(i)
               iabuf = iabuf + 1
            enddo
         endif
      enddo

#      call putbak(NEWLINE)
#      do i = iabuf, 1, -1
#         call putbak(abuf(i))
#      enddo
#      call cpbstr('      Allocate')
      call putchr(abuf,iabuf-1)

      end

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine eatup(lcode)

include_cstat
include_cfile
include_ctype

      integer lcode
      integer wswid, icont
      integer gtok,gnbtokw
      external gtok,gnbtokw
      integer t, needlog, kesc, lcode0
      
      needlog = 0
      wswid = 0
      t = 0
      lcode0 = lcode
      do
         if (t == 0) t = gtok(token,ltoken)
         icont = lnbt
         
         if (t == LINEFEED) then  # --nopretty
            call conlin
            indpc = 0
            t = gtok(token,ltoken)
         elseif (t == COMMENT) then
            if (icont == NO & lcode0 > 0) then
               call putchr(code,lcode)
               lcode0 = 0
            endif
            call endcomment(CBEFORE, icont, token, ltoken, wswid)
            if (icont == 1) then
               call outtab(0,0)
               t = 0
               next
            else
               break
            endif
         else if (t == NEWLINE) then
            if (lcode0 > 0) then
               call putchr(code,lcode)
            endif
            call outlin
            break
         else if (t == SEMICOLON) then
            if (lcode0 > 0) 
               call putchr(code,lcode)
# Read ahead to get token length, then put back
            t = gnbtokw(token,ltoken,wswid)
            call pbstr(token,ltoken)
# If the white space and token fit on this line, put semicolon and white space
            if (lastpc + wswid + ltoken + 1 <= col72) then
               call putqs(';')
               call outfil(wswid)
               break
            else
# otherwise, treat as an end of statement
               t = EOS
            endif
         else if (wswid <> 0) then
            call outfil(wswid)
            wswid = 0
         endif
         
         if (t == WHITE) then
# trim trailing whitespace
            wswid = ltoken
         elseif (t == EOS) then
            call outlin
# preserve indention level
            indflg = indpc
            break
         else if (t<> ESCAPE) then
            call putchr(token,ltoken)
         else
            kesc = token(2)
            if (kesc == MFUNCTION | kesc == MSUBROUTINE) then
# function can follow a type
               call domod(kesc)      
               needlog = 1
            elseif ( kesc == MEND ) then
# for end=label in open statements
               call putqs('end')
            elseif (kesc == MSHAPE) then
               call doshape
            else
               call warn('Misused keyword (?)')
            endif
         endif
         t = 0
      enddo
      if ( needlog <> 0) call prolog
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine eval(argstk,i,j)
#eval --expand args i through j; evaluate builtin or push back defn
      integer argstk(ARGSIZE),i,j,k,m,n,t,td, ano, ml
      integer lbl(5),lenlbl,nl,nat,natl
      integer labgen, i23000
      integer k2
      external labgen
include_cmacro

      t = argstk(i)
      if (argstk(i+1) == t ) then
         td = NULL
      else
         td = evalst(t)
      endif

      if ( td == ESCAPE) then
         select(evalst(t+1))
            case DEFTYPE:           call dodef(argstk,i,j)
            case IFDEFTYPE:         call doifdf(argstk,i,j)
            case IFELSETYPE:        call doif (argstk,i,j)
            case ERRPRINTTYPE:      call doerrp(argstk,i,j)
            case INFOPRINTTYPE:     call doinfop(argstk,i,j)
            case DUMPDEFTYPE:       call dodmp(argstk,i,j)
            case EVALUATETYPE:      call domath(argstk,i,j)
            case IMMEDIATETYPE:     call doimed(argstk,i,j)
            case REMARKTYPE:        call doremk(argstk,i,j)
            case UNDEFINETYPE:      call doundf(argstk,i,j)
            case SMODTYPE:          call domodn
            case SSETSUP:           call dosetsup(argstk,i,j)
            default: go to 10
         endselect
         return
      endif

 10   continue
# do replacement on text
# first scan for how many @n's needed
      nat = 0
      do k=t,argstk(i+1)-2
         if (evalst(k) == ATSIGN) then
            n = evalst(k+1) - ZERO
            if (n < 1 | n > 9) then
               call oops('Bad at sign argument in macro definition.')
            endif
            nat = max(nat,n)
         endif
      enddo

      if (nat > 0) natl = labgen(nat)

# now scan text backwards looking for $n, @n
      for (k = argstk(i+1) - 1, k>t , k = k-1)
          if (evalst(k-1) <> ATSIGN & evalst(k-1) <> DOLLAR) then
             call putbak(evalst(k))
             next
          endif
          
# now decide if in COL1C area; if so, no expansion
          do k2 = k-1, t, -1
             if (evalst(k2) == COL1C) then
                call putbak(evalst(k))
                next 2
             endif
             if (evalst(k2) == NEWLINE) then
                break
             endif
          enddo
          
          if (evalst(k-1) == ATSIGN) then
             n = evalst(k) - ZERO
             nl = natl + n - 1
             call itotok(nl,lbl,lenlbl)
             call pbstr(lbl,lenlbl)
             k = k - 1
          else # $n or $* or $- or $$ or $(other)
             if (evalst(k) == ASTERISK) then
                for (ano=j-i-1,ano>0,ano=ano-1)
                    n = i + ano + 1
                    m = argstk(n)
                    ml = argstk(n+1)-argstk(n)
                    call pbstr(evalst(m),ml)
                    if (ano>1) call pbstr(COMMA,1)
                endfor
             elseif (evalst(k) == MINUS) then
                for (ano=j-i-1,ano>1,ano=ano-1)
                    n = i + ano + 1
                    m = argstk(n)
                    ml = argstk(n+1)-argstk(n)
                    call pbstr(evalst(m),ml)
                    if (ano>2) call pbstr(COMMA,1)
                endfor
             elseif (evalst(k) == DOLLAR) then
                continue
             else #look for digit
                ano = evalst(k) - ZERO
                if (ano >=0 & ano <=9) then
                   if ( ano < j-i) then
                      n = i + ano + 1
                      m = argstk(n)
                      ml = argstk(n+1)-
                      argstk(n)
                      call pbstr(
                      evalst(m),ml)
                   endif
                else  # other, leave it alone 
                   call putbak(evalst(k))
                endif
             endif
             k = k - 1 #skip over $
          endif
      endfor loop on replacement text

      if (k == t) #do last character
         call putbak(evalst(k))

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# GETLEV - find integer after break,next statements if any

      subroutine getlev(nlev,argstk,i,j)

      integer nlev,toktoi
      integer i,j,argstk(1)
      integer a1,a2

include_cstat
include_cmacro
      
      if ( j > i + 2)
         call warn('Too many arguments to break or next')

      a1 = argstk(i+2)
      a2 = argstk(i+3)

      if (a2 > a1) then  #there is an argument
         nlev = toktoi(evalst(a1),a2-a1) - 1
      else
         nlev = 0
      endif

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
c ISOMPDIR - return 1 if contents of cbuf is an OMP directive
c          - return 0 otherwise
      
      integer function isompdir(s)
      character*(*) s
      
      if (s(2:5) .eq. '$omp') then
         isompdir = 1
      else
         isompdir = 0
      endif
      
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# GETLIN - read the next line
#        - send comments out immediately
      
      subroutine getlin

include_cfile
include_ctype
include_icom
include_ctlvars

      integer i,c1,nextline,ompdir
      
      integer lnb, isompdir
      external lnb, isompdir
      
      ompdir = NO
      lcbuf = nextline(optnum)
      yyline(inlev) = yyline(inlev) + 1
      if ( lcbuf < 0)  #####END OF FILE
         go to 2000
      if ( lcbuf == 0) go to 200
      c1 = ichar(cbuf(1:1))
      if ( c1 == PERIOD)   #alternate method for end-of-file
         go to 2000
      
# is this a comment?
      if (col1(c1) | type(c1) == COMMENT) then
         pbbuf(1) = COMMENT
         bp = 1
         cbuf(1:1) = cchar
         if (isompdir(cbuf) .eq. 0) then
            return
         else
            ompdir = YES
         endif
      endif
 200  continue
      bp = lcbuf + 1
      pbbuf(1) = NEWLINE
      
# line goes backward into pbbuf
      do i=1,lcbuf
         pbbuf(bp + 1 - i) = ichar(cbuf(i:i))
      enddo
      
# is this a continued line ?
      if (ompdir == YES) then
# delete the '$omp" part.
         bp = bp - 4
# Replace the comment character with escape sequence
         pbbuf(bp)     = OMPTYPE
         pbbuf(bp + 1) = ESCAPE
         bp = bp + 1
# Look for continued omp directive
         if (bp >= 3 & col6 & type(pbbuf(bp-2)) <> WHITE) then
# replace continuation character with space and add NULL marker
            if (optlang == LANG_F90) pbbuf(bp-2) = BLANK
# use LINEFEED as a continuation marker
# chkcont will replace the NULL with LINEFEED if hnl == YES
            if (hnl == NO) then
               bp = bp + 1
               pbbuf(bp) = LINEFEED
            endif
            bp = bp + 1
            pbbuf(bp) = NULL
         endif
      else if (bp >= 7 & col6 ) then
         if (cbuf(1:5) == '     ' & type(pbbuf(bp-5)) <> WHITE) then
            if (optlang == LANG_F77) then
# delete the unwanted part
               bp = bp - 5
               pbbuf(bp) = NULL
            else if (optlang == LANG_F90) then
# replace continuation character with space and add NULL marker
               pbbuf(bp-5) = BLANK
               bp = bp + 1
               pbbuf(bp) = NULL
            endif
         endif
      else if (optlang == LANG_IS_F90) then
         do i=bp,1,-1
            if (pbbuf(i) == AMPERSAND) then
               bp = i - 1
               break
            else if (type(pbbuf(i)) <> WHITE ) then
               break
            endif
         enddo
      endif
      return
      
# end-of-file
 2000 continue
      call filcls(iusin(inlev))
      inlev = inlev - 1
      if (inlev > 0) then #back to previous file
         call popyin(iusin(inlev),lnb(filnam(inlev)),filnam(inlev))
         bp = pblinl(inlev)
         do i=1,bp
            pbbuf(i) = pblins(i,inlev)
         enddo
         if (pbbuf(1) == COMMENT) then
            cbuf = cbsav(inlev)
            lcbuf = lcsav(inlev)
         endif
      else
         bp = 1
         pbbuf(bp) = EOF
      endif
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# GETTOK - return next token, length of which is toksiz
#        - on NEWLINE, check for following NULL which means line is
#        - continued
#        - check if last non-white token indicates continuation
#        - Splitting one token across two lines works with f77, but not
#        - f90 free form.  Thus logical operators, real numbers, and
#        - muticharacter operators (//)
#        - must be recognized as one token.
      
      function gettok(token,toksiz)
      integer gettok
      integer toksiz
      integer token(*)
      integer i,j,n,iamp
      integer i23002
      integer toktoi, zpakchrz
      character*(MPPL_MAXCARD) msg
      external toktoi, zpakchrz

include_ctype
include_cfile
include_cmacro
include_stdunits

      character qte
      
      integer isompdir
      external isompdir
      
# look at next character first
# gettok is the only routine allowed to take anything OUT of pbbuf
      do
         if (bp .eq. 0) call getlin

         token(1) = pbbuf(bp)
         gettok = type(token(1))
         if (gettok == EOF) break

         bp = bp - 1
         toksiz = 1

# pbbuf has only a NEWLINE, EOF, or COMMENT in position 1
# in the case of COMMENT, the text is still in cbuf
# a newline might not count if the following character is NULL
# ALPHAS, DIGITS can not be broken over continued lines
         select (gettok)

# NEWLINE
            case NEWLINE:

# check ahead for possible continuation
                 if (bp == 0) then
                    call getlin
                    call chkcont
                    if (lnbt == YES) next
                    lnbt = NO
                 endif
                 break
                 
# LETTER
            case LETTER:
                 do i=bp,1,-1
                    if (alphan(pbbuf(i)) == NO) break
                 enddo
                 do j=bp,i+1,-1
                    token(2+bp-j) = pbbuf(j)
                 enddo
                 toksiz = 1 + bp - i
                 bp = i
                 gettok = ALPHA
                 lnbt = NO
                 break

# QUOTE
            case QUOTE:
                 i = bp
                 if (optlang == LANG_IS_F90) then
                    i = bp
                    iamp = 0  # location of ampersand
                    do
                       if (pbbuf(i) == NEWLINE) then
                          if (iamp == 0) then
                             call inform('Missing continuation in string')
                             lnbt = NO
                             call putbak(NEWLINE)
                             break
                          endif
                          do j=bp,iamp,-1
                             token(toksiz+bp+1-j) = pbbuf(j)
                          enddo
                          toksiz = toksiz + 1 + bp - iamp
                          call getlin
                          i = bp
# skip past first amperand (if present)
                          do
                             if (type(pbbuf(i)) <> WHITE ) break
                             i = i - 1
                          enddo
                          if (pbbuf(i) == AMPERSAND) then
                             i = i - 1
                             bp = i
                          else
                             i = bp
                          endif
                       else if (pbbuf(i) == AMPERSAND) then
                          iamp = i + 1
                          i = i - 1
                       else if (pbbuf(i) == token(1)) then
                          if (pbbuf(i-1) <> token(1)) break
                          i = i - 1
                       else
                          i = i - 1
                       endif
                    enddo
                 else
 500                continue
                    if (i == 1) then   # at end of line, check for continuation
                       do j=bp,2,-1
                          token(toksiz+bp+1-j) = pbbuf(j)
                       enddo
                       toksiz = toksiz + bp - 1
                       call getlin
                       if (pbbuf(bp) == NULL) then
                          bp = bp -1
                          i  = bp
                          go to 500
                       endif
                       qte=char(token(1))
                       call inform('Missing quote ('//qte//')')
                       lnbt = NO
                       call putbak(NEWLINE)
                       break
                    endif

                    if (pbbuf(i) == token(1)) then
# probably the end but watch out for doubled quote
                       if (pbbuf(i-1) <> token(1)) go to 501
                       i = i - 1
                    endif
                    i = i - 1
                    go to 500
 501                continue
                 endif
                 do j=bp,i,-1
                    token(toksiz+bp+1-j) = pbbuf(j)
                 enddo
                 toksiz = toksiz + 1 + bp - i
                 bp = i - 1
                 lnbt = NO
                 break

# WHITE
            case WHITE:
                 do i=bp,1,-1
                    if (type(pbbuf(i)) <> WHITE ) break
                 enddo
                 do j=bp,i+1,-1
                    token(2+bp-j) = pbbuf(j)
                 enddo
# If --pretty, only return size 1 tokens
                 toksiz = min(1 + bp-i, maxws)
                 bp = i
# avoid setting lnbt on white
                 break

# DIGIT
            case DIGIT:
                 do i=bp,1,-1
                    if (type(pbbuf(i)) <> DIGIT) break
                 enddo

                 do j=bp,i+1,-1
                    token(2+bp-j) = pbbuf(j)
                 enddo

                 toksiz = 1 + bp-i
                 bp = i

# peek ahead for Hollerith
                 if (pbbuf(bp) == 72 | pbbuf(bp) == 104) then
                    if (toksiz > 2) call oops('Hollerith count too large.')
                    n = toktoi(token,toksiz)
                    if (n >= bp - 1) call oops('Hollerith constant error.')
                    toksiz = toksiz + 1
                    token(toksiz) = pbbuf(bp)
                    do i = 1, n
                       token(toksiz+i) = pbbuf(bp - i)
                    enddo
                    toksiz = toksiz+n
                    gettok = QUOTE
                    bp = bp - (n+1)

# peek ahead for real number
                 else if (pbbuf(bp) == PERIOD) then
                    do i=bp-1,1,-1
                       if (type(pbbuf(i)) <> LETTER) break
                    enddo
                    if (i <> bp-1 & i > 1) then
                       if (pbbuf(i) <> PERIOD)
                           call parreal(token,toksiz)
                       # else this is a logical operator
                    else
                       call parreal(token,toksiz)
                    endif
# look for exponent (d,D,e,E)  [ 4e4 ]
                 else if (pbbuf(bp) == 68 | pbbuf(bp) == 100 |
                          pbbuf(bp) == 69 | pbbuf(bp) == 101) then
                     call parreal(token,toksiz)
                 endif
                 lnbt = NO
                 break
                 
# NUMBER
            case NUMBER:
                 toksiz = pbbuf(bp)
                 bp = bp - 1

                 do j=bp,bp-toksiz+1,-1
                    token(1+bp-j) = pbbuf(j)
                 enddo
                 bp = bp - toksiz

# peek ahead for Hollerith
                 if (pbbuf(bp) == 72 | pbbuf(bp) == 104) then
                    if (toksiz > 2) call oops('Hollerith count too large.')
                    n = toktoi(token,toksiz)
                    if (n >= bp - 1) call oops('Hollerith constant error.')
                    toksiz = toksiz + 1
                    token(toksiz) = pbbuf(bp)
                    do i = 1, n
                       token(toksiz+i) = pbbuf(bp - i)
                    enddo
                    toksiz = toksiz+n
                    gettok = QUOTE
                    bp = bp - (n+1)
                 endif
                 lnbt = NO
                 break
                 
# COMMENT
            case COMMENT:
                 if (bp == 0) then   # whole line a comment
                    comchar = token(1)
                    token(1) = COL1C
                    gettok = COL1C
                    toksiz = lcbuf + 1
                    do i = 2, lcbuf
                       token(i) = ichar(cbuf(i:i))
                    enddo
                    token(toksiz) = NEWLINE
                    lnbt = NO
                    if (toksiz > col72 + 1) then
                       if (isompdir(cbuf) .eq. 1) then
                          call inform("c$omp line too long.")
                          call inform(cbuf(1:lcbuf))
                       endif
                    endif
                    
                 else
                    comchar = token(1)
                    token(1) = cichar
                    do j=bp,2,-1
                       if (pbbuf(j) == NEWLINE) break
                    enddo

#                    if (bckeep & (cp==0)) then
                    if (bckeep) then
                       toksiz = 1
# Do not include the NEWLINE in the token
                       do i = bp, j+1, -1
                          toksiz = toksiz + 1
                          token(toksiz) = pbbuf(i)
                       enddo
                       
                       if (cp <> 0) then
# If in a macro, then revert to mppl comment
#                    token(1) = POUND
#                    token(toksiz+1) = NEWLINE
#                    toksiz = toksiz+1
                          toksiz = zpakchrz(msg, len(msg), token, toksiz)
                          call wrline(stdout,msg,toksiz)
                       endif
                    endif

# If in a macro, do not consume the NEWLINE else do
                    if (cp <> 0) then
                       bp = j
                    else
                       bp = j-1
                    endif

# check ahead for possible continuation
                    if (bp == 0) then
                       call getlin
                       call chkcont
                    endif
                 endif
                 
                 if (cp<>0) next  # ignore comments in macros
                 break

# PERIOD
# Look for logical operators (.or. .and.) and real numbers (.123)
            case PERIOD:
                 if (type(pbbuf(bp)) == DIGIT) then
                    call parreal(token,toksiz)
                    gettok = DIGIT
                 else
                    do i=bp,1,-1
                       if (type(pbbuf(i)) <> LETTER) break
                    enddo
                    if (i <> bp & i > 1) then
                       if (pbbuf(i) == PERIOD) then
                          do j=bp,i,-1
                             token(2+bp-j) = pbbuf(j)
                          enddo
                          toksiz = 2 + bp - i
                          bp = i - 1
                          gettok = LOGICAL
                       endif
                    endif
                 endif
                 lnbt = NO
                 break
                
# Recognize multi character operators 
# Recognize /, //, *, **
            case SLASH, ASTERISK:
                 if (bp > 1) then
                    if (pbbuf(bp) == gettok) then
                       token(2) = gettok
                       gettok = OPERATOR
                       toksiz = 2
                       bp = bp - 1
                    endif
                 endif
# can't continue on SLASH because of data statement
                 if (gettok == SLASH) then
                    lnbt = NO
                 else
                    lnbt = YES
                 endif
                 break

# BSLASH
            case BSLASH:
                 lnbt = YES
                 next

# ESCAPE
            case ESCAPE:
                 token(2) = pbbuf(bp)
                 toksiz = 2
                 bp = bp - 1
                 lnbt = NO
                 break

# COL1C
            case COL1C:
                 do j = bp, 1, -1
                    token(2 + bp - j) = pbbuf(j)
                    if (pbbuf(j) == NEWLINE) go to 11
                 enddo
                 call oops('Comment line token damaged. Internal error.')
 11              continue
                 toksiz = 2 + bp - j
                 bp = j - 1
                 lnbt = NO
                 break

# AMPERSAND
            case AMPERSAND:
                 if (optlang == LANG_IS_F90) then
                    lnbt = YES
                    # look for token after white space
                    do i=bp,1,-1
                       if (type(pbbuf(i)) <> WHITE ) break
                    enddo
                    if (pbbuf(i) == NEWLINE) bp = i
                    next
                    
                 else
                    lnbt = contu(gettok)
                    break
                 endif

# remark: otherwise is a single letter token, returns as itself
            default:
                lnbt = contu(gettok)
                break
         endselect
      enddo

# debug - print token
#      do i=1,toksiz
#         msg(i:i) = char(token(i))
#      enddo
#      print *, msg(1:toksiz)

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------

#
# Parse the remainder of a real number
# bp is pointing to the decimal point
#
      subroutine parreal(token,ltoken)

include_ctype
include_cfile

      integer token(*), ltoken

# look for period
      if (pbbuf(bp) == PERIOD) then
         ltoken = ltoken + 1
         token(ltoken) = pbbuf(bp)
         bp = bp - 1
      endif

# collect digits
      do
         if (type(pbbuf(bp)) <> DIGIT) break
         ltoken = ltoken + 1
         token(ltoken) = pbbuf(bp)
         bp = bp - 1
      enddo

# look for exponent (d,D,e,E)
      if (pbbuf(bp) == 68 | pbbuf(bp) == 100 |
          pbbuf(bp) == 69 | pbbuf(bp) == 101) then
          ltoken = ltoken + 1
          token(ltoken) = pbbuf(bp)
          bp = bp - 1

# look for + or =          
          if (pbbuf(bp) == 43 | pbbuf(bp) == 45) then
             ltoken = ltoken + 1
             token(ltoken) = pbbuf(bp)
             bp = bp - 1
          endif

# collect exponent
          do
             if (type(pbbuf(bp)) <> DIGIT) break
             ltoken = ltoken + 1
             token(ltoken) = pbbuf(bp)
             bp = bp - 1
          enddo
      endif

      end

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#
# Check for continuation
# return YES if this line is continued, else NO
#
      subroutine chkcont

include_ctype
include_cfile

      integer i

      if (pbbuf(bp) == NULL) then
# delete NULL marker
         bp = bp - 1

         if (hnl == YES) then
            if (optpretty == YES) then
# remove all leading white space since we're controlling indention
               do i=bp,1,-1
                  if (type(pbbuf(i)) <> WHITE ) break
               enddo
               bp = i
            endif
# insert linefeed
            bp = bp + 1
            pbbuf(bp) = LINEFEED
         endif
         lnbt = YES
      else if (lnbt == YES & pbbuf(bp) <> EOF) then
         if (hnl == YES) then
            if (optpretty == YES) then
# remove all leading white space since we're controlling indention
               do i=bp,1,-1
                  if (type(pbbuf(i)) <> WHITE ) break
               enddo
               bp = i
            else if (optlang == LANG_F77) then
# remove leading space similar to conventional continuation
               do i=1,6
                  if (type(pbbuf(bp)) <> WHITE ) break
                  bp = bp - 1
               enddo
            endif
# insert linefeed
            bp = bp + 1
            pbbuf(bp) = LINEFEED
         endif
      endif

      end

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      function gnbtok(token,ltoken)
      integer gnbtok,token(*),ltoken
      integer gtok
      external gtok

      gnbtok = gtok(token,ltoken)
      while(gnbtok == WHITE)
         gnbtok = gtok(token,ltoken)
      endwhile

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      function gnbtokw(token,ltoken,wswid)
      integer gnbtokw,token(*),ltoken,wswid
      integer gtok
      external gtok

      wswid = 0
      gnbtokw = gtok(token,ltoken)
      while(gnbtokw == WHITE)
         wswid = wswid + ltoken
         gnbtokw = gtok(token,ltoken)
      endwhile

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      function gtok(token,ltoken)
      integer gtok
      integer token(*),ltoken
      integer lookup,addr,supchar
      integer gettok,peek,putdef
      external lookup,gettok,peek,putdef
      integer t

include_cfile
include_cmacro
include_cargs
include_ctype
include_ctlvars

# return with next token after resolving macro definitions
      for (t=gettok(token,ltoken), t <> EOF , t=gettok(token,ltoken))

# if token is alphanumeric, see if it is a macro and expand it if
# we are not inside square brackets
          if (t == ALPHA ) then
             if (nlb > 0) go to 100  #no lookup if inside brackets
             addr = lookup(ltoken,token)
             if (addr == -1) go to 100

             call getsup(addr, supchar)
             t = peek()
             if (supchar <> 0 & t == supchar) goto 100

# token is a macro ; set up stack frame
             cp = cp + 1
             if (cp > CALLSIZE) then
                cp = CALLSIZE
                call oops('Macro error, call stack overflow.')
             endif
             mline(cp) = yyline(inlev)
             mlev(cp) = inlev
             callst(cp) = ap

# start stack frame
             call push(ep,argstk,ap)

# stack definition
             if (putdef(addr,evalst,ep,EVALSIZE) <> 0) then
                call oops('Evaluation stack overflow.')
             endif

             call push(ep,argstk,ap)

# stack name
             call putarg(token,ltoken)
             call push(ep,argstk,ap)

# add parenthesis if they are not already on the way
             if (t <> LPAREN) then  # push back parens
                call putbak(RPAREN)
                call putbak(LPAREN)
             else
                do
                   t=gettok(token,ltoken)
                   if (t == LPAREN) break
                enddo
                call putbak(LPAREN)
            endif
             plev(cp) = 0
# start collecting arguments
             next

          elseif (t==LBRACK) then
             nlb = nlb + 1
#strip one level of []
             if (nlb == 1) next

          elseif (t==RBRACK) then
             nlb = nlb - 1
             if (nlb < 0) then
                call inform('Extraneous right square bracket.')
                nlb = 0
             endif
             if (nlb == 0) next
          endif
 100      continue

          if (cp == 0)  # not in a macro, this is the token we want
             return(t)

# if inside square brackets just copy token
          if (nlb > 0) then
             call putarg(token,ltoken)

# argument collection, look for commas, but not inside parens
          elseif (t==LPAREN) then
             if (plev(cp) > 0)
             call putarg(token,ltoken)
             plev(cp) = plev(cp) + 1

          elseif (t==RPAREN) then
             plev(cp) = plev(cp) - 1
             if (plev(cp) > 0 ) then
                call putarg(token,ltoken)

             else    #end of argument list found !
# evaluate the macro and its arguments
                argstk(ap) = ep
                call eval(argstk,callst(cp),ap-1)
#pop evaluation stack
                ap = callst(cp)
                ep = argstk(ap)
                cp = cp - 1
             endif

          elseif (t == COMMA & plev(cp) == 1) then    #new arg
             call push(ep,argstk,ap)

          else
             call putarg(token,ltoken)   #just stack it
          endif
      endfor  # end of gettok call loop

# arrive here if end-of-file, check for screwed up [] or parens
      if (cp <> 0 )
         call oops(
            'Unexpected end of file in macro arguments--missing ) or ] ?')
      
      if (nlb > 0)
         call oops('Missing right square bracket, at end-of-file.')

      return(EOF)
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine init

include_idircom
include_ctype
include_cstat
include_cfile

      integer i

# default include directory separator (a slash)
      dirsep = '/'
      inclnum = 0

# type table and switch tables
      call setsen
      do i=LEXMIN,LEXMAX
         type(i) = i
         alphan(i) = NO
         contu(i) = NO
         col1(i)  = .false.
      enddo
      do i=48,57
         type(i) = DIGIT
         alphan(i) = YES
      enddo
      do i=65,90
         type(i) = LETTER
         alphan(i) = YES
      enddo
      do i=97,122
         type(i) = LETTER
         alphan(i) = YES
      enddo
      type(BLANK) = WHITE
      type(TAB) = WHITE
      type(UNDERSCORE) = LETTER
      type(TICK) = QUOTE
      type(BANG) = COMMENT
      type(POUND) = COMMENT
      type(ESCAPE) = ESCAPE
      
      alphan(UNDERSCORE) = YES
# characters which cause a line to be continued
      contu(PLUS) = YES
      contu(MINUS) = YES
      contu(ASTERISK) = YES
# can't do it on SLASH because of data statement
      contu(LPAREN) = YES
      contu(BSLASH) = YES
      contu(EQUALS) = YES
      contu(COMMA) = YES
      contu(VBAR) = YES
      contu(AMPERSAND) = YES
      contu(TILDE) = YES
      contu(LANGLE) = YES
      contu(RANGLE) = YES
# characters which are a comment in column 1
      col1(99) = .true.     # 'c'
      col1(67) = .true.     # 'C'
      col1(ASTERISK) = .true.
#XXX        col1(BANG) = .true.
# column 6 continuation conventions
      col6 = .true.
      
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine init1
include_cfile
include_ctype
      integer i

      if (optpretty == YES) then
         maxws = 1
      else
         maxws = MAXTOK+1
      endif

      if (optlang == LANG_F77) then
#           if (optpretty == YES) type(SEMICOLON) = NEWLINE
         type(SEMICOLON) = NEWLINE
         cchar = 'c'
         optrel = LANG_F77
      else if (optlang == LANG_F90) then
         cchar = '!'
         if (optpretty == YES & colcom == -1) colcom = 40
      else if (optlang == LANG_IS_F90) then
         cchar = '!'
         if (optpretty == YES & colcom == -1) colcom = 40
#        reset mppl continuation and comment defaults
#         type(POUND) = POUND  # need to recognize POUND for mppl.std
         do i=LEXMIN,LEXMAX
            contu(i) = NO
            col1(i)  = .false.
         enddo
         col6 = .false.
      endif

      if (optpretty == NO) hnl = YES
      cichar = ichar(cchar)

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      integer function initio(fil)
      character*(*) fil
      integer il, ierr
      integer lnb
      external lnb

include_cfile
include_ctlvars
include_stdunits

# initialize input and output buffers
      Filename tmpfil

      inlev = 1
      filnam(inlev) = fil
      call setmod(QUESTION,1)
      yyline(inlev) = 0
      lastpc = 0      #output line empty
      bp = 0          #push back buffer empty
      icontinue = 0
 10   continue
      
      for (il = len(filnam(inlev)), il > 0, il=il-1)
          if (' ' <> filnam(inlev)(il:il)) go to 20
      endfor
 20   continue

      if ( verbose) then
         write(stderr,101) filnam(inlev)(1:il)
 101     format('   Preprocessing ',a)
      endif
      
      tmpfil = filnam(inlev)
      call filopn(iusin(inlev),ierr,lnb(tmpfil),tmpfil)
      if (ierr <> 0 ) go to 200
      return(OK)

 200  continue
      write(stderr,100) filnam(inlev)(1:il)
 100  format('  Could not open input file ',a)

      call warn('  ******** Will proceed if others can be opened **********')

      return(ERR)
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# return the current value of modnam
      subroutine domodn
      integer lnb
      external lnb

include_cstat

      call cpbstr(modname(0)(1:lnb(modname(0))))

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# convert n into a string in token, length to ltoken
      subroutine itotok(n,token,ltoken)
      integer n,token(*),ltoken
      character*16 target
      integer i,j

      if (n == 0) then
         ltoken = 1
         token(1) = ZERO
         return
      endif

      write(target,100) n
 100  format(i16)

      do i=1,16
         if ( target(i:i) <> ' ')
         break
      enddo

      i = i - 1
      ltoken = 16 - i
      do j = 1, ltoken
         token(j) = ichar(target(i+j:i+j))
      enddo

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      function labgen(n)
      integer labgen,n

include_clabs

      labgen = labnxt
      labnxt = labnxt + n

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine reset

include_clabs

      labnxt = laborg

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine setmod(name,lname)
      integer name(1),lname,i

include_cstat

      modname(ifacelev) = ' '
      do i=1,lname
         modname(ifacelev)(i:i) = char(name(i))
      enddo

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine setorg(n)
      integer n

include_clabs

      laborg = n

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine oops(msg)
      character*(*) msg

      call warn(msg)
      call finish(FATALERROR)

      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine warn(msg)
      character*(*) msg

include_cfile

      call inform(msg)

# attempt to recover to next line
      call outlin
      bp = 1

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine inform(msg)
      character*(*) msg
      integer igoof,ilev,jlev,a1,a2,j,il, ip, jl,lnb,k
      external lnb
      character*56 mname

include_cmacro
include_cfile
include_cstat
include_cargs
include_ctlvars
include_stdunits

      finerr = finerr+1
      write(stderr,90) modname(0),msg
      ilev = inlev
      if (pbbuf(bp) = EOF) ilev = ilev + 1
      jlev = ilev
      while(ilev > 0)
         igoof = yyline(ilev)
         for (il = 1, filnam(ilev)(il:il) <> ' ', il=il+1)
             if (il == len(filnam(ilev))) break
         endfor

         if (ilev == jlev) then
            write(stderr,100) igoof,filnam(ilev)(1:il)
            do ip = 1,cp
               a1 = argstk(callst(ip)+1)
               a2 = argstk(callst(ip)+2) - 1
               jl = min(a2-a1+1,56)
               do j=1,jl
                  mname(j:j)=char(evalst(a1-1+j))
               enddo j
               if (mname=='Errprint') break
               if (mname=='Infoprint') break
               k=lnb(filnam(mlev(ip)))
               if (ip = 1) then
                  write(stderr,103) \
                  mname(1:jl),mline(ip),filnam(mlev(ip))(1:k)
               else
                  write(stderr,104) \
                  mname(1:jl),mline(ip),filnam(mlev(ip))(1:k)
               endif
            enddo ip
         else
            write(stderr,101) igoof-1,filnam(ilev)(1:il)
         endif

         ilev = ilev - 1
      endwhile ilev > 0

      call outlin
      return

 90   format(' mppl error : module = ',a/1x,a)
 100  format(' Near line no. ',i5,' in file ',a)
 101  format(' (Included from line no. ',i5,' in file ',a,')')
 103  format(' ERROR OCCURRED DURING MACRO/KEYWORD PROCESSING:'/\
      ' Error in  ',a,' which began on line ',i5,' of file ',a)
 104  format(' which called  ',a,' on line ',i5,' of file ',a)

      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# put out the statement 'n continue'

      subroutine outcnt(n, indent, iblock)
      integer n, indent, iblock

include_cfile

      if (optpretty == YES) then
         if (lastpc > 0)
         call inform('Label not permitted on this kind of statement.')
      else
         lastpc = 0
      endif

      call puti5(n)
      call outtab(indent, iblock)
      call putqs('continue')
      call outlin

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# put the statment 'go to n' into the output buffer, call outlin
      
      subroutine outgo(n)
      integer n
      
      call putqs('go to ')
      call puti5(n)

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# if a label is already present, output a continue on it
# otherwise do nothing
# used to handle labels on statements that generate their own label
# like while, block do

      subroutine outifl

include_cfile

      if (lastpc <> 0) then
         call outtab(0,0)
         call putqs('continue')
         call outlin
      endif

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# output one line
      subroutine outlin

include_cfile
include_cstat
include_stdunits

      character*(MPPL_MAXCARD) msg
      integer zpakchrz, n
      external zpakchrz

      n = zpakchrz(msg, len(msg), outbuf,lastpc)
      call wrline(stdout,msg,n)
      lastpc = 0
      icontinue = 0
      nonblk = NO

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# get past statement field
# if already there, do nothing
      
      subroutine outtab(indent, iblock)

include_cfile
include_cstat

      integer indent, iblock
      integer newpc, i
      
#        if (lastpc > 5)
#           return
      
      if (optpretty == YES) then
         newpc = 6+(iflevel + level + sellev + ifacelev+ icontinue)*indlev
      else
# indent = 0, uses indpc
         newpc = max(indent,indpc) + iblock*indlev + icontinue*indlev
      endif
      
      do i=lastpc+1,newpc
         outbuf(i) = BLANK
      enddo
      
      lastpc = max(lastpc,newpc)
      conpc = newpc
      
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# Add some spaces into the output
      
      subroutine outfil(width)

include_cfile
#include_cstat

      integer newpc, i, width

      newpc = lastpc + width
      do i=lastpc+1,newpc
         outbuf(i) = BLANK
      enddo
      lastpc = newpc

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine pbstr(in,n)

# push back in

      integer in(1)
      integer n
      integer i,bpnew

include_cfile

      bpnew = bp + n
      if (bpnew > BUFSIZE)
         call oops('Macro processor error in pbstr:'//\
                   ' too many characters pushed back')

      do i = 1, n
         pbbuf(bp + i) = in(n + 1 - i)
      enddo

      bp = bpnew

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      function peek()

# return next non-blank character
# only checks in this line

      integer peek

include_ctype
include_cfile

      integer i

      do i=bp,2,-1
         if (type(pbbuf(i)) <> WHITE) break
      enddo

      return(pbbuf(i))

      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine prolog

# insert a statement Prolog after each module card

include_cstat
include_cfile

      if (ifacelev == 0 & optmacro == YES) then
         call putbak(NEWLINE)
         call cpbstr('      Prolog')
      endif

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine push(ep,argstk,ap)
      integer ep,argstk(ARGSIZE),ap
      
      if (ap >= ARGSIZE)
         call oops('Macro processor error: argument stack overflow.')
      argstk(ap) = ep
      ap = ap + 1

      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine putarg(cout,n)
      integer i,n
      integer cout(1)

include_cmacro

      if (ep + n > EVALSIZE)
         call oops('Macro processor error: evaluation stack overflow.')

      do i=1,n
         evalst(ep - 1 + i ) = cout(i)
      enddo
      ep = ep + n

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine putbak(c)
      integer c

include_cfile

      bp = bp + 1
      if (bp > BUFSIZE)
         call oops('Macro processor error: '//\
                   'too many characters pushed back.')
      pbbuf(bp) = c

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine putchr(cout,n)
      integer i,n, nc, idone
      integer cout(1)
      integer zpakchrz, k
      character*(MPPL_MAXCARD) msg

include_cfile
include_cstat
include_stdunits

      if ( lastpc + n <= col72 ) then
         do i=1,n
            outbuf(lastpc + i) = cout(i)
         enddo
         lastpc = lastpc + n
         nonblk = YES
         return
      endif

# doesn't fit
# blast out existing line, set up for continuation
# if characters have been written past conpc that are nonblank
      if (lastpc > conpc & nonblk == YES) call conlin

      call outtab(0,0)

# watch out for extremely long tokens
      nc = 0
      do
         if ( lastpc + n - nc <= col72) then
            do i=1,n-nc
               outbuf(lastpc + i) = cout(nc + i)
            enddo
            lastpc = lastpc + n - nc
            nonblk = YES
            return
         endif
         if (optlang .eq. LANG_F77) then
            idone = col72 - lastpc
            do i=1,idone
               outbuf(lastpc + i) = cout(nc + i)
            enddo
            k = zpakchrz(msg,col72, outbuf,col72)
            call wrline(stdout,msg,k)
            lastpc = 6
         else if (optlang .eq. LANG_F90) then
            idone = col72 - lastpc - 1
            do i=1,idone
               outbuf(lastpc + i) = cout(nc + i)
            enddo
            outbuf(col72) = AMPERSAND
            k = zpakchrz(msg,col72, outbuf,col72)
            call wrline(stdout,msg,k)
            lastpc = 0
            call outtab(0,0)
            lastpc = lastpc + 1
            outbuf(lastpc) = AMPERSAND
         else if (optlang .eq. LANG_IS_F90) then
            idone = col72 - lastpc - 1
            do i=1,idone
               outbuf(lastpc + i) = cout(nc + i)
            enddo
            outbuf(col72) = AMPERSAND
            k = zpakchrz(msg,col72, outbuf,col72)
            call wrline(stdout,msg,k)
            lastpc = 0
            call outtab(0,0)
            lastpc = lastpc + 1
            outbuf(lastpc) = AMPERSAND
         else
            call oops("Unexpected value of oplang")
         endif
         nc = nc + idone
      enddo

      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# continue the current line
      
      subroutine conlin

include_cfile
include_cstat
include_stdunits

      integer i
      
      if (optlang .eq. LANG_F77) then
         call outlin
         do i=1,5
            outbuf(i) = BLANK
         enddo
         outbuf(6) = AMPERSAND
         lastpc = 6
      else if (optlang .eq. LANG_F90) then
         outbuf(lastpc + 1) = BLANK
         outbuf(lastpc + 2) = AMPERSAND
         lastpc = lastpc + 2
         call outlin
      else if (optlang .eq. LANG_IS_F90) then
         outbuf(lastpc + 1) = AMPERSAND
         lastpc = lastpc + 1
         call outlin
      else
         call oops("Unexpected value for optlang - conlin")
      endif
      conpc = lastpc

      icontinue = 1
      if (optpretty == YES) call outtab(0,0)
      
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine puti5(n)
# adds the character representation of n to the current output line
# used only for label fields...right adjust in 5 characters

      integer n, m, i
      integer lb(5)

      m = n
      lb(5) = mod(m,10) + ZERO
      m = m/10
      do i=4,1,-1
         if ( m = 0) then
            lb(i) = BLANK
         else
            lb(i) = mod(m,10 ) + ZERO
            m = m/10
         endif
      enddo

      call putchr(lb,5)

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine putlab(token,ltoken)
      integer token(*),ltoken, i

include_cfile

      do i=1,ltoken
         outbuf(i) = token(i)
      enddo

      do i=ltoken+1,6
         outbuf(i) = BLANK
      enddo

      lastpc = 6

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# PUTQS - 

      subroutine putqs(str)
      character*(*) str
      integer i,n
      integer qs(80)

include_cfile

      n = len(str)
      do i=1,n
         qs(i) = ichar(str(i:i))
      enddo

      call putchr(qs,n)

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine sbrks

include_cstat

      integer t,gnbtok,toktoi
      external gnbtok,toktoi
      integer nlev
      
# look for digit after the next
      t = gnbtok(token,ltoken)
      if ( t == DIGIT) then
         nlev = toktoi(token,ltoken) - 1
         t = gnbtok(token,ltoken)
      else
         nlev = 0
      endif

      if (level-nlev <= 0) then
         call warn('Illegal -break- statement, level wrong')
      else
         call outtab(0,0)
         call outgo(labb(level-nlev))
         useb(level-nlev) = YES
# shouldn't be anything else here
         if (t == COMMENT) then
            call endcomment(CBEFORE, 0, token, ltoken, 0)
         else if (t == NEWLINE) then
            call outlin
         else
            call warn('Illegal syntax in -break- statement.')
         endif
      endif

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine sbrks90

include_cstat

      integer t,gtok,toktoi,wswid
      external gtok,toktoi
      integer nlev
      
      wswid = 0
# look for digit after the next
      t = gtok(token,ltoken)
      if (t == WHITE) then
         wswid = ltoken
         t = gtok(token,ltoken)
      endif

      if (t == DIGIT) then
         nlev = toktoi(token,ltoken) - 1
         t = gtok(token,ltoken)
      else
         nlev = 0
      endif

      if (level-nlev <= 0) then
         call warn('Illegal -break- statement, level wrong')
      else
         call outtab(0,0)
         if (nlev == 0) then
            call putqs('exit')
         else
            useb(level-nlev) = YES
            call outgo(labb(level-nlev))
         endif

         if (t == WHITE) then
            wswid = ltoken
            t = gtok(token,ltoken)
         endif

# shouldn't be anything else here
         if (t == COMMENT) then
            call endcomment(CBEFORE, 0, token, ltoken, wswid)
         elseif (t == NEWLINE) then
            call outlin
         else
            call warn('Illegal syntax in -break- statement.')
         endif
      endif

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine sdo

include_cstat

      integer labgen,gnbtok,toktoi
      external labgen,gnbtok,toktoi
      integer t, n

# expand a do statement -- statement might have a label
      doindent(level+1) = indpc

# peek ahead
      t = gnbtok(token,ltoken)
      if (t == DIGIT) then  #Old style, user supplied label for the end
         call outtab(0,0)   # get past statement field
         call putqs('do ')  # XXX - put out 'do '
         level = level + 1
         dotype(level) = OLD
         labb(level) = labgen(1)
         labn(level) = toktoi(token,ltoken)
         useb(level) = NO
         call putchr(token,ltoken)
         call eatup(0)
      elseif (t == NEWLINE | t == COMMENT) then
         if (t == COMMENT) call endcomment(CBEFORE, 0, token, ltoken, 0)
         call outifl
         n = labgen(1)
         call outcnt(n,0,0)  #target for repeat, until
         level = level + 1
         dotype(level) = BLOCK
         labn(level) = n
         labb(level) = labgen(1)
         useb(level) = NO
      else  # new style do var=... or do for var=...
         if ( t == ESCAPE) then
            if (token(2) = SFOR) then
               t=gnbtok(token,ltoken)
            elseif (token(2) = SWHILE) then
               call swhile
               return
            else
               call warn(' Syntax error in do statement.')
               return
            endif
         endif
         call outtab(0,0)
         call putqs('do ') #put out 'do '
         level = level + 1
         dotype(level) = REGULAR
         labn(level) = labgen(1)
         labb(level) = labgen(1)
         useb(level) = NO
         call puti5(labn(level))
         code(1) = BLANK
         call putchr(code,1)
         call putchr(token,ltoken)
         call eatup(0)
      endif

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine sdo90

include_cstat

      integer labgen,gnbtok,toktoi
      external labgen,gnbtok,toktoi
      integer t
      
                                ! expand a do statement -- statement might have a label
      doindent(level+1) = indpc
# peek ahead
      t = gnbtok(token,ltoken)
      if (t == DIGIT) then  #Old style, user supplied label for the end
         call outtab(0,0)   # get past statement field
         call putqs('do ')  #put out 'do '
         level = level + 1
         dotype(level) = OLD
         labb(level) = labgen(1)
         labn(level) = toktoi(token,ltoken)
         useb(level) = NO
         usen(level) = NO
         call putchr(token,ltoken)
         call eatup(0)
      elseif (t == NEWLINE | t == COMMENT) then
         call outtab(0,0)
         call putqs('do') #put out 'do '
         if (t .eq. COMMENT) then
            call endcomment(CBEFORE, 0, token, ltoken, 0)
         else
            call outlin
         endif
         level = level + 1
         dotype(level) = BLOCK90
         labn(level) = labgen(1)
         labb(level) = labgen(1)
         usen(level) = NO
         useb(level) = NO
      else  # new style do var=... or do for var=...
         if (t .eq. ESCAPE) then
            if (token(2) .eq. SFOR) then
               t=gnbtok(token,ltoken)
            elseif (token(2) .eq. SWHILE90) then
               call swhile90
               return
            else
               call warn(' Syntax error in do statement.')
               return
            endif
         endif
         call outtab(0,0)
         call putqs('do ') #put out 'do '
         level = level + 1
         dotype(level) = REGULAR90
         labn(level) = labgen(1)
         labb(level) = labgen(1)
         usen(level) = NO
         useb(level) = NO
         call putchr(token,ltoken)
         call eatup(0)
      endif

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine sedo

# process enddo or labeled target of traditional do

include_cstat

      integer gnbtok,lnb
      external gnbtok,lnb
      integer it,nlev,lab,i,nforiter,oldpc

      if (level == 0) then
         call warn('Unmatched end of do block.')
         return
      endif
      oldpc = doindent(level)
      
      it = dotype(level)
      if (it == REGULAR) then
         call outifl
         level = level - 1
         call outcnt(labn(level+1),0,0)
         if (useb(level+1) == YES) call outcnt(labb(level+1),0,0)
         call spit(CBEFORE)
      elseif (it == OLD) then
# dofile has just processed the labeled statement on a traditional do
# put out the continue statements for breaks
# have to watch out for the case of multiple old-style dos with the
# SAME target  i.e. do 200 i= 1,100 ; do 200 j=1,100 ; .... 200 continue
         nlev = level   #save level for later use
         lab = labn(level)
         level = level - 1
# get the new level of indentation
         while(labn(level) == lab)  #this is sure to stop (labn(0)=0)
            level = level - 1
         endwhile
         do i=nlev,level+1,-1
            if (useb(i) == YES) call outcnt(labb(i),doindent(i),0)
         enddo

      elseif (it == BLOCK) then
         call outifl
         call putqs('c -- repeat')
         call outlin
         level = level - 1
         call outtab(oldpc,0)
         call outgo(labn(level+1))
         call spit(CAFTER)
         if (useb(level+1) == YES) call outcnt(labb(level+1),oldpc,0)

      elseif (it == WHILE) then
         call sewhile

      elseif (it == REGULAR90) then
         if (usen(level) == YES) call outcnt(labn(level),oldpc,1)
         level = level - 1
         call outtab(oldpc,0)
         call putqs('enddo')
         call spit(CAFTER)
         if (useb(level+1) == YES) call outcnt(labb(level+1),oldpc,0)

      elseif (it == BLOCK90) then
         if (usen(level) == YES) call outcnt(labn(level),0,1)
         level = level - 1
         call outtab(oldpc,0)
         call putqs('enddo')
         call spit(CAFTER)
         if (useb(level+1) == YES) call outcnt(labb(level+1),oldpc,0)

      elseif (it == FOR90) then
         if (usen(level) == YES) call outcnt(labn(level),0,1)
# Add the for loop increment
         call outtab(0,1)
         nforiter = lnb(foriter(level))
         call putqs(foriter(level)(:nforiter))
         call outlin
         level = level - 1
         call outtab(0,0)
         call putqs('enddo')
         call spit(CAFTER)
         if (useb(level+1) == YES) call outcnt(labb(level+1),0,0)

      elseif (it == WHILE90) then
         call sewhile90

      elseif (it == DOPRETTY) then
          level = level - 1
          call outtab(oldpc,0)
          call putqs('enddo')
          call eatup(0)
      endif

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine sefor
include_cfile

      call sedo
      call putqs(cchar//' endfor')
      call outlin

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine selif
# process elseif statement
# call docond to output condition & translate logical operators
# elseif (condition) must be followed by then; we supply even if missing
include_cstat
      integer stoken(MAXTOK), sltoken, i
      integer t,gtok,gnbtok,gnbtokw,docond,wswid
      external gtok,gnbtok,gnbtokw,docond
      
      if (iflevel == 0) then
         call warn('Elseif not inside if block.')
         return
      endif

      iflevel = iflevel - 1
      call outtab(0,0)
      call putqs('elseif')  # XXX add space between 'else if'
      if (docond() <> 0) return
      iflevel = iflevel + 1

# 1) if () # then
# 2) if () #           --> if () then #
# 3) if () \n          --> if () then \n
# 4) if () then
# 5) if () \r
# 6) if () \r then

      t = gnbtokw(token,ltoken,wswid)
      if (t == COMMENT) then
# save comment, look at next token         
         do i=1,ltoken
            stoken(i) = token(i)
         enddo
         sltoken = ltoken
         t = gnbtokw(token, ltoken, wswid)
         if (t == LINEFEED) then
            t = gnbtokw(token, ltoken, wswid)
         endif
         if (t == ESCAPE & token(2) == STHEN) then
            call endcomment(CBEFORE, 1, stoken, sltoken, wswid)
            call outtab(0,0)
            call putqs(' then')
            call spit(CAFTER)
         else
            call pbstr(token,ltoken)
            call putqs(' then')
            call endcomment(CAFTER, 0, stoken, sltoken, wswid)
         endif

      else if (t == LINEFEED) then
         t = gnbtokw(token, ltoken, wswid)
         if (t == ESCAPE & token(2) == STHEN) then
            call putqs(' then')
            call spit(CAFTER)
         else
            call pbstr(token,ltoken)
            call putqs(' then')
         endif
      else if (t == NEWLINE) then
         call putqs(' then')
         call outlin
      else if (t == ESCAPE & token(2)==STHEN) then
         call putqs(' then')
         call spit(CAFTER)
      else
         call warn('Syntax error in elseif statement.')
         call spit(CAFTER)
      endif

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine selse
include_cstat
      integer gtok,wswid
      external gtok
      integer t

      if (iflevel == 0) then
         call warn('Unmatched else.')
         return
      endif

      wswid = 0
      t = gtok(token,ltoken)
      if (t == WHITE) then
         wswid = ltoken
         t = gtok(token,ltoken)
      endif

# check for 'else if' which is treated as elseif
      if (t == ESCAPE) then
         if (token(2) = SIF) then
            call selif
            return
         endif
      endif

      iflevel = iflevel - 1
      call outtab(0,0)
      call putqs('else')

      if (t == COMMENT) then
         call endcomment(CBEFORE, 0, token, ltoken, wswid)
      else if (t == NEWLINE) then
         call outlin
      else
         call outlin
         call warn('Syntax error in else statement')
      endif

      iflevel = iflevel + 1

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine sendif

include_cstat

      if (iflevel == 0) then
         call warn('Unmatched endif.')
         return
      endif

      iflevel = iflevel - 1
      call outtab(0,0)
      call putqs('endif')
      call spit(CAFTER)

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine setopt(optstr)

c processes all the options

      character*(*) optstr
      integer c1,i, n, ind1
      integer i23000, i23005, i23023, i23051, i23059
      integer evalone,ierr
      external evalone

include_irset
include_idircom
include_cfile
include_ctype
include_icom
include_ctlvars
include_fname
include_stdunits

# is passed the option string with the leading - removed
      
      if (optstr .eq. "-nolang") then
         optlang = LANG_NONE
         optpretty = NO
      else if (optstr .eq. "-langf77") then
         optlang = LANG_F77
         cchar = 'c'
      else if (optstr .eq. "-langf90") then
         optlang = LANG_F90
      else if (optstr .eq. "-isf77") then
         optlang = LANG_IS_F77
      else if (optstr .eq. "-isf90") then
         optlang = LANG_IS_F90
      else if (optstr .eq. "-macro") then
         optmacro = YES
      else if (optstr .eq. "-nomacro") then
         optmacro = NO
      else if (optstr .eq. "-nonumeric") then
         optnum = NO
         basis = " "
      else if (optstr .eq. "-pretty") then
         optpretty = YES
      else if (optstr .eq. "-nopretty") then
         optpretty = NO
      else if (optstr .eq. "-relationalf77") then
         optrel = LANG_F77
      else if (optstr .eq. "-relationalf90") then
         optrel = LANG_F90
         
      else if (optstr .eq. "-honour-newlines") then
         hnl = YES
      else if (optstr .eq. "-honor-newlines") then
         hnl = YES
      else if (optstr .eq. "hnl") then
         hnl = YES
         
      else if (optstr .eq. "-allocate") then
         optalloc = YES

      else if (optstr(1:11) .eq. "-linelength") then
         col72 = evalone(optstr(12:),ierr)
         
      else if (optstr(1:25) .eq. "-continuation-indentation") then
         indlev = evalone(optstr(26:),ierr)
      else if (optstr(1:2) .eq. "ci") then
         indlev = evalone(optstr(3:),ierr)
         
      else if (optstr(1:20) .eq. "-comment-indentation") then
         colcom = evalone(optstr(21:),ierr)
      else if (optstr(1:4) .eq. "comi") then
         colcom = evalone(optstr(5:),ierr)
         
      else
         c1 = ichar(optstr(1:1))
         select (c1)
            case ZERO-NINE:
               n = c1 - ZERO
               do i=2,len(optstr)
                  c1 = ichar(optstr(i:i))
                  select(c1)
                     case ZERO-NINE:
                        n = n*10+c1-ZERO
                     case BLANK: break
                     default: go to 900
                  endselect
               enddo i
               call setorg(n)
            case 119:   # w
               lexwarn = YES
            case 98:    #b
               bckeep = .false.
            case 99:    #c
               do i=LEXMIN,LEXMAX
                  col1(i) = .false.
               enddo
               do i=2,len(optstr)
                  c1 = ichar(optstr(i:i))
                  select c1
                     case BLANK: 
                        break
                     default: 
                        col1(c1) = .true.
                  endselect
               enddo
            case 67:    #C
               call cnstal('COMPILER',optstr(2:))
            case 100:     # d
               nodblquo = YES
            case 68:    # D
               ind1 = index(optstr, '=')
               if (ind1 == 0) then
                  ind1 = index(optstr,' ')
                  call cnstal(optstr(2:ind1-1),' ')
               elseif (len(optstr) == ind1) then
                  call cnstal(optstr(2:ind1-1), ' ')
               else
                  call cnstal(optstr(2:ind1-1), optstr(ind1+1:))
               endif
            case 102: #f
# free form input: no col1 convention, no col6 convention
               do i=LEXMIN,LEXMAX
                  col1(i) = .false.
               enddo
               col6 = .false.
            case  73: #I
               inclnum = inclnum + 1
               incldirs(inclnum) = optstr(2:)
            case  108: #l
               if (optstr(2:) == " ") then
                  col72 = 80
               else
                  col72 = evalone(optstr(2:),ierr)
               endif
            case  109: #m
               basis=" "
            case  77: #M
               call cnstal('MACHINE',optstr(2:))
            case 116:  #t
               system=optstr(2:)
            case 105: #i
               intsize = evalone(optstr(2:),ierr)
               select(intsize)
                  case 2,4,8: ireset = .true.
                  default: goto 900
               endselect
            case 114: #r
               realsize = evalone(optstr(2:),ierr)
               select(realsize)
                  case 4,8,16: rreset = .true.
                  default: goto 900
               endselect
            case 117: #u
               call notsen
            case 118:  #v
               verbose=.not.verbose
            default:
               go to 900
         endselect
      endif
      return
# bad options
 900  continue
      write(stderr,100) optstr
 100  format(' Error in option....'/a)
      call finish(FATALERROR)
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine sewhile
# do endwhile statement
# put out go to L,endif
include_cstat
      integer oldpc
      oldpc = doindent(level)
      call outifl
      call outtab(oldpc,0)
      call outgo(labn(level))
      call outlin
      level = level - 1
      call outtab(0,0)
      call putqs('endif')
      call outlin
      call putqs('c endwhile')
      call spit(CAFTER)
      if (useb(level+1) == YES) call outcnt(labb(level+1),0,0)
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# do endwhile statement
      
      subroutine sewhile90
include_cstat
      integer oldpc
      oldpc = doindent(level)
      if (usen(level) == YES) call outcnt(labn(level),oldpc,1)
      level = level - 1
      call outtab(oldpc,0)
      call putqs('enddo')
      call spit(CAFTER)
      if (useb(level+1) == YES) call outcnt(labb(level+1),oldpc,0)
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# process if statement
# call docond to output condition & translate logical operators
# if (condition) may be followed by
# a. then -- put out as is
# b. some other statement
#     We check on the next line if nothing follow the cond.
# Note that return(value) has to be handled correctly.

      subroutine sif
include_cstat
include_cfile
      integer t,gnbtok,gtok,docond,wswid
      external gnbtok,gtok,docond
      
      call outtab(0,0)
      call putqs('if')
      if (docond() <> 0) return
      
      wswid = 0
      t = 0
      do
         if (t == 0) t = gtok(token,ltoken)
         if (t == COMMENT) then
            call endcomment(CBEFORE, 1, token, ltoken, wswid)
            wswid = 0
            t = 0
            if (icontinue == 1) then # --langf90
               if (optpretty == YES) then
                  call outtab(0,0)
                  t = gnbtok(token,ltoken)
                  icontinue = 0
               else
                  icontinue = 0
                  t = gtok(token,ltoken)
                  if (t == WHITE) call outtab(ltoken,0)
               endif
            endif
            next
         elseif (t == LINEFEED) then
            wswid = 0
            if (nonblk == YES) call conlin
         elseif (t == NEWLINE) then
            wswid = 0
            if (hnl == YES) call conlin
         elseif (t == WHITE) then
            wswid = ltoken
         else
            break
         endif
         t = 0
      enddo
      call outfil(wswid)
      
      iflevel = iflevel + 1
      icontinue = 0
      if (t <> ESCAPE) then
         call outtab(0,0)
         call putchr(token,ltoken)
         call eatup(0)
         iflevel = iflevel - 1
         return
      else
         t = token(2)
      endif
      if (t == STHEN) then
         call putqs('then')
         call spit(CAFTER)
      else
         if (t == MRETURN) then
            if (modfun .eq. YES) then
               call doret(.true.)
            else
               call doret(.false.)
            endif
         elseif (t == SBREAK) then
            call sbrks
         elseif (t == SNEXT) then
            call snext
         elseif (t == SBREAK90) then
            call sbrks90
         elseif (t == SNEXT90) then
            call snext90
         else #?? something wrong
            call putchr(token,ltoken)
            call eatup(0)
         endif
         iflevel = iflevel - 1
      endif
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine snext
include_cstat
      integer t,gnbtok,toktoi
      external gnbtok,toktoi
      integer nlev

# look for digit after the next
      t = gnbtok(token,ltoken)
      if ( t == DIGIT) then
         nlev = toktoi(token,ltoken) - 1
         t = gnbtok(token,ltoken)
      else
         nlev = 0
      endif

      if (level-nlev <= 0) then
         call warn('Illegal -next- statement, level wrong')
      else
         call outtab(0,0)
         call outgo(labn(level-nlev))
# shouldn't be anything else here
         if (t == COMMENT) then
            call endcomment(CBEFORE, 0, token, ltoken, 0)
         else if (t == NEWLINE) then
            call outlin
         else
            call warn('Illegal syntax in -next- statement.')
         endif
      endif

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine snext90
include_cstat
      integer t,gtok,toktoi,wswid
      external gtok,toktoi
      integer nlev
      
      wswid = 0
# look for digit after the next
      t = gtok(token,ltoken)
      if (t == WHITE) then
         wswid = ltoken
         t = gtok(token,ltoken)
      endif

      if ( t == DIGIT) then
         nlev = toktoi(token,ltoken) - 1
         t = gtok(token,ltoken)
      else
         nlev = 0
      endif

      if (level-nlev <= 0) then
         call warn('Illegal -next- statement, level wrong')
      else
         call outtab(0,0)
# next and break beyond the inner loop requires labels
# as well as next from a for loop which must do the increment step.
         if (nlev == 0 & dotype(level) <> FOR90) then
            call putqs('cycle')
         else
            usen(level-nlev) = YES
            call outgo(labn(level-nlev))
         endif

         if (t == WHITE) then
            wswid = ltoken
            t = gtok(token,ltoken)
         endif

# shouldn't be anything else here
         if (t == COMMENT) then
            call endcomment(CBEFORE, 0, token, ltoken, wswid)
         else if (t == NEWLINE) then
            call outlin
         else
            call warn('Illegal syntax in -next- statement.')
         endif
      endif

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# delete to end of line, inclusive
# but preserve comments
      
      subroutine spit(ipos)
include_cstat
include_cfile  # lastpc
      integer ipos, wswid, t
      integer gtok
      external gtok
      
      wswid = 0
      do
         t = gtok(token,ltoken)
         if (t .eq. COMMENT) then
            call endcomment(ipos, 0, token, ltoken, wswid)
            break
         elseif (t .eq. WHITE) then
            wswid = ltoken
         elseif (t .eq. NEWLINE) then
            if (lastpc <> 0)
               call outlin
            break
         endif
      enddo
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine suntil
# end block do with until(condition)
# translates to: if (.not.(condition)) go to L ; enddo
include_cstat
      integer docond, oldpc
      external docond
      if (level == 0) then
         call warn('Extraneous until statement.')
         return
      elseif (dotype(level) <> BLOCK)
         call warn('Until statement in wrong kind of do loop.')
         return
      endif
      oldpc = doindent(level)
      call outifl
      level = level - 1
      call outtab(oldpc,1)
      call putqs('if ( .not.')
      if (docond() <> 0) return
      code(1) = BLANK
      code(2) = RPAREN
      call putchr(code,2)
      call outgo(labn(level+1))
      call spit(CAFTER)
      if (useb(level+1) == YES) call outcnt(labb(level+1),oldpc,0)
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# end block do with until(condition)
# translates to: if (condition) exit; enddo
      
      subroutine suntil90
include_cstat
      integer oldpc
      integer docond
      external docond
      
      if (level == 0) then
         call warn('Extraneous until statement.')
         return
      elseif (dotype(level) <> BLOCK90) then
         call warn('Until statement in wrong kind of do loop.')
         return
      endif
      
      oldpc = doindent(level)
      
      if (usen(level) == YES) call outcnt(labn(level),oldpc,1)
      call outtab(0,1)
      call putqs('if')
      if (docond() <> 0) return
      call putqs('exit')
      call spit(CAFTER)
      level = level - 1
      call outtab(0,0)
      call putqs('enddo')
      call outlin
      if (useb(level+1) == YES) call outcnt(labb(level+1),oldpc,0)
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine swhile
# translate while(cond) to
#       continue   (in case this statement was labeled)
# L     if (cond) then
#
include_cstat
      integer docond,n, labgen
      external docond, labgen
#
      call outifl
      n = labgen(2)
      call puti5(n)
      call outtab(0,0)
      call putqs('if')
      if (docond() <> 0) return
      call putqs(' then')
      level = level + 1
      labn(level) = n
      labb(level) = n + 1
      useb(level) = NO
      dotype(level) = WHILE
      call spit(CAFTER)
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# translate while(cond) to
#       do while (cond)
      
      
      subroutine swhile90
include_cstat
      integer n
      integer docond, labgen, getdef
      external docond, labgen, getdef
      
      doindent(level+1) = indpc
      n = labgen(2)
      call outtab(0,0)
      call putqs('do while')
      if (docond() <> 0) return
      call spit(CBEFORE)
      level = level + 1
      labn(level) = n
      labb(level) = n + 1
      usen(level) = NO
      useb(level) = NO
      foriter(level) = " "
      if (getdef('mppl_foriter', foriter(level)) >= 0) then
# do not reuse macro with next loop
         call undef('mppl_foriter')
         dotype(level) = FOR90
      else
         dotype(level) = WHILE90
      endif
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      integer function toktoi(token,toksiz)
# convert a token to an integer
      integer token(1),toksiz,i,j,k,isgn
      toktoi = 0
      isgn = 1
      do j=1,toksiz
         if (token(j) <> BLANK) break
      enddo
      if (token(j) == MINUS) then
         isgn = -1
         k=j + 1
         do j=k,toksiz
            if (token(j) <> BLANK) break
         enddo
      endif
      do i=j,toksiz
         toktoi = toktoi*10 + token(i) - ZERO
      enddo
      toktoi = toktoi*isgn
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine sselect
# sselect - generate code for beginning of select statement
      integer lab, t
      integer labgen, gnbtok
include_cstat
      lab = labgen(2)
      if (sellast + 3 > MAXSELECT)
         call oops('select table overflow.')
      call outifl
      call putqs('c select')
      call outlin
      call outtab(0,0)    # Innn=(e)
      call selvar(lab)
      t = gnbtok(token,ltoken)
      if (t = NEWLINE) then
         call warn('select statement syntax error.')
         return
      endif
      if (t <> EQUALS) then
         code(1) = EQUALS
         call putchr(code,1)
      endif
      call putchr(token,ltoken)
      call eatup(0)
      sellev = sellev + 1
      if (sellev > MAXDEPTH)
         call oops('select statements nested too deeply.')
      sellab(sellev) = lab
# the triplets in selstak represent lower, upper bounds + label
# in the FIRST one however, at seltop,
# selstak(seltop) = previous seltop
# selstak(seltop+1) = number of cases in this select so far
# selstak(seltop+2) = label for default case, 0 if no default stat yet.
      selstak(sellast) = seltop
      selstak(sellast+1) = 0
      selstak(sellast+2) = 0
      seltop = sellast
      sellast = sellast + 3
      call outtab(0,0)
      call outgo(lab)  # goto L
      call outlin
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# sselect - generate code for beginning of select statement
      
      subroutine sselect90
include_cstat
      integer t
      integer gnbtok
      external gnbtok
      
      if (sellast + 3 .gt. MAXSELECT)
         call oops('select table overflow.')
# XXX - ?
      call outtab(0,0)    # Innn=(e)
      t = gnbtok(token,ltoken)
      if (t == NEWLINE) then
         call warn('select statement syntax error.')
         return
      endif
      call putqs('select case (')
      call putchr(token,ltoken)
      code(1) = RPAREN
      call eatup(1)
      sellev = sellev + 1
      if (sellev .gt. MAXDEPTH)
         call oops('select statements nested too deeply.')
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine scase(td)
# case or default statement
# td is SCASE or SDEFAULT
      integer td
      integer t, l, lb, ub, i, j, lab, junk
      integer caslab, labgen, gnbtok
include_cstat
      if (sellev <= 0) then
         call warn('illegal case or default.')
         return
      endif
      call outifl
      lab = sellab(sellev)

      if (selstak(seltop+1) > 0) then
# in case the previous statement was a break or other goto, label this one
         i = labgen(1)
         call puti5(i)
         call outtab(0,0)
         call outgo(lab+1)  # terminate previous case
         call outlin
      endif

      l = labgen(1)
      if (td = SCASE) then   # case n[,n]... : ...
         while (caslab(lb, t) <> NEWLINE)
            ub = lb
            if (t == MINUS)
               junk = caslab(ub, t)
            if (lb > ub) then
               call warn('illegal range in case label.')
               return
            endif

            if (sellast + 3 > MAXSELECT)
               call oops('select table overflow.')

            for (i = seltop + 3, i < sellast, i = i + 3)
                if (lb <= selstak(i)) then
                   break
                else if (lb <= selstak(i+1)) then
                   call warn('duplicate case label.')
                   return
                endif
            endfor

            if (i < sellast & ub >= selstak(i)) then
               call warn('duplicate case label.')
               return
            endif

# insert new entry
            for (j = sellast, j > i, j = j - 1)
                selstak(j+2) = selstak(j-1)
            endfor

            selstak(i) = lb
            selstak(i+1) = ub
            selstak(i+2) = l
            selstak(seltop+1) = selstak(seltop+1) + 1
            sellast = sellast + 3
            call putqs('c -- case ')
            call outnum(lb)
            if (ub > lb) then
               call putqs('- ')
               call outnum(ub)
            endif

            call outlin

            if (t == COLON) then
               break
            else if (t <> COMMA) then
               call warn('illegal case syntax.')
               return
            endif
         endwhile

      else      # default : ...
         call putqs('c -- case (default)')
         call outlin
         t = gnbtok(token, ltoken)
         if (selstak(seltop+2) <> 0) then
            call warn('multiple defaults in select statement.')
            return
         endif
         selstak(seltop+2) = l
      endif

      if (t <> COLON)
         call inform('missing colon in case or default label.')

      sellev = sellev - 1
      call outcnt(l,0,0)
      sellev = sellev + 1

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# caslab - get one case label
      function caslab(n, t)
      integer caslab
      integer n, t
      integer s
      integer gnbtok, toktoi
include_cstat
      t = gnbtok(token, ltoken)
      if (t == NEWLINE)
         return(t)
      if (t == MINUS) then
         s = -1
      else
         s = +1
      endif
      if (t == MINUS | t == PLUS)
         t = gnbtok(token, ltoken)
      if (t <> DIGIT) then
         call inform('invalid case label.')
         t = COLON
         n = 9999
         return(0)
      endif
      n = s*toktoi(token,ltoken)
# get next token (should be comma or colon)
      t = gnbtok(token, ltoken)
      return(0)
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# case or default statement
# td is SCASE or SDEFAULT
      
      subroutine scase90(td)
include_cstat
include_cfile
      integer td
      integer t, junk, wswid
      integer caslab90, gnbtok, gtok
      external gnbtok, gtok
      
      if (sellev .le. 0) then
         call warn('illegal case or default.')
         return
      endif
      if (td == SCASE90) then   # case n[,n]... : ...
         sellev = sellev - 1
         call outtab(0,0)
         sellev = sellev + 1
         call putqs('case (')
         while (caslab90(t) <> NEWLINE)
            if (t == MINUS) then
               call putqs(':')
               junk = caslab90(t)
            endif
            if (t == COLON) then
               break
            else if (t <> COMMA) then
               call warn('illegal case syntax.')
               return
            endif
            call putqs(',')
         enddo
         call putqs(')')
      else      # default : ...
         sellev = sellev - 1
         call outtab(0,0)
         sellev = sellev + 1
         call putqs('case default')
         t = gnbtok(token, ltoken)
      endif

      if (t <> COLON) then
         call inform('missing colon in case or default label.')
      endif

# The statment may be on the same line or the next
      t = gtok(token, ltoken)
      if (t == WHITE) then
         wswid = ltoken
         t = gtok(token, ltoken)
      else
         wswid = 0
      endif
      if (t == COMMENT) then
         call endcomment(CAFTER, 0, token, ltoken, wswid)
      else
         if (t <> NEWLINE) then
            call pbstr(token,ltoken)
# Any statement immediately following will be indented a line
            indflg = -1
         endif
         call outlin
      endif
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# caslab - get one case label
      
      function caslab90(t)
include_cstat
      integer caslab90
      integer t
      integer s
      integer gnbtok
      
      t = gnbtok(token, ltoken)
      if (t == NEWLINE)
         return(t)
      if (t == MINUS) then
         s = -1
      else
         s = +1
      endif
      if (t == MINUS | t == PLUS)
         t = gnbtok(token, ltoken)
      if (t <> DIGIT & t <> ALPHA) then
         call inform('invalid case label.')
         t = COLON
         return(0)
      endif
      call putchr(token,ltoken)
                                ! get next token (should be comma or colon)
      t = gnbtok(token, ltoken)
      return(0)
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine seselect
# seselect - finish off select statement; generate dispatch code
      integer lab
      integer lb, ub, n, i, j
      integer labgen
      external labgen
include_cstat
      if (sellev <=0) then
         call warn('Unmatched endselect.')
         return
      endif
      lab = sellab(sellev)
      lb = selstak(seltop+3)
      ub = selstak(sellast-2)
      n = selstak(seltop+1)
      sellev = sellev - 1
      call outifl
      call putqs('c -- dispatch area for select')
      call outlin
      if ( n > 0 ) then
# in case the previous statement was a break or other goto, label this one
         i = labgen(1)
         call puti5(i)
         call outtab(0,0)
         call outgo(lab+1)  # terminate last case
         call outlin
      endif
      if (selstak(seltop+2) == 0)
         selstak(seltop+2) = lab + 1    # default default label
      call outcnt(lab,0,0)    # L   continue
      if (n >= CUTOFF & ub - lb + 1 < DENSITY * n ) then
# output branch table
         if (lb <> 1) then    # L  Innn=Innn-lb+1
            call outtab(0,0)
            call selvar(lab)
            code(1) = EQUALS
            call putchr(code,1)
            call selvar(lab)
            if (lb < 1) then
               code(1) = PLUS
               call putchr(code,1)
            endif
            call outnum(-lb + 1)
            call outlin
         endif
         call outtab(0,0)    #  if (Innn.lt.1.or.Innn.gt.ub-lb+1)goto default
         call putqs('if (')
         call selvar(lab)
         call putqs('.lt. 1 .or. ')
         call selvar(lab)
         call putqs('.gt.')
         call outnum(ub - lb + 1)
         call putqs(') go to ')
         call puti5(selstak(seltop+2))
         call outlin

# go to (....), Innnn
         call outtab(0,0)
         call putqs('go to (')

         j = lb
         for (i = seltop + 3, i < sellast, i = i + 3)
             for ( , j < selstak(i), j = j + 1)  # fill in vacancies
                 call outnum(selstak(seltop+2))
                 code(1) = COMMA
                 call putchr(code,1)
             endfor

             for (j = selstak(i+1) - selstak(i), j >= 0, j = j - 1)
                 call outnum(selstak(i+2))  # fill in range
                 if ((i < sellast - 3) | (j > 0)) then
                    code(1) = COMMA
                    call putchr(code,1)
                 endif
             endfor
             j = selstak(i+1) + 1
         endfor

         call putqs('), ')
         call selvar(lab)
         call outlin

      else if (n > 0) then    # output linear search form
         for (i = seltop + 3, i < sellast, i = i + 3)
             call outtab(0,0)    # if (Innn
             call putqs('if ( ')
             call selvar(lab)
             if (selstak(i) == selstak(i+1)) then
                call putqs(' .eq. ')  #   .eq....
                call outnum(selstak(i))
             else
                call putqs(' .ge. ')  #   .ge.lb.and.Innn.le.ub
                call outnum(selstak(i))
                call putqs(' .and. ')
                call selvar(lab)
                call putqs(' .le. ')
                call outnum(selstak(i+1))
             endif
             call putqs(') ')   # ) go to ....
             call outgo(selstak(i+2))
             call outlin
         endfor

         if (lab + 1 <> selstak(seltop+2)) then
            call outtab(0,0)
            call outgo(selstak(seltop+2))
            call outlin
         endif
      endif

      call outcnt(lab+1,0,0)      # L+1  continue
      call putqs('c endselect')

      sellast = seltop  # pop select stack
      seltop = selstak(seltop)

      call spit(CAFTER)

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# seselect90 - 
      
      subroutine seselect90
include_cstat
      
      if (sellev .le.0) then
         call warn('Unmatched endselect.')
         return
      endif

      sellev = sellev - 1
      call outtab(0,0)
      call putqs('end select')

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine selvar(lab)
      integer lab

      call putqs('i')
      call outnum(lab)

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# 'do' pretty print

      subroutine sdop

include_cstat

      integer t, wswid
      integer gnbtokw, toktoi
      external gnbtokw, toktoi

      doindent(level+1) = indpc

# peek ahead
      t = gnbtokw(token,ltoken,wswid)
      if (t == DIGIT) then  #Old style, user supplied label for the end
         call outtab(0,0)   # get past statement field
         call putqs('do')
         level = level + 1
         dotype(level) = OLD
         labn(level) = toktoi(token,ltoken)
         useb(level) = NO
         call outfil(wswid)
         call putchr(token,ltoken)
         call eatup(0)
      else
         call outtab(0,0)
         call putqs('do')
         level = level + 1
         dotype(level) = DOPRETTY
         if (t == COMMENT) then
            call endcomment(CAFTER, 0, token, ltoken, 0)
         else if (t == NEWLINE) then
            call outlin
         else
            call outfil(wswid)
            call putchr(token,ltoken)
            call eatup(0)
         endif
      endif

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------

# 'select' pretty print
      
      subroutine sselectp
include_cstat

      integer t, wswid
      integer gnbtokw
      external gnbtokw

      if (sellast + 3 > MAXSELECT)
         call oops('select table overflow.')
      call outtab(0,0)
      call putqs('select')
      t = gnbtokw(token,ltoken,wswid)
      call outfil(wswid)
      if (t == ESCAPE & token(2) == SCASEI) then
         call putqs('case')
      else
         call putchr(token,ltoken)
      endif

      call eatup(0)
      sellev = sellev + 1
      if (sellev > MAXDEPTH)
         call oops('select statements nested too deeply.')
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------

# 'case' pretty print
      
      subroutine scasep
include_cstat

      if (sellev <= 0) then
         call warn('illegal case or default.')
         return
      endif
      sellev = sellev - 1
      call outtab(0,0)
      call putqs('case')
      call eatup(0)
      sellev = sellev + 1

      end

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine outnum(n)
      integer n,i
      character*16 msg
      common /onc/ msg

      write(msg,100) n
 100  format(i16)

      for(i = 1 , i<16 & msg(i:i) = ' ', i=i+1)
      endfor

      call putqs(msg(i:16))

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# DOMATH - this subroutine evaluates an expression

      subroutine domath(argstk,i,j)
      integer evalone
      external evalone
      integer argstk(1),i,j
      integer ival, ierr
      integer jrem,jq,a1,a2
      integer i0,pos,k
      character*(MAXSTATE)  str

include_cmacro
include_ctype

      ierr = OK
      ival = 0
      pos = 1

# if there are too many arguments
      if (i+2 <>j) then
         call warn('Too many arguments to Evaluate macro')
         ierr=ERR

      else
         i0 = ZERO
         a1=argstk(i+2)
         a2=argstk(i+3)
         if (a2-a1 > MAXSTATE) then
            call warn('Too long an argument to Evaluate macro')
            ierr = ERR
            return
         endif

# if the string is not null, create the character string
         if (a1<>a2) then
            for (k=a1,k<a2,k=k+1)
                str(pos:pos) = char(evalst(k))
                pos=pos+1
            endfor
            str(pos: )=' '
# evaluate the string
            ival=evalone(str,ierr)
         endif
      endif

      if (ierr=ERR) then      # an error occurred
         call pbstr(evalst(a1),a2-a1)

      else                   # put the anwswer back
         jrem=abs(ival)
         if (jrem==0) then
            call putbak(i0)
            return
         endif

         while(jrem>0)
            jq=jrem/10
            call putbak(i0+jrem-jq*10)
            jrem=jq
         endwhile
         if (ival<0) then
            call putbak(MINUS)
         endif
      endif

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      function evalone(str, ierr)
#
#   This fuction returns the value of a vlaid infix integer
#   expression. If it cannot be evaluated, it returns 0
#   and ierr = ERR
#
#   extended by
#   Cathleen Benedetti
#   10-13-86
#
#   VARIABLES
#
#
include_cone

      integer evalone        # function name
      character*(*) str      # input string
      integer ierr, i23005, i23014
      integer i,j,           # delimits current token in str
      lstr,          # length of str
      tok,           # type of current token
      term,          # value of integer token
      total          # value of expression
      integer index,         # index to act1,act2
      state,nstate,  # current state,next state
      t              # temporary variable
      character*(1) action,  # current action
      nxtin    # next input
#
      integer evaltokn,stlength    # functions
      external evaltokn,stlength   # functions
#
#   ***********initialize**************
#
      total = 0
      ierr = OK
      action = 'e'
      stop = 0
      numtop = 0
      state = 2
      call evpush(state,stray,stop,ierr)
      lstr = stlength(str)

      for (i=1, (ierr = OK & action <>'a'), i = j+1)
          tok = evaltokn(str,i,j,ierr,lstr)
          if (ierr = OK) then
             call getin(tok,i,j,str,term,nxtin,index)
             action = 'e'
             while(ierr=OK & action .ne. 'a' & action .ne. 's')
                state=stray(stop)
                action=act1(state)(index:index)
                nstate=act2(state,index)
                select (ichar(action))
                   case 101: # error
                      ierr = ERR
                   case 97: #accept
                      call evpop(total, numray, numtop, ierr)
                   case 115: #shift
                      if (nxtin = '#') then
                          call evpush (term, numray, numtop, ierr)
                       else
                          t = ichar(nxtin)
                          call evpush(t,numray,numtop,ierr)
                       endif
                       call evpush (nstate, stray, stop, ierr)
                   case 114: # reduce
                      call operate (ierr, nstate, stray, stop, numray, numtop)
                      select (nstate)
                         case 2,3,4,5,6,7: state = move(stray(stop),1)
                         case 8,9,10:      state = move(stray(stop),2)
                         case 11,12,13:    state = move(stray(stop),3)
                         case 14,15:       state = move(stray(stop),4)
                         default:call oops('evalsub1:bad input state')
                      endselect
                      call evpush (state,stray, stop, ierr)
                   default:
                      call oops ('evalsub1: bad input action')
                endselect
             endwhile
          endif
      endfor

      return (total)
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      function evaltokn(str, i, j, ierr,lstr)
#
#  this function determines whether the current token
#  invalid, eof, an operator, an integer, or a variable
#
#  str      input string
#  i,j      position of token in strinteger evaltok
#  c1       integer value of current character
#
#
      integer evaltokn
      character*(*) str
      integer i,j,lstr, c1, ierr

      ierr = OK
      while ((str(i:i)=' ') & (i<=lstr))
         i=i+1
      endwhile

      if (i>lstr) return(TOKEOF)     # it's the end of the string

#  (, ), *, +, -, /
      c1 = ichar(str(i:i))
      if (c1=40|c1=41|c1=42|c1=43|c1=45|c1=47) then
         j=i
         return(TOKOPER)           # it's an operator
      elseif (c1 >= 48 & c1 <= 57) then         # integer
         for (j = i + 1, j <= lstr, j = j + 1)
             c1 = ichar(str(j:j))
             if (c1 < 48 | c1 > 57) break
         endfor
         j = j -1
         return (TOKNUM)         # it's an integer

      else
         ierr = ERR
         return (TOKEOF)            # it's a bad character
      endif

      end

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# STLENGTH - this fucntion returns the length of str

      function stlength(str)
      integer stlength,temp
      character*(*) str

      temp=len(str)

      while(str(temp:temp) = ' ')
         temp=temp-1
      endwhile

      return(temp)
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine getin(tok,i,j,str,term,nxtin,index)

      integer tok,        # type of token
      i,j,        # delimiters
      term,       # value of integer token
      index,      # index to arrays
      t           # temporary variable
      character*(*) str   # input string
      character*(1) nxtin # next input
      integer i23000

      select(tok)
         case TOKEOF:
            index=7
            nxtin = '$'
         case TOKOPER:
            index=ichar(str(i:i))-39
            nxtin=str(i:i)
         case TOKNUM:
            index=5
            nxtin = '#'
            t=i
            term=0
            while(t<=j)
               term=term*10+(ichar(str(t:t))-48)
               t=t+1
            endwhile
         default: call oops('getin:impossible token from evaltok')
      endselect

      return
      end

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# OPERATE - this subroutine performs a reduction

      subroutine operate(ierr, p, stray, stop, numray, numtop)
      integer stray(1), numray(1), stop, numtop, ierr, k, i23004, i23014
      integer first, second, temp, p, optr, value

# p corresponds to the production being used
      if (p<2 | p>15) then
         ierr = ERR

      elseif (p=2 | p=8 | p=11 | p=14) then
         call evpop(temp, stray, stop, ierr)

      elseif (p=15) then
         do k=1,3
            call evpop(temp, stray, stop, ierr)
         enddo k
         call evpop(temp, numray, numtop, ierr)
         call evpop(value, numray, numtop,ierr)
         call evpop(temp, numray, numtop, ierr)
         call evpush (value,numray,numtop,ierr)

      else
         do k=1,2
            call evpop(temp, stray, stop, ierr)
         enddo k
         call evpop(second, numray, numtop, ierr)
         call evpop(optr, numray, numtop, ierr)
         if (p=3) then
            value = -second
         else
            call evpop(temp, stray, stop, ierr)
            call evpop(first, numray, numtop, ierr)
            if (p .ne. 5 & p .ne. 7) then
               select (optr)
                  case 42: value = first * second
                  case 43: value = first + second
                  case 45: value = first - second
                  case 47: if (second <>0) then
                              value = first/second
                           else
                              call oops('evaluate macro--divide by zero')
                           endif
               endselect
            else
               call evpop(temp, numray, numtop, ierr)
               call evpop (temp, stray, stop, ierr)
               select (optr)
                  case 45: value = -first - second
                  case 43: value =  -first + second
               endselect
            endif
         endif

         call evpush (value, numray,numtop, ierr)
      endif

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# EVPOP - this function pops an integer off an integer stack

      subroutine evpop(item, stack, top, ierr)
      integer item, stack, top, ierr
      dimension stack(1)

      item = 0
      if (top>0) then
         item = stack(top)
         top = top - 1

      else
         ierr = ERR
      endif

      return
      end

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# EVPUSH - this subroutine pushes an integer onto an integer stack

      subroutine evpush(item, stack, top, ierr)
      integer item, stack, top, ierr
      dimension stack(1)

      if (top < MAXSTATE ) then
         top = top + 1
         stack(top) = item
      else
         ierr = ERR
      endif

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# DOUNDF - take definition out of table

      subroutine doundf(argstk,i,j)
      integer a1,a2,argstk(1),i,j, ilo, ihi, lname, k

include_cmacro
include_ctype

      if (j <> i+2)
         call oops('wrong number of arguments in undefine')

      a1=argstk(i+2)
      a2=argstk(i+3)

      do ilo = a1, a2-1 
         if (type(evalst(ilo))<>WHITE) break
      enddo

      do ihi = a2-1, a1, -1
         if (type(evalst(ihi))<>WHITE) break
      enddo
      lname = ihi -ilo + 1

      if (lname <=0) 
         call oops(' Empty name in Undefine macro.')

      do k = ilo, ihi
         if (alphan(evalst(k))<>YES) 
            call oops(' Name not alphanumeric in Undefine macro.')
      enddo 

      call unstal(evalst(ilo),lname)

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      subroutine dodmp(argstk,i,j)
      integer i,j,argstk(1)
      integer k,a1,a2
      integer dumpdf
      external dumpdf, dumpa
      character*80 out

include_cmacro
include_ctype

      do k = i + 2 ,j
         a1 = argstk(k)
         a2 = argstk(k+1)
         if (a2==a1) then
            call dumpa
         else
            while(type(evalst(a1)) == WHITE & a1 <a2)
               a1 = a1 + 1
            endwhile
            while(type(evalst(a2-1)) == WHITE & a1 <a2)
               a2 = a2 - 1
            endwhile
            if ( a2-a1 <=0) 
               call warn('Dumpdef: empty name')
            if ( dumpdf(a2-a1,evalst(a1)) <> 0) then
               do i=1, a2-a1
                  out(i:i) = char(evalst(a1-1+i))
               enddo
               call warn('Dumpdef: name not defined')
               call rem(out,a2-a1)
            endif
         endif
      enddo k

      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# Set either RealSize or IntSize definition.  Called whenever "realsize"
# or "intsize" is changed, to change the corresponding macros.

      subroutine setsize(name,val)
      character *(*)name
      integer val
      integer i23000
      character *1 s1
      character *2 s2

      select(val)
         case 2,4,8:
            write(s1,'(i1)') val
            call cnstal(name,s1)
         case 16:
            write(s2,'(i2)') val
            call cnstal(name,s2)
         default:
            call oops("Attempted to write bad size in setsize")
      endselect

      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# Query the hash table and find the current definition of WORDSIZE
# Fatal error if WORDSIZE is not defined

      subroutine getwdsz(ws)
      integer ws,getdef
      external getdef
      character *8 wsstr

      if (getdef('WORDSIZE',wsstr) > 0)then
         read(wsstr,'(i2)') ws
         return
      endif

      call oops("WORDSIZE is not defined!")
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# Read a definition from the hash table, leaving the string value in "val".
# Val must be long enough to store the definition value.  Return value is
# length of "val", or -1 if "def" was not in the table.

      integer function getdef(def,val)
      character *(*) def, val
      integer lookup,defp
      integer i, readdef, lnb
      external lookup,readdef, lnb
      integer idef(32),lidef,lval
      
# Measure the length of "def" and convert it to integer form
      lidef = lnb(def)
      do i=1,lidef
         idef(i) = ichar(def(i:i))
      enddo
      
      defp = lookup(lidef,idef)
      if (defp == -1) return(-1)
      
      lval = readdef(defp,val)

      return(lval)
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
      integer function lnb(s)
      character *(*) s
      integer i

      do i=len(s),1,-1
         if (s(i:i) <> ' ') break
      enddo

      return(i)
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# Remove a definition from the hash table.
      
      subroutine undef(def)
      character *(*) def
      integer i
      integer idef(32),lidef
      integer lnb
      external lnb
      
# Measure the length of "def" and convert it to integer form
      lidef = lnb(def)
      do i=1,lidef
         idef(i) = ichar(def(i:i))
      enddo
      
      call unstal(idef, lidef)
      
      return
      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
      
# Write a comment at the end of a line
# Do not break the line

      subroutine endcomment(ipos, icont, stoken, sltoken, wswid)
      
include_cfile
include_ctype
include_cstat
include_stdunits
      
      integer ipos, icont, stoken(*), sltoken, wswid
      integer i, toksiz, wswid0
      character*(MPPL_MAXCARD) msg
      integer zpakchrz, gtok
      external zpakchrz, gtok
      
      if (optlang .eq. LANG_F77) then
         if (ipos .eq. CBEFORE) then
# write comment out immediately, before statement
            toksiz = zpakchrz(msg, len(msg), stoken, sltoken)
            call wrline(stdout,msg,toksiz)
         else
# put current line, then the comment
            call outlin
            call putchr(stoken, sltoken)
         endif
         if (lastpc > 0)
            call outlin
         if (icont == 1) then
            do i=1,5
               outbuf(i) = BLANK
            enddo
            outbuf(6) = AMPERSAND
            lastpc = 6
         endif

      else if (optlang .eq. LANG_F90 | optlang .eq. LANG_IS_F90) then
# for f90, keep comment at the end of the line
# do not continue comments across lines
         if (icont .eq. 1) then
            call putqs(" &")
            wswid0 = max(0, wswid-2)
         else
            wswid0 = wswid
         endif
         
         if (colcom == -1) then
            call outfil(wswid0)
         else if (colcom > lastpc) then
            call outfil(colcom - lastpc - 1)
         endif
         
         do i=1,sltoken
            outbuf(lastpc + i) = stoken(i)
         enddo
         lastpc = lastpc + sltoken
         call outlin
         if (icont .eq. 1) then
            icontinue = 1
         endif

      else
         call outfil(wswid)
         code(1) = comchar
         call putchr(code,1)   # actual comment character used
         call putchr(stoken, sltoken)
         call outlin
      endif

      end
      
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
