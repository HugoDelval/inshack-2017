//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// file:    sgs-exec.h
// date:    2017-01-04
// author:  paul.dautry
// purpose:
//
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#ifndef _SGS_EXEC_H_
#define _SGS_EXEC_H_

#ifdef DEBUG
#   define PRINT_DBG(...) fprintf(stderr, __VA_ARGS__)
#   define PRINT_INSTR(...)                                                   \
        PRINT_DBG("instr (pc=%04d): ", pc);                                   \
        PRINT_DBG(__VA_ARGS__);                                               \
        PRINT_DBG("\n")
#else /* DEBUG */        
#   define PRINT_DBG(...)
#   define PRINT_INSTR(...)
#endif /* DEBUG */
/*  */
//      ASSERT_ALL    0x00 // 0b00
#define ASSERT_OFFSET 0x01 // 0b01
#define ASSERT_VALUE  0x02 // 0b10
/* special registers setters */
#define SET_RR(val) stack[0]=(val)
#define SET_RF(val) stack[1]=(val)
#define GET_RR() (stack[0])
#define GET_RF() (stack[1])
#define TEST_RF() (GET_RF()!=0)

#define ASSERT_MEM_ACCESS_VIOLATION(oft)                                      \
    if (oft<0||oft>stack_sz) {                                                \
        PRINT_DBG("trying to access stack at %#08x\n", oft);                  \
        err=-16; goto abrt;                                                   \
    }
#define ASSERT_BIN_ACCESS_VIOLATION(oft)                                      \
    if (oft<0||oft>bin_sz) {                                                  \
        PRINT_DBG("trying to access binary at %#08x\n", oft);                 \
        err=-18; goto abrt;                                                   \
    }
/*-----------------------------------------------------------------------------
init
    Parse binary and setup internal variables to allow run
-----------------------------------------------------------------------------*/
int init(const char *filename);
/*-----------------------------------------------------------------------------
check_integrity
    Verify program integrity
-----------------------------------------------------------------------------*/
int check_integrity(void);
/*-----------------------------------------------------------------------------
prepare_sections
    Initialize variables related to data section and code section
-----------------------------------------------------------------------------*/
int prepare_sections(void);
/*-----------------------------------------------------------------------------
run
    Run the program
-----------------------------------------------------------------------------*/
int run(void);
/*-----------------------------------------------------------------------------
term
    Terminates the program after cleaning up memory
-----------------------------------------------------------------------------*/
void term(void);
/*-----------------------------------------------------------------------------
exec_instr
    Execute an instruction
-----------------------------------------------------------------------------*/
int exec_instr(instr_t instr);
/*-----------------------------------------------------------------------------
usage
    Display program help
-----------------------------------------------------------------------------*/
void usage(void);
/*-----------------------------------------------------------------------------
print_err
    Display program error
-----------------------------------------------------------------------------*/
void print_err(int err);
/*-----------------------------------------------------------------------------
find
    find offset of first occurence of a string or return -1 if not found
-----------------------------------------------------------------------------*/
int find(const char *search, const char *in, int in_sz);
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
int asm_res(instr_t instr);
int asm_cpy(instr_t instr);
int asm_red(instr_t instr);
int asm_ech(instr_t instr);
int asm_ext(instr_t instr);
int asm_lod(instr_t instr);
int asm_aft(instr_t instr);
int asm_aftb(instr_t instr);
int asm_equ(instr_t instr);
int asm_gth(instr_t instr);
int asm_lth(instr_t instr);
int asm_not(instr_t instr);
int asm_jmp(instr_t instr);
int asm_add(instr_t instr);
int asm_sub(instr_t instr);
/*-----------------------------------------------------------------------------
prepare_operand
    
-----------------------------------------------------------------------------*/
int prepare_operand(instr_t instr, op_t *op, int n, int expect);
/*-----------------------------------------------------------------------------
copy functions:
    cpy_bool
    cpy_int
    cpy_char
-----------------------------------------------------------------------------*/
int cpy_bool(offset_t bin_oft, offset_t stack_oft);
int cpy_int(offset_t bin_oft, offset_t stack_oft);
int cpy_char(offset_t bin_oft, offset_t stack_oft);
/*-----------------------------------------------------------------------------
print_stack

-----------------------------------------------------------------------------*/
void print_stack(void);

#endif /*_SGS_EXEC_H_*/
