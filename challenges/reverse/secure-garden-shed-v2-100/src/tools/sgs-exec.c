//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// file:    sgs-exec.c
// date:    2017-01-04
// author:  paul dautry
// purpose:
//      Secure Garden Shed microprocessor emulator
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/* system includes */
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
/* personnal includes */
#include "sgs-config.h"
#include "sgs-exec.h"
/* static global variables */
static int bin_fd=-1;
static void *bin=NULL;
static off_t bin_sz=0;
static unit_t *bin_data=NULL;
static instr_t *bin_code=NULL;
static pc_t max_pc=0;
static word_t *stack=NULL;
static sz_t stack_sz=0;
static pc_t pc=0;
static int jumped=FALSE;
static int encrypted=FALSE;
/*=============================================================================
    TYPES
=============================================================================*/
typedef unsigned char _uchar;
/*=============================================================================
    PRIVATE FUNCTIONS
=============================================================================*/
/*-----------------------------------------------------------------------------
easter_egg
    Well played you found the eater egg !
-----------------------------------------------------------------------------*/
void easter_egg(void) 
{
#ifdef ENABLE_EASTER_EGG
    /*--------------------------------------------------------------------------
        CryptoFlagGenerator 
        crypto_system: xor-cbc
        flag: INSA{34573R_3995_4r3_s0_NUF!}
    --------------------------------------------------------------------------*/
    int buf_sz=32, bsize=16, i, j;
    const _uchar key[]={
        0xb1, 0x0d, 0x9a, 0x33,
        0xf7, 0xb5, 0x27, 0x19,
        0xf2, 0x1e, 0x8e, 0x13,
        0xa4, 0x6c, 0x78, 0x75 };
    _uchar iv[]={
        0x09, 0xa0, 0x6e, 0x22,
        0x93, 0xd6, 0xef, 0xba,
        0xd8, 0x97, 0x67, 0x05,
        0x4a, 0x34, 0x69, 0xa6 };
    _uchar buf[]={
        0xf1, 0xe3, 0xa7, 0x50,
        0x1f, 0x50, 0xfc, 0x96,
        0x1d, 0xba, 0xbb, 0x49,
        0xdd, 0x61, 0x28, 0xe6,
        0x1f, 0xda, 0x4f, 0x50,
        0xb7, 0x96, 0xeb, 0xd0,
        0xa1, 0xf1, 0x73, 0x7b,
        0x04, 0x0e, 0x53, 0x90 };
    _uchar c;
    /* iterate over blocks to decrypt */
    for(i=0; i<(buf_sz/bsize); ++i) {
        for(j=0; j<bsize; ++j) {
            /* decode character */
            c=(buf[i*bsize+j] ^ key[j]) ^ iv[j];
            /* prepare next iv */
            iv[j]=buf[i*bsize+j];
            /* write decoded char on buf */
            buf[i*bsize+j]=c;
        }
    }
    /* unpad PKCS#7 */
    i=(int)(buf[buf_sz-1]);
    for(j=0; j<i; ++j) {
        buf[buf_sz-1-j]=0;
    }
    /* print flag */
    for(i=0; i<buf_sz; ++i) {
        if (buf[i]==0) {
            putchar('\n');
            break;
        }
        putchar(buf[i]);
    }
#endif /* ENABLE_EASTER_EGG */
}
/*-----------------------------------------------------------------------------
decrypt
    
-----------------------------------------------------------------------------*/
int decrypt(int c_off, int d_off)
{
    int err, key_sz, i;
    unit_t *bin_key_it, *bin_data_it;
    key_sz=c_off-(strlen(BS_SIGN)+1);
    if (c_off<=0) {
        err=-21; goto abrt;
    }
    bin_key_it=bin+strlen(BS_SIGN)+1;
    bin_data_it=bin+d_off+strlen(BS_DATA);
    for (i=0; i<bin_sz-(d_off+strlen(BS_DATA)); ++i) {
        bin_data_it[i]^=bin_key_it[i%key_sz];
    }
    /* success */
    err=0;
abrt:
    return err;
}
/* entry point */
int main(int argc, char **argv)
{
    PRINT_DBG("in: main\n");
    int err;
    if (argc!=2) {
        usage();
        goto done;
    }
    if ((err=init(argv[1]))!=0) {
        goto abrt;
    }
    if ((err=run())!=0) {
        goto abrt;
    }
    /* success */
done:
    err=EXIT_SUCCESS;
abrt:
    if (err!=EXIT_SUCCESS) {
        print_err(err);
    }
    term();
    exit(err);
}
/*=============================================================================
    PUBLIC FUNCTIONS
=============================================================================*/
/*-----------------------------------------------------------------------------
parse_bin
    Parse binary and setup internal variables to allow run
-----------------------------------------------------------------------------*/
int init(const char *filename)
{
    PRINT_DBG("in: init(filename=<%s>)\n", filename);
    int err;
    struct stat sb;
    if ((bin_fd=open(filename, O_RDONLY))<0) {
        err=-1; goto abrt;
    }
    if (fstat(bin_fd, &sb)==-1) {
        err=-2; goto abrt;
    }
    bin_sz=sb.st_size;
    bin=mmap(NULL, bin_sz, PROT_READ|PROT_WRITE, MAP_PRIVATE, bin_fd, 0);
    if (bin==MAP_FAILED) {
        err=-3; goto abrt;
    }
    if ((err=check_integrity())!=0) {
        goto abrt;
    }
    if ((err=prepare_sections())!=0) {
        goto abrt;
    }
    err=0;
abrt:
    return err;
}
/*-----------------------------------------------------------------------------
check_integrity
    Verify program integrity
-----------------------------------------------------------------------------*/
int check_integrity(void)
{
    PRINT_DBG("in: check_integrity\n");
    int err, i;
    char *sign=BS_SIGN;
    char *tab=bin;
    /* check signature */
    for (i=0; i<strlen(BS_SIGN); ++i) {
        if (tab[i]!=sign[i]) {
            err=-4; goto abrt;
        }
    }
    if (tab[strlen(BS_SIGN)]=='E') {
        PRINT_DBG("binary data section is encrypted\n");
        encrypted=TRUE;
    }
    /* verify MD5 checksum */
    /// \todo https://tools.ietf.org/html/rfc1321
    err=0;
abrt:
    return err;
}
/*-----------------------------------------------------------------------------
prepare_sections
    Initialize variables related to data section and code section
-----------------------------------------------------------------------------*/
int prepare_sections(void)
{
    PRINT_DBG("in: prepare_sections\n");
    int err, d_off, c_off, len;
    c_off=find(BS_CODE, bin, bin_sz);
    d_off=find(BS_DATA, bin, bin_sz);
    len=d_off-(c_off+strlen(BS_CODE));
    if (d_off<0) {
        err=-5; goto abrt;
    }
    if (c_off<0) {
        err=-6; goto abrt;
    }
    if (len%4!=0) {
        err=-15; goto abrt;
    }
    /* success */
    bin_data=bin+d_off+strlen(BS_DATA);
    bin_code=bin+c_off+strlen(BS_CODE);
    max_pc=len/4;
    if (encrypted!=FALSE) {
        if ((err=decrypt(c_off, d_off))!=0) {
            goto abrt;
        }
    }
    PRINT_DBG("4 first bytes of data: %#02x %#02x %#02x %#02x\n", bin_data[0], bin_data[1], bin_data[2], bin_data[3]);
    PRINT_DBG("4 first instructions of code: %#08x %#08x %#08x %#08x\n", bin_code[0], bin_code[1], bin_code[2], bin_code[3]);
    PRINT_DBG("data section at %#08x (length=%lu)\n", d_off, bin_sz-(d_off+strlen(BS_DATA)));
    PRINT_DBG("code section at %#08x (length=%d) -> max_pc=%04d\n", c_off, len, max_pc);
    err=0;
abrt:
    return err;
}
/*-----------------------------------------------------------------------------
run
    Run the program
-----------------------------------------------------------------------------*/
int run(void)
{
    PRINT_DBG("in: run\n");
    int err;
    instr_t instr;
    pc=0;
    jumped=FALSE;
    while (pc<max_pc) {
#ifdef DEBUG_EXEC_STEP_BY_STEP
        printf("pc is %d, press <enter> to continue or 'q' to exit.\n", pc);
        char c=getchar();
        if (c=='q') {
            err=0; goto abrt;
        }
#endif /* DEBUG_EXEC_STEP_BY_STEP */
        instr=BETOLE(bin_code[pc]);
        if ((err=exec_instr(instr))!=0) {
            goto abrt;
        }
        if (jumped==FALSE) {
            pc++;
        } else {
            jumped=FALSE;
        }
    }
    /* success */
    err=0;
abrt:
    return err;
}
/*-----------------------------------------------------------------------------
term
    Terminates the program after cleaning up memory
-----------------------------------------------------------------------------*/
void term(void)
{
    PRINT_DBG("in: term\n");
    if (stack!=NULL) {
        free(stack);
    }
    bin_code=NULL;
    bin_data=NULL;
    if (bin!=NULL) {
        if (munmap(bin, bin_sz)==-1) {
            printf("Cleanup failure: munmap failed! (expect memory leaks)\n"
                   "Continuing cleanup.");
        }
        bin=NULL;
        bin_sz=0;
    }
    if (bin_fd>=0) {
        if (close(bin_fd)==-1) {
            printf("Cleanup failure: close failed!\nContinuing cleanup.");   
        }
        bin_fd=-1;
    }
}
/*-----------------------------------------------------------------------------
exec_instr
    Execute an instruction
-----------------------------------------------------------------------------*/
int exec_instr(instr_t instr)
{
    PRINT_DBG("in: exec_instr(instr=%#08x)\n", instr);
    int err;
    code_t code;
    code=CODE(instr);
    PRINT_DBG("instr hex is %#08x\n", instr);
    switch (code) {
        case ASM_RES:
            if ((err=asm_res(instr))!=0) { goto abrt; }
            break;
        case ASM_CPY:
            if ((err=asm_cpy(instr))!=0) { goto abrt; }
            break;
        case ASM_RED:
            if ((err=asm_red(instr))!=0) { goto abrt; }
            break;
        case ASM_ECH:
            if ((err=asm_ech(instr))!=0) { goto abrt; }
            break;
        case ASM_EXT:
            if ((err=asm_ext(instr))!=0) { goto abrt; }
            break;
        case ASM_LOD:
            if ((err=asm_lod(instr))!=0) { goto abrt; }
            break;
        case ASM_AFT:
            if ((err=asm_aft(instr))!=0) { goto abrt; }
            break;
        case ASM_AFTB:
            easter_egg();
            break;
        case ASM_EQU:
            if ((err=asm_equ(instr))!=0) { goto abrt; }
            break;
        case ASM_GTH:
            if ((err=asm_gth(instr))!=0) { goto abrt; }
            break;
        case ASM_LTH:
            if ((err=asm_lth(instr))!=0) { goto abrt; }
            break;
        case ASM_NOT:
            if ((err=asm_not(instr))!=0) { goto abrt; }
            break;
        case ASM_JMP:
            if ((err=asm_jmp(instr))!=0) { goto abrt; }
            break;
        case ASM_ADD:
            if ((err=asm_add(instr))!=0) { goto abrt; }
            break;
        case ASM_SUB:
            if ((err=asm_sub(instr))!=0) { goto abrt; }
            break;
        case ASM_NOP:
            PRINT_INSTR("nop");
            break; /* nothing to do, it's a nop */
        default:
            err=-7; goto abrt;
    }
#ifdef DEBUG
#   ifndef DEBUG_NO_STACK
    print_stack();
#   endif
#endif
    err=0;
abrt:
    return err;
}
/*-----------------------------------------------------------------------------
usage
    Display program help
-----------------------------------------------------------------------------*/
void usage(void)
{
    printf("usage: ./sgs-exec <file>\n");
}
/*-----------------------------------------------------------------------------
print_err
    Display program error
-----------------------------------------------------------------------------*/
void print_err(int err)
{
    printf("! error: ");
    switch (err) {
        case -1:
            printf("open failed on the given file!"); break;
        case -2:
            printf("fstat failed on the given file!"); break;
        case -3:
            printf("mmap failed on the given file!"); break;
        case -4:
            printf("SGS signature not found!"); break;
        case -5:
            printf("data marker not found!"); break;
        case -6:
            printf("code marker not found!"); break;
        case -7:
            printf("unknown instruction code!"); break;
        case -8:
            printf("max stack size exceeded!"); break;
        case -9:
            printf("calloc failed to allocate memory!"); break;
        case -10:
            printf("aft instruction with value as destination!"); break;
        case -11:
            printf("unknown instruction type!"); break;
        case -12:
            printf("invalid expect value!"); break;
        case -13:
            printf("invalid operand number!"); break;
        case -14:
            printf("expected-type violation!"); break;
        case -15:
            printf("something's wrong about code section size (should be multiple of 4)!"); break;
        case -16:
            printf("memory access violation (out of stack boundaries)!"); break;
        case -17:
            printf("unknown type to cpy!"); break;
        case -18:
            printf("memory access violation (out of binary boundaries)!"); break;
        case -19:
            printf("multiple stack allocation!"); break;
        case -20:
            printf("invalid padding in data section!"); break;
        case -21:
            printf("decryption key is missing!"); break;
        case 1:
            printf("not implemented."); break;
        default:
            printf("unhandled error (%d)", err); 
            break;
    }
    printf("\n");
}
/*-----------------------------------------------------------------------------
find
    find offset of first occurence of a string or return -1 if not found
-----------------------------------------------------------------------------*/
int find(const char *search, const char *in, int in_sz)
{
    PRINT_DBG("in: find(search=<%s>, in=%p, in_sz=%d)\n", search, in, in_sz);
    int i, j, l, found;
    l=strlen(search);
    for (i=0; i<in_sz; ++i) {
        for (j=0; j<l; ++j) {
            found=1;
            if (in[i+j]!=search[j]) {
                found=0;
                break;
            }
        }
        if (found) {
            goto end;
        }
    }
    i=-1;
end:
    return i;
}
/*-----------------------------------------------------------------------------
asm functions:
    asm_res  size                              : no ret
    asm_cpy  type bin_oft stack_oft            : no ret
    asm_red  stack_oft                         : (ret>=0 if ok else ret<0) in @stack_oft
    asm_ech  stack_oft                         : no ret
    asm_ext  (stack_oft|val)                   : no ret
    asm_lod  stack_oft val                     : ret in rR
    asm_aft  (stack_oft|val) stack_oft         : no ret
    asm_aftb (stack_oft|val) stack_oft         : no ret
    asm_equ  (stack_oft|val) (stack_oft|val)   : no ret, set rF
    asm_gth  (stack_oft|val) (stack_oft|val)   : no ret, set rF
    asm_lth  (stack_oft|val) (stack_oft|val)   : no ret, set rF 
    asm_not  (stack_oft|val)                   : no ret, set rF
    asm_jmp  val                               : no ret, set pc
    asm_add  (stack_oft|val) (stack_oft|val)   : ret in rR, set rF
    asm_sub  (stack_oft|val) (stack_oft|val)   : ret in rR, set rF
-----------------------------------------------------------------------------*/
int asm_res(instr_t instr) 
{
    PRINT_DBG("in: asm_res(instr=%#08x)\n", instr);
    int err;
    stack_sz=FVAL(instr);
    PRINT_INSTR("res %#08x", stack_sz);
#ifndef DEBUG_NO_EXEC
    if (stack_sz>(1<<13)) {
        err=-8; goto abrt;
    }
    while (stack_sz%4!=0) {
        stack_sz++;
    }
    if (stack!=NULL) {
        err=-19; goto abrt;
    }
    stack=(word_t*)calloc(sizeof(unit_t), stack_sz);
    if (stack==NULL) {
        err=-9; goto abrt;
    }
#endif
    /* success */
    err=0;
abrt:
    return err;
}
int asm_cpy(instr_t instr)
{
    PRINT_DBG("in: asm_cpy(instr=%#08x)\n", instr);
    int err;
    type_t type;
    offset_t bin_oft, stack_oft, oft;
    type=TYPE(instr);
    bin_oft=FVAL_TYPE(instr);
    stack_oft=SVAL_TYPE(instr);
    PRINT_INSTR("cpy %#08x bin@%#08x stack@%#08x", type, bin_oft, stack_oft);
#ifndef DEBUG_NO_EXEC
    switch (type) {
        case VT_BOOL:
            if ((err=cpy_bool(bin_oft, stack_oft))!=0) { goto abrt; }
            break;
        case VT_INT:
            if ((err=cpy_int(bin_oft, stack_oft))!=0) { goto abrt; }
            break;
        case VT_CHAR:
            if ((err=cpy_char(bin_oft, stack_oft))!=0) { goto abrt; }
            break;
        default:
            err=-17; goto abrt;
    }
#endif /* DEBUG */
    /* success */
    err=0;
abrt:
    return err;
}
int asm_red(instr_t instr)
{
    PRINT_DBG("in: asm_red(instr=%#08x)\n", instr);
    int err, c;
    offset_t stack_oft;
    unit_t *stack_it=(unit_t*)(stack);
    unit_t u;
    stack_oft=FVAL(instr);
    PRINT_INSTR("red stack@%#08x", stack_oft);
#ifndef DEBUG_NO_EXEC
    ASSERT_MEM_ACCESS_VIOLATION(stack_oft);
    c=getchar();
    if (c<0x61||c>0x7a) { // allowed input charset is [a-z] only
        u=0;
        SET_RR(FALSE);
    } else {
        u=(unit_t)(c);
        SET_RR(TRUE);
    }
    stack_it[stack_oft]=u;
#endif /* DEBUG */
    /* success */
    err=0;
abrt:
    return err;
}
int asm_ech(instr_t instr)
{
    PRINT_DBG("in: asm_ech(instr=%#08x)\n", instr);
    int err;
    offset_t stack_oft;
    unit_t *stack_it=(unit_t*)(stack);
    stack_oft=FVAL(instr);
    PRINT_INSTR("ech stack@%#08x", stack_oft);
#ifndef DEBUG_NO_EXEC
    while (stack_it[stack_oft]!='\0') {
        putchar(stack_it[stack_oft]);
        stack_oft++;
        ASSERT_MEM_ACCESS_VIOLATION(stack_oft);    
    }
    putchar('\n');
#endif /* DEBUG */
    /* success */
    err=0;
abrt:
    return err;
}
int asm_ext(instr_t instr)
{
    PRINT_DBG("in: asm_ext(instr=%#08x)\n", instr);
    int err;
    op_t fop;
    if ((err=prepare_operand(instr, &fop, 1, 0))!=0) { goto abrt; }
    PRINT_INSTR("ext %#08x", fop);
#ifndef DEBUG_NO_EXEC
    term();
    exit(fop);
#endif /* DEBUG */
    /* success */
    err=0;
abrt:
    return err;
}
int asm_lod(instr_t instr)
{
    PRINT_DBG("in: asm_lod(instr=%#08x)\n", instr);
    int err;
    op_t sop;
    offset_t soft;
    unit_t *stack_it=(unit_t*)(stack);
    soft=FVAL_TYPE(instr);
    if ((err=prepare_operand(instr, &sop, 2, 0))!=0) { goto abrt; }
    PRINT_INSTR("lod stack@%#08x %#08x", soft, sop);
#ifndef DEBUG_NO_EXEC
    soft+=sop;
    ASSERT_MEM_ACCESS_VIOLATION(soft);
    SET_RR(stack_it[soft]);
#endif /* DEBUG */
    /* success */
    err=0;
abrt:
    return err;
}
int asm_aft(instr_t instr)
{
    PRINT_DBG("in: asm_aft(instr=%#08x)\n", instr);
    int err;
    op_t fop;
    offset_t stack_oft;
    if ((err=prepare_operand(instr, &fop, 1, 0))!=0) { goto abrt; }
    stack_oft=SVAL_TYPE(instr);
    PRINT_INSTR("aft %#08x %#08x", fop, stack_oft);
#ifndef DEBUG_NO_EXEC
    ASSERT_MEM_ACCESS_VIOLATION(stack_oft);
    stack[stack_oft/4]=fop;
#endif /* DEBUG */
    /* success */
    err=0;
abrt:
    return err;
}
int asm_aftb(instr_t instr)
{
    PRINT_DBG("in: asm_aftb(instr=%#08x)\n", instr);
    int err;
    op_t fop;
    offset_t stack_oft;
    unit_t *stack_it=(unit_t*)(stack);
    if ((err=prepare_operand(instr, &fop, 1, 0))!=0) { goto abrt; }
    stack_oft=SVAL_TYPE(instr);
    PRINT_INSTR("aft.b %#08x %#08x", fop, stack_oft);
#ifndef DEBUG_NO_EXEC
    ASSERT_MEM_ACCESS_VIOLATION(stack_oft);
    stack_it[stack_oft]=(unit_t)(fop&0xff);
#endif /* DEBUG */
    /* success */
    err=0;
abrt:
    return err;
}
int asm_equ(instr_t instr)
{
    PRINT_DBG("in: asm_equ(instr=%#08x)\n", instr);
    int err;
    op_t fop, sop;
    if ((err=prepare_operand(instr, &fop, 1, 0))!=0) { goto abrt; }
    if ((err=prepare_operand(instr, &sop, 2, 0))!=0) { goto abrt; }
    PRINT_INSTR("equ %#08x %#08x", fop, sop);
#ifndef DEBUG_NO_EXEC
    SET_RF((fop&0xff)==(sop&0xff)? TRUE: FALSE);
#endif /* DEBUG */
    /* success */
    err=0;
abrt:
    return err;
}
int asm_gth(instr_t instr)
{
    PRINT_DBG("in: asm_gth(instr=%#08x)\n", instr);
    int err;
    op_t fop, sop;
    if ((err=prepare_operand(instr, &fop, 1, 0))!=0) { goto abrt; }
    if ((err=prepare_operand(instr, &sop, 2, 0))!=0) { goto abrt; }
    PRINT_INSTR("gth %#08x %#08x", fop, sop);
#ifndef DEBUG_NO_EXEC
    SET_RF(fop>sop? TRUE: FALSE);
#endif /* DEBUG */
    /* success */
    err=0;
abrt:
    return err;
}
int asm_lth(instr_t instr)
{
    PRINT_DBG("in: asm_lth(instr=%#08x)\n", instr);
    int err;
    op_t fop, sop;
    if ((err=prepare_operand(instr, &fop, 1, 0))!=0) { goto abrt; }
    if ((err=prepare_operand(instr, &sop, 2, 0))!=0) { goto abrt; }
    PRINT_INSTR("lth %#08x %#08x", fop, sop);
#ifndef DEBUG_NO_EXEC
    SET_RF(fop<sop? TRUE: FALSE);
#endif /* DEBUG */
    /* success */
    err=0;
abrt:
    return err;
}
int asm_not(instr_t instr)
{
    PRINT_DBG("in: asm_not(instr=%#08x)\n", instr);
    int err;
    op_t fop;
    if ((err=prepare_operand(instr, &fop, 1, 0))!=0) { goto abrt; }
    PRINT_INSTR("not %#08x", fop);
#ifndef DEBUG_NO_EXEC
    SET_RF(fop==FALSE? TRUE: FALSE);
#endif /* DEBUG */
    /* success */
    err=0;
abrt:
    return err;
}
int asm_jmp(instr_t instr)
{
    PRINT_DBG("in: asm_jmp(instr=%#08x)\n", instr);
    int err;
    val_t val;
    val=FVAL(instr);
    val=SET_SIGN(val);
    PRINT_INSTR("jmp %d", val);
#ifndef DEBUG_NO_EXEC
    if (TEST_RF()) {
        pc+=val;
        jumped=TRUE;
    }
#endif /* DEBUG_NO_EXEC */
    /* success */
    err=0;
abrt:
    return err;
}
int asm_add(instr_t instr)
{
    PRINT_DBG("in: asm_add(instr=%#08x)\n", instr);
    int err;
    op_t fop, sop;
    if ((err=prepare_operand(instr, &fop, 1, 0))!=0) { goto abrt; }
    if ((err=prepare_operand(instr, &sop, 2, 0))!=0) { goto abrt; }
    PRINT_INSTR("add %#08x %#08x", fop, sop);
#ifndef DEBUG_NO_EXEC
    SET_RR(fop+sop);
#endif /* DEBUG */
    /* success */
    err=0;
abrt:
    return err;
}
int asm_sub(instr_t instr)
{
    PRINT_DBG("in: asm_sub(instr=%#08x)\n", instr);
    int err;
    op_t fop, sop;
    if ((err=prepare_operand(instr, &fop, 1, 0))!=0) { goto abrt; }
    if ((err=prepare_operand(instr, &sop, 2, 0))!=0) { goto abrt; }
    PRINT_INSTR("sub %#08x %#08x", fop, sop);
#ifndef DEBUG_NO_EXEC
    SET_RR(fop-sop);
#endif /* DEBUG */
    /* success */
    err=0;
abrt:
    return err;
}
/*-----------------------------------------------------------------------------
prepare_operand

-----------------------------------------------------------------------------*/
int prepare_operand(instr_t instr, op_t *op, int n, int expect)
{
    PRINT_DBG("in: prepare_operand(instr=%#08x, op=%p, n=%d, expect=%d)\n", instr, op, n, expect);
    int err;
    type_t type;
    unit_t *stack_it=(unit_t*)(stack);
    word_t word;
    if (expect<0||expect>2) {
        err=-12; goto abrt;
    }
    if (n<1||n>2) {
        err=-13; goto abrt;
    }
    n--;
    type=TYPE(instr);
    if (type<0||type>3) {
        err=-11; goto abrt;   
    }
    if (n==0) {
        (*op)=FVAL_TYPE(instr);
    } else {
        (*op)=SVAL_TYPE(instr);
    }
    if ((type>>n)&0x01) { /* offset */
        if ((((~expect)&0x03)&ASSERT_VALUE)==0) {
            err=-14; goto abrt;
        }
#ifndef DEBUG_NO_EXEC
        PRINT_DBG("reading from stack @ %#08x\n", *op);
        word=0;
        word|=(word_t)(stack_it[(*op)+3])<<24;
        word|=(word_t)(stack_it[(*op)+2])<<16;
        word|=(word_t)(stack_it[(*op)+1])<<8;
        word|=(word_t)(stack_it[(*op)]);
        (*op)=word;
#else
        (*op)=0x00000abc;
#endif
    } else { /* value */
        if ((((~expect)&0x03)&ASSERT_OFFSET)==0) {
            err=-14; goto abrt;
        }
        (*op)=SET_SIGN(*op);
        PRINT_DBG("value is: %d\n", *op);
    }
    /* success */
    PRINT_DBG("operand value is: %#08x\n", *op);
    err=0;
abrt:
    return err;
}
/*-----------------------------------------------------------------------------
copy functions:
    cpy_bool
    cpy_int
    cpy_char
-----------------------------------------------------------------------------*/
int cpy_bool(offset_t bin_oft, offset_t stack_oft)
{
    PRINT_DBG("in: cpy_bool(bin_oft=%d, stack_oft=%d)\n", bin_oft, stack_oft);
    int err, i;
    /// \todo stop when 0b11 reached (test lsb only)
    unit_t *stack_it=(unit_t*)(stack);
    offset_t boft, soft;
    unit_t byte, tbyte, fbit, stop;
    boft=(bin_oft/8)-1;
    soft=stack_oft-1;
    stop=0;
    for(;;) {
        boft++;
        ASSERT_BIN_ACCESS_VIOLATION(boft);
        byte=bin_data[boft];
        for (i=0; i<4; ++i) {
            soft++;
            ASSERT_MEM_ACCESS_VIOLATION(soft);
            tbyte=byte>>(6-(i*2));
            fbit=(tbyte&0x2);
            stop=((tbyte&0x1)>0? TRUE: FALSE);
            PRINT_DBG("byte is %#02x\n\ttbyte is %#02x\n\t\tfbit is %#02x\n\t\tstop is %#02x\n", 
                byte, tbyte, fbit, stop);
            if (stop!=FALSE) {
                break;
            }
            if ((boft*8+(6-(i*2)))>bin_oft) {
                PRINT_DBG("copying bool: %d\n", fbit>0? TRUE: FALSE);
                stack_it[soft]=(fbit>0? TRUE: FALSE);
            }
        }
        if (stop!=FALSE) {
            break;
        }
    }
    err=0;
abrt:
    return err;
}
int cpy_int(offset_t bin_oft, offset_t stack_oft)
{
    PRINT_DBG("in: cpy_int(bin_oft=%d, stack_oft=%d)\n", bin_oft, stack_oft);
    int err;
    word_t i;
    word_t *bin_data_it;
    offset_t boft, soft;
    if (bin_oft%8!=0) {
        err=-20; goto abrt;
    }
    bin_data_it=(word_t*)(bin_data+(bin_oft/8));
    boft=-1;
    soft=stack_oft-1;
    for (;;) {
        boft++;
        soft++;
        ASSERT_BIN_ACCESS_VIOLATION(boft);
        ASSERT_MEM_ACCESS_VIOLATION(soft);
        i=bin_data_it[boft];
        i=BETOLE(i);
        if (i==0xffffffff) {
            break;
        }
        PRINT_DBG("copying int: %#08x\n", i);
        stack[soft]=i;
    }
    err=0;
abrt:
    return err;
}
int cpy_char(offset_t bin_oft, offset_t stack_oft)
{
    PRINT_DBG("in: cpy_char(bin_oft=%d, stack_oft=%d)\n", bin_oft, stack_oft);
    int err;
    unit_t *stack_it=(unit_t*)(stack);
    offset_t boft, soft;
    if (bin_oft%8!=0) {
        err=-20; goto abrt;
    }
    boft=(bin_oft/8)-1;
    soft=stack_oft-1;
    do {
        boft++;
        soft++;
        ASSERT_BIN_ACCESS_VIOLATION(boft);
        ASSERT_MEM_ACCESS_VIOLATION(soft);
        PRINT_DBG("copying char: %#02x\n", bin_data[boft]);
        stack_it[soft]=bin_data[boft];
    } while (bin_data[boft]!='\0');
    /* success */
    err=0;
abrt:
    return err;
}

/*-----------------------------------------------------------------------------
print_stack

-----------------------------------------------------------------------------*/
void print_stack(void)
{
    int i;
    unit_t *stack_it=(unit_t*)(stack);
    if (stack!=NULL) {
        PRINT_DBG("---------- stack ----------\n");
        for (i=0; i<(stack_sz/4); ++i) {
            PRINT_DBG("%08d: %02x %02x %02x %02x ", i*4, stack_it[i*4], stack_it[i*4+1], stack_it[i*4+2], stack_it[i*4+3]);
            PRINT_DBG("|%c%c%c%c|\n", CHR(stack_it[i*4]), CHR(stack_it[i*4+1]), CHR(stack_it[i*4+2]), CHR(stack_it[i*4+3]));
        }
        PRINT_DBG("---------------------------\n");
    } else {
        PRINT_DBG("stack=(null)\n");
    }
}
