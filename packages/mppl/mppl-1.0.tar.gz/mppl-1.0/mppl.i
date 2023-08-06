#parameter file for mppl
include scon.h
define TTY '-'
define NO 0
define YES 1
define FATALERROR 1
# sizes
define ARGSIZE 500
define CALLSIZE 200
define BUFSIZE 50000
define EVALSIZE 50000
define MAXDEPTH 10
define MAXSELECT 500
define MAXSTATE 125
define MAXTOK 20000
# lexical
define LEXMIN 0
define NULL 0
define COMMENT 1
define LETTER 2
define DIGIT  3
define ALPHA  4
define WHITE  5
define COL1C 6
define BELL 7
define TAB 9
define LINEFEED 10
define NEWLINE 13
define NUMBER 14
define OPERATOR 15
define LOGICAL 16
define EOS 27
define EOF 28
define BLANK 32
define BANG 33
define QUOTE 34
define POUND 35
define DOLLAR 36
define PERCENT 37
define AMPERSAND 38
define TICK 39
define LPAREN 40
define RPAREN 41
define ASTERISK 42
define PLUS 43
define COMMA 44
define MINUS 45
define PERIOD 46
define SLASH 47
define ZERO 48
define NINE 57
define COLON 58
define SEMICOLON 59
define LANGLE 60
define EQUALS 61
define RANGLE 62
define QUESTION 63
define ATSIGN 64
define LBRACK 91
define BSLASH 92
define RBRACK 93
define CARET 94
define UNDERSCORE 95
define GRAVE 96
define LBRACE 123
define VBAR 124
define RBRACE 125
define TILDE 126
define ESCAPE 127  # can't collide with normal text or flags below
define LEXMAX 127
#
# builtin flags
define DEFTYPE 65
define IFELSETYPE  66
define IFDEFTYPE   67
define ERRPRINTTYPE 68
define INFOPRINTTYPE 110
define DUMPDEFTYPE 69
define EVALUATETYPE 70
define IMMEDIATETYPE 71
define UNDEFINETYPE 72
define SMODTYPE 73
define SSETSUP 119
#
define SENDDO      74
define SBREAK      75
define SNEXT       76
define SDO         77
define SWHILE      78
define SENDWHILE   79
define SUNTIL      80
define SIF         81
define SELSE       82
define SENDIF      83
define SELSEIF     84
define STHEN       85
define SSELECT     86
define SCASE       87
define SDEFAULT    88
define SESELECT    89
define SFOR        90
define SEFOR       91
define SINCLUDE    92
define SBLOCK      93
define MPROGRAM    94
define MSUBROUTINE 95
define MFUNCTION   96
define MRETURN     97
define MEND        98
define MINTERFACE  99
define SBREAK90    100
define SNEXT90     101
define SDO90       102
define SWHILE90    103
define SENDWHILE90 104
define SUNTIL90    105
define SSELECT90   106
define SCASE90     107
define SDEFAULT90  108
define SESELECT90  109
# 110 defined above
define SDOI        111
define SSELECTI    112
define SCASEI      113
define REMARKTYPE  114
define OMPTYPE     115
define MALLOCATE   116
define MDEALLOCATE 117
define MSHAPE      118
# 119 defined above

#values for do statement types
define OLD       1
define REGULAR   2
define BLOCK     3
define WHILE     4
define REGULAR90 5
define BLOCK90   6
define WHILE90   7
define FOR90     8
define DOPRETTY  9
# select parameters
define CUTOFF 3
define DENSITY 3
# value for domath
define TOKOPER 100
define TOKEOF 101
define TOKNUM 102
define ERR 1
define OK 0
define INLINE 512

define CBEFORE 1
define CAFTER  2

define LANG_NONE   1
define LANG_F77    2
define LANG_F90    3
define LANG_IS_F77 4
define LANG_IS_F90 5

# include files
# IRSET
define(include_irset,[
        logical ireset,rreset
        common /irset/ ireset,rreset
])
# STDUNITS
define(include_stdunits,[
        integer stdin,stdout,stderr
        common /stdunits/ stdin,stdout,stderr
])
# FNAME
define(include_fname,[
        Filename std,basis,sys,system
        common /fname/ std,basis,sys,system
])
# IDIRCOM
define(include_idircom,[
        character dirsep
        Filename incldirs(200)
        integer inclnum
        common /idircom/ inclnum
        common /idircoc/ dirsep, incldirs
])
# ICOM
define(include_icom,[
        integer icompile
        common /icom/icompile
])
# PATHVARS
define(include_pathvars,[
        Filename argv0
        Filename realname
        Filename realpath
        integer len1,len2,len3
        common /cpathvars/argv0,realname,realpath
        common /ipathvars/len1,len2,len3
])
# CTLVARS
define(include_ctlvars,[
        integer lexwarn,realsize,intsize,wordsize
        integer inlev,finerr,nodblquo,yyline(MPPL_MAXINLEV)
        common /ctlvars/ lexwarn,realsize,intsize,wordsize
        common /ctlvars/ inlev,finerr,nodblquo,yyline
])
# CARGS
define(include_cargs,[
        integer ap,argstk(ARGSIZE),callst(CALLSIZE),nlb,plev(CALLSIZE)
        common /cargs/ ap,argstk,callst,nlb,plev
])
# CFILE
define(include_cfile,[
        integer iusin(MPPL_MAXINLEV),lnbt
        integer lcbuf
        common /cfile/iusin,lcbuf,lnbt

        Filename filnam(MPPL_MAXINLEV)
        common /cfilec/filnam
        logical firstfil, verbose
        common /cfiled/firstfil, verbose

        character*MPPL_MAXCARD cbuf
        character*MPPL_MAXCARD cbsav(MPPL_MAXINLEV)
        integer lcsav(MPPL_MAXINLEV)
        common /cbsav1/ lcsav
        common /cbsav2/ cbsav
        common /cinbuf/cbuf

        integer outbuf(BUFSIZE),lastpc,conpc,col72,colcom,icontinue,maxws
        integer cichar,optlang,optmacro,optpretty,indlev,optrel,hnl,
                optalloc,optnum,nonblk
        logical bckeep
        character cchar
        common /cputc/outbuf,lastpc,conpc,col72,colcom,icontinue,maxws,
          cichar,optlang,optmacro,optpretty,indlev,optrel,hnl,
          optalloc,optnum,nonblk,bckeep
        common /cputcc/ cchar

        integer bp,pblinl(MPPL_MAXINLEV)
        common /cdef/bp,pblinl

        integer pbbuf(BUFSIZE),pblins(BUFSIZE,MPPL_MAXINLEV)
        common /cdefc/pbbuf,pblins
])
# CLABS
define(include_clabs,[
        integer labnxt,laborg
        common /labg/labnxt,laborg
])
# CMACRO
define(include_cmacro,[
        integer cp                      #current call stack pointer
        integer ep                      #next free position in evalst
        integer mline(CALLSIZE),mlev(CALLSIZE)
                                        #line,file at which macro began
        common /cmacro/ cp,ep,mline,mlev

        integer evalst(EVALSIZE)        #evaluation stack
        common /cmacrc/ evalst

])
# CSTAT
define(include_cstat,[
        integer indpc,indflg
        integer level,iflevel,ifacelev
        integer dotype(0:MAXDEPTH), doindent(0:MAXDEPTH)
        integer labn(0:MAXDEPTH),labb(0:MAXDEPTH)
        integer usen(0:MAXDEPTH),useb(0:MAXDEPTH)
        integer token(MAXTOK),ltoken,code(2)
        integer modtype(0:MAXDEPTH), modfun
        character*(130) foriter(0:MAXDEPTH)
        common /stat1/indpc,indflg,level,iflevel,ifacelev
        common /stat1/dotype,doindent,labn,labb,usen,useb,token,ltoken,code,
                      modtype,modfun
        character*32 modname(0:MAXDEPTH)
        common /stat2/ modname, foriter
        integer seltop   # current select entry; init = 0
        integer sellast  # next available position; init = 1
        integer selstak  # select information
        integer sellev   # select depth
        integer sellab   # label that started this select
        common /csel/ sellev,seltop, sellast,
                        selstak(MAXSELECT),sellab(MAXDEPTH)
])
# CTYPE
define(include_ctype,[
        integer type(LEXMIN:LEXMAX)
        integer alphan(LEXMIN:LEXMAX)
        integer contu(LEXMIN:LEXMAX)
        integer comchar
        logical col1(LEXMIN:LEXMAX)
        logical col6
        common /ctype/type,alphan,contu,comchar,col1,col6
])
define(include_cone,[
        character*(8) act1     # array of actions(shift,reduce,etc)
        integer act2,          # array  of states corresponding to act1
                move,          # array of next states after reduction
                stray,stop,    # stack of states,stack top
                numray,numtop  # stack of tokens, stack top
        common /ceo/ act1(26)
        common /ceo1/ act2(26,8), move(26,4)
        common /ceo2/ stray(MAXSTATE), stop, numray(MAXSTATE), numtop
])
        block data mppldata
include_cargs
include_cfile
include_cone
include_clabs
include_cmacro
include_cstat
include_ctype
include_icom
        integer i
        data verbose/FALSE/
        data laborg/23000/
        data col72/72/
        data indlev/3/
        data colcom/-1/
####
# Debug flags
#        data optlang/LANG_F90/
#        data optmacro/NO/
#        data optpretty/NO/
#        data optrel/LANG_F77/
#        data hnl/YES/
####
        data optlang/LANG_F77/
        data optmacro/YES/
        data optpretty/YES/
        data optrel/LANG_F77/
        data hnl/NO/
	data optalloc/NO/
        data optnum/YES/
        data firstfil /TRUE/
#
# act1,act2 indexed by current state and input
# columns 1-8 correspond to: ( ) * + int - eof /
#
        data act1(1)/'eeeeeeee'/
        data act1(2)/'seeessee'/
        data act1(3)/'seeessee'/
        data act1(4)/'seeeseee'/
        data act1(5)/'errrerrr'/
        data act1(6)/'eeesesee'/
        data act1(7)/'eeeeeeae'/
        data act1(8)/'errrerrr'/
        data act1(9)/'ersrerrs'/
        data act1(10)/'eseeeeee'/
        data act1(11)/'eeesesee'/
        data act1(12)/'ersrerrs'/
        data act1(13)/'seeeseee'/
        data act1(14)/'seeeseee'/
        data act1(15)/'eeeeeeae'/
        data act1(16)/'seeeseee'/
        data act1(17)/'seeeseee'/
        data act1(18)/'errrerrr'/
        data act1(19)/'seeeseee'/
        data act1(20)/'seeeseee'/
        data act1(21)/'ersrerrs'/
        data act1(22)/'ersrerrs'/
        data act1(23)/'errrerrr'/
        data act1(24)/'errrerrr'/
        data act1(25)/'ersrerrs'/
        data act1(26)/'ersrerrs'/
        data (act2(1,i), i=1,8) /8*1/
        data (act2(2,i), i=1,8) /3,3*1,5,4,2*1/
        data (act2(3,i), i=1,8) /3,1,1,1,5,4,1,1/
        data (act2(4,i), i=1,8) /3,3*1,5,3*1/
        data (act2(5,i), i=1,8) /1,3*14,1,3*14/
        data (act2(6,i), i=1,8) /3*1,13,1,14,2*1/
        data (act2(7,i), i=1,8) /8*1/
        data (act2(8,i), i=1,8) /1,3*11,1,3*11/
        data (act2(9,i), i=1,8) /1,2,16,8,1,8,2,17/
        data (act2(10,i), i=1,8) /1,18,6*1/
        data (act2(11,i), i=1,8) /3*1,19,1,20,2*1/
        data (act2(12,i), i=1,8) /1,3,16,8,1,8,3,17/
        data (act2(13,i), i=1,8) /3,3*1,5,3*1/
        data (act2(14,i), i=1,8) /3,3*1,5,3*1/
        data (act2(15,i), i=1,8) /8*1/
        data (act2(16,i), i=1,8) /3,3*1,5,3*1/
        data (act2(17,i), i=1,8) /3,3*1,5,3*1/
        data (act2(18,i), i=1,8) /1,3*15,1,3*15/
        data (act2(19,i), i=1,8) /3,3*1,5,3*1/
        data (act2(20,i), i=1,8) /3,3*1,5,3*1/
        data (act2(21,i), i=1,8) /1,4,16,9,1,9,4,17/
        data (act2(22,i), i=1,8) /1,6,16,10,1,10,6,17/
        data (act2(23,i), i=1,8) /1,3*12,1,3*12/
        data (act2(24,i), i=1,8) /1,3*13,1,3*13/
        data (act2(25,i), i=1,8) /1,5,16,9,1,9,5,17/
        data (act2(26,i), i=1,8) /1,7,16,10,1,10,7,17/
#
# move indexed by stray(stop) and current non-terminal
# from grammar
# columns 1-4 correspond to: E  E'  T  F
#
        data (move(1,i), i=1,4) /4*1/
        data (move(2,i), i=1,4) /7,6,9,8/
        data (move(3,i), i=1,4) /10,6,9,8/
        data (move(4,i),i=1,4) /1,11,12,8/
        data (move(5,i), i=1,4) /4*1/
        data (move(6,i), i=1,4) /4*1/
        data (move(7,i), i=1,4) /4*1/
        data (move(8,i), i=1,4) /4*1/
        data (move(9,i), i=1,4) /4*1/
        data (move(10,i), i=1,4) /4*1/
        data (move(11,i), i=1,4) /4*1/
        data (move(12,i), i=1,4) /4*1/
        data (move(13,i), i=1,4) /2*1,21,8 /
        data (move(14,i), i=1,4) /2*1,22,8/
        data (move(15,i), i=1,4) /4*1/
        data (move(16,i), i=1,4) /3*1,23/
        data (move(17,i), i=1,4) /3*1,24/
        data (move(18,i), i=1,4) /4*1/
        data (move(19,i), i=1,4) /2*1,25,8/
        data (move(20,i), i=1,4) /2*1,26,8/
        data (move(21,i), i=1,4) /4*1/
        data (move(22,i), i=1,4) /4*1/
        data (move(23,i), i=1,4) /4*1/
        data (move(24,i), i=1,4) /4*1/
        data (move(25,i), i=1,4) /4*1/
        data (move(26,i), i=1,4) /4*1/
#
        end
