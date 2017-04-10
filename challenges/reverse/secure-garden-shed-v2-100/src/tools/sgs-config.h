//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// file:    sgs-config.h
// date:    2017-01-04
// author:  paul dautry
// purpose:
//      Define shared data structures and constants
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#ifndef _SGS_CONFIG_H_
#define _SGS_CONFIG_H_

#include <stdint.h>

/* 
 * definitions must match sgs_compil_utils/sgs_config.py values ! 
 */
/* instruction codes */
#define ASM_RES  0x0
#define ASM_CPY  0x1
#define ASM_RED  0x2
#define ASM_ECH  0x3
#define ASM_EXT  0x4
#define ASM_LOD  0x5
#define ASM_AFT  0x6
#define ASM_AFTB 0x7
#define ASM_EQU  0x8
#define ASM_GTH  0x9
#define ASM_LTH  0xa
#define ASM_NOT  0xb
#define ASM_JMP  0xc
#define ASM_ADD  0xd
#define ASM_SUB  0xe
#define ASM_NOP  0xf
/* section names */ 
#define BS_SIGN ".SGS"
#define BS_DATA ".data"
#define BS_CODE ".code"
/* var types for ASM_CPY */ 
#define VT_BOOL 0x0
#define VT_INT  0x1
#define VT_CHAR 0x2
/*
 * var layouts for  
 *      ASM_EXT,
 *      ASM_AFT,
 *      ASM_EQU,
 *      ASM_GTH,
 *      ASM_LTH,
 *      ASM_NOT,
 *      ASM_ADD,
 *      ASM_SUB
 */
#define VAL_VAL 0x0
#define MEM_VAL 0x1
#define VAL_MEM 0x2
#define MEM_MEM 0x3
/* emulator types */
typedef uint8_t   unit_t;
typedef int32_t  word_t;
typedef uint32_t instr_t;
typedef uint32_t code_t;
typedef uint32_t type_t;
typedef uint32_t offset_t;
typedef int32_t  val_t;
typedef uint32_t sz_t;
typedef int32_t  pc_t;
typedef int32_t  op_t;
/* some masks */
#define CODE_MASK 0x0000000f
#define TYPE_MASK 0x00000003
#define VAL_MASK  0x00001fff
#define SIGN_MASK 0x00001000
/* helpers macros */
#define BETOLE(rinstr)    (((rinstr&0xff)<<24)|((rinstr&0xff00)<<8)|((rinstr&0xff0000)>>8)|((rinstr&0xff000000)>>24))
#define CODE(instr)      (((instr)>>28)&CODE_MASK)
#define TYPE(instr)      (((instr)>>26)&TYPE_MASK)
#define FVAL_TYPE(instr) (((instr)>>13)&VAL_MASK)
#define SVAL_TYPE(instr) ((instr)&VAL_MASK)
#define FVAL(instr)      (((instr)>>15)&VAL_MASK)
#define SVAL(instr)      (((instr)>>2)&VAL_MASK)
#define SET_SIGN(val)    ((SIGN_MASK&val)?-1:1)*(val&(~SIGN_MASK))

#define TRUE    1
#define FALSE   0

#define CHR(c) ((c<20||c>126)? '.': c)

#endif /*_SGS_CONFIG_H_*/
