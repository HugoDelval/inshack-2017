# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    sgs_compiler.py
# date:    2017-01-05
# author:  paul dautry
# purpose:
#       Classe du compilateur SGS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from sgs_compil_utils.sgs_config import SGSConfig
import json

class SGSCompiler(object):
    """docstring for SGSCompiler"""
    def __init__(self, options, prog_struct):
        super(SGSCompiler, self).__init__()
        self.options = options
        self.prog_struct = prog_struct
        self.error = 'n/a'
        self.nop = [ SGSConfig.asm_instr(SGSConfig.ASM_NOP, []) ]
        

    def compile(self):
        register_table = [ None for i in range(0, 8) ]
        asm_instr_list = []
        for instr in self.prog_struct['instructions']:
            typ = instr['type'] 
            if typ == SGSConfig.CST_BLOC:
                asm_instr_list += self.compile_bloc(instr)
            elif typ == SGSConfig.CST_INST:
                asm_instr_list += self.compile_instr(instr)
            else:
                self.error = 'Unknown type: %s' % typ
                return False
        self.prog_struct['asm'] = asm_instr_list
        return True

    def compile_bloc(self, bloc):
        SGSConfig.dbg('compile_bloc called with:')
        SGSConfig.dbg(json.dumps(bloc, sort_keys=True, indent=2), True)
        asm_instr_list = []
        bloc_instr_list = []
        # add condition preparation instructions
        bloc_instr_list += self.compile_condition(bloc['condition'])
        # compile loop instructions
        for instr in bloc['instructions']:
            typ = instr['type']
            if typ == SGSConfig.CST_BLOC:
                asm_instr_list += self.compile_bloc(instr)
            elif typ == SGSConfig.CST_INST:
                asm_instr_list += self.compile_instr(instr)
            else:
                SGSConfig.fat('Unknown type: %s' % typ)
        # finalize bloc instruction knowing internal bloc size
        keyword = bloc['keyword']
        if keyword == SGSConfig.LK_WHILE:
            bloc_instr_list.append(
                SGSConfig.asm_instr(SGSConfig.ASM_JMP, [len(asm_instr_list)+2])
            )
            bloc_instr_list += asm_instr_list
            bloc_instr_list.append(
                SGSConfig.asm_instr(SGSConfig.ASM_JMP, [-len(bloc_instr_list)])
            )
        elif keyword == SGSConfig.LK_IF:
            bloc_instr_list.append(
                SGSConfig.asm_instr(SGSConfig.ASM_JMP, [len(asm_instr_list)+1])
            )
            bloc_instr_list += asm_instr_list
        else:
            SGSConfig.fat('Unknown keyword: %s' % keyword)
        return bloc_instr_list

    def compile_instr(self, instr):
        SGSConfig.dbg('compile_instr called with:')
        SGSConfig.dbg(json.dumps(instr, sort_keys=True, indent=2), True)
        # compile instruction
        asm_instr_list = []
        func = instr['func']
        if func in SGSConfig.FUNC_MAP.keys(): 
            asm = SGSConfig.asm_instr(SGSConfig.FUNC_MAP[func], [])
            for op in instr['operands']:
                if isinstance(op, dict):
                    asm_instr_list += self.compile_instr(op)
                    asm['ops'].append(SGSConfig.SV_RR)
                else:
                    asm['ops'].append(SGSConfig.identifier(op))
            asm_instr_list.append(asm)
        else:
            SGSConfig.fat('Unknown function: %s' % func)
        return asm_instr_list

    def compile_condition(self, clause):
        parts = clause.split(' ')
        asm_instr_list = []
        if len(parts) == 3:
            if parts[1] == SGSConfig.SYM_NEQ:
                asm_instr_list.append(SGSConfig.asm_instr(SGSConfig.ASM_EQU, 
                    [ parts[0], parts[2] ], True))
            elif parts[1] == SGSConfig.SYM_EQU:
                asm_instr_list.append(SGSConfig.asm_instr(SGSConfig.ASM_EQU, 
                    [ parts[0], parts[2] ], True))
                asm_instr_list.append(SGSConfig.asm_instr(SGSConfig.ASM_NOT, 
                    [ SGSConfig.SV_RF ]))
            elif parts[1] == SGSConfig.SYM_GTE:
                asm_instr_list.append(SGSConfig.asm_instr(SGSConfig.ASM_LTH, 
                    [ parts[0], parts[2] ], True))
            elif parts[1] == SGSConfig.SYM_LTE:
                asm_instr_list.append(SGSConfig.asm_instr(SGSConfig.ASM_GTH, 
                    [ parts[0], parts[2] ], True))
            elif parts[1] == SGSConfig.SYM_LTH:
                asm_instr_list.append(SGSConfig.asm_instr(SGSConfig.ASM_LTH, 
                    [ parts[0], parts[2] ], True))
                asm_instr_list.append(SGSConfig.asm_instr(SGSConfig.ASM_NOT, 
                    [ SGSConfig.SV_RF ]))
            elif parts[1] == SGSConfig.SYM_GTH:
                asm_instr_list.append(SGSConfig.asm_instr(SGSConfig.ASM_GTH, 
                    [ parts[0], parts[2] ], True))
                asm_instr_list.append(SGSConfig.asm_instr(SGSConfig.ASM_NOT, 
                    [ SGSConfig.SV_RF ]))
            else:
                SGSConfig.fat('Unhandled comparison operator: %s' % parts[1])
        elif len(parts) == 2:
            if parts[0] == SGSConfig.SYM_NOT:
                asm_instr_list.append(SGSConfig.asm_instr(SGSConfig.ASM_NOT, 
                    [ parts[1] ], True))
                asm_instr_list.append(SGSConfig.asm_instr(SGSConfig.ASM_NOT, 
                [ SGSConfig.SV_RF ]))
            else:
                SGSConfig.fat('Unhandled boolean operator: %s' % parts[0])
        elif len(parts) == 1:
            asm_instr_list.append(SGSConfig.asm_instr(SGSConfig.ASM_NOT, 
                [ parts[0] ], True))
        else:
            SGSConfig.fat('Unhandled condition syntax: %s' % clause)
        return asm_instr_list

    
