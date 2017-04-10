# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    sgs_config.py
# date:    2017-01-06
# author:  paul dautry
# purpose:
#       Classe de configuration du format SGS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SGSConfig(object):
    # global constants
    MAX_INT_32 = (2**31)-1
    MAX_SGS_UINT = (2**13)
    MAX_SGS_INT = (2**12)-1
    # SGS language elements
    # -- Language Keywords
    LK_WHILE = 'while'
    LK_IF    = 'if'
    LK_END   = 'end'
    LK_TAB   = 'tab'
    BLOC_KEYWORDS = [
        LK_IF, LK_WHILE
    ]
    # -- Built-In Functions
    BIF_READ  = 'read'
    BIF_ECHO  = 'echo'
    BIF_EXIT  = 'exit'
    # -- OPerators
    OP_ADD   = 'add'
    OP_SUB   = 'sub'
    OP_LOAD  = 'load'
    OP_AFCT  = 'affect'
    # -- Code Section Types
    CST_INST = 'instruction'
    CST_BLOC = 'bloc'
    # -- SCript Section
    SCS_OPT  = '.options'
    SCS_VAR  = '.vardecl'
    SCS_SCR  = '.script'
    # -- SYMbols
    SYM_ADD  = '+'
    SYM_SUB  = '-'
    SYM_LOAD = '['
    SYM_AFCT = '->'
    SYM_LTH  = '<'
    SYM_LTE = '<='
    SYM_GTH  = '>'
    SYM_GTE = '>='
    SYM_NOT  = '!'
    SYM_EQU  = '=='
    SYM_NEQ  = '!='
    SYM_COM  = '#'
    SYM_SCT  = '.'
    SYM_SEP  = ':'
    SYM_PSEP = ' '
    SYM_VSEP = ','
    SYM_SBND = '"'
    SUB_OPS = [
        SYM_ADD,
        SYM_SUB,
        SYM_LOAD,
        SYM_PSEP
    ]
    # SGS ASM
    # -- Special Vars
    SV_RR    = 'rR'
    SV_RF    = 'rF'
    # -- Var Types
    VT_REG   = 'reg'
    VT_BOOL  = 'bool'
    VT_INT   = 'int'
    VT_CHAR  = 'char'
    BOOL_VALUES = ['true','false']
    # -- instruction names
    ASM_RES     = 'RES'
    ASM_CPY     = 'CPY'
    ASM_RED     = 'RED'
    ASM_ECH     = 'ECH'
    ASM_EXT     = 'EXT'
    ASM_LOD     = 'LOD'
    ASM_AFT     = 'AFT'
    ASM_EQU     = 'EQU'
    ASM_GTH     = 'GTH'
    ASM_LTH     = 'LTH'
    ASM_NOT     = 'NOT'
    ASM_JMP     = 'JMP'
    ASM_ADD     = 'ADD'
    ASM_SUB     = 'SUB'
    ASM_NOP     = 'NOP'
    ASM_REQ_LAYOUT = [
        ASM_EXT,
        ASM_AFT,
        ASM_EQU,
        ASM_GTH,
        ASM_LTH,
        ASM_NOT,
        ASM_ADD,
        ASM_SUB,
        ASM_LOD
    ]
    # map func_name -> asm_instr
    FUNC_MAP    = {
        BIF_READ:   ASM_RED,
        BIF_ECHO:   ASM_ECH,
        BIF_EXIT:   ASM_EXT,
        OP_LOAD:    ASM_LOD,
        OP_AFCT:    ASM_AFT,
        OP_ADD:     ASM_ADD,
        OP_SUB:     ASM_SUB
    }
    # map asm_operator -> binary value
    ASM_MAP     = {
        ASM_RES:  0x0,
        ASM_CPY:  0x1,
        ASM_RED:  0x2,
        ASM_ECH:  0x3,
        ASM_EXT:  0x4,
        ASM_LOD:  0x5,
        ASM_AFT:  0x6,
        ASM_EQU:  0x8,
        ASM_GTH:  0x9,
        ASM_LTH:  0xa,
        ASM_NOT:  0xb,
        ASM_JMP:  0xc,
        ASM_ADD:  0xd,
        ASM_SUB:  0xe,
        ASM_NOP:  0xf
    }
    # map var type -> binary value
    TYPE_MAP = {
        VT_BOOL: 0x0,
        VT_INT:  0x1,
        VT_CHAR: 0x2
    }
    # Bin Sections
    BS_SIGN = b'.SGS'
    BS_SIGN_ENC = b'.SGSE'
    BS_DATA = b'.data'
    BS_CODE = b'.code'
    # RunTime properties
    RT_VERBOSE=False
    RT_DEBUG=False
    RT_ENCRYPT=False
    RT_ENCODING='utf8'
    # format methods
    @staticmethod
    def format_asm(asm):
        asm_text = ''
        l=0
        for instr in asm:
            asm_text += ('%04d: %s %s\n' % (l, instr['code'], ' '.join([ str(e) for e in instr['ops'] ])))
            l += 1
        return asm_text
    # factory methods
    @staticmethod
    def identifier(name):
        if name.isdigit():
            return int(name)
        else:
            return '@'+name

    @staticmethod
    def asm_instr(code, ops, process_ops=False):
        if not isinstance(code, str) or not code in SGSConfig.ASM_MAP.keys():
            SGSConfig.fat('Invalid code given to asm_instr (%s)' % code)
        if not isinstance(ops, list):
            SGSConfig.fat('Invalid ops given to asm_instr (%s)' % ops)
        if process_ops:
            ops = [ SGSConfig.identifier(op) for op in ops ]
        return {
            'code': code,
            'ops': ops
        }

    @staticmethod
    def asm_layout(layout):
        if len(layout) > 2:
            SGSConfig.fat('Unexpected layout value given to asm_layout! (%s)' % layout)
        i=0
        o=0
        for l in layout:
            if l == 's':
                i|=(1<<o)
                o += 1
        return i

    # logging methods
    @staticmethod
    def printf(msg, lvl=None):
        if lvl is None:
            print(msg)
        else:
            print('[%s] > %s' % (lvl, msg))

    @staticmethod
    def err(msg):
        SGSConfig.printf(msg, 'err')

    @staticmethod
    def fat(msg):
        SGSConfig.printf(msg, 'fat')
        exit(-1)

    @staticmethod
    def inf(msg):
        if SGSConfig.RT_VERBOSE or SGSConfig.RT_DEBUG:
            SGSConfig.printf(msg, 'inf')

    @staticmethod
    def dbg(msg, no_prefix=False):
        if SGSConfig.RT_DEBUG:
            if no_prefix:
                SGSConfig.printf(msg)
            else:
                SGSConfig.printf(msg, 'dbg')