# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    sgs_assembler.py
# date:    2017-01-05
# author:  paul dautry
# purpose:
#       Classe de l'assembleur SGS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from sgs_compil_utils.sgs_config import SGSConfig
import struct
import ctypes
import json
import os

class SGSAssembler(object):
    """docstring for SGSAssembler"""
    def __init__(self, outfile, options, prog_struct):
        super(SGSAssembler, self).__init__()
        self.outfile = outfile
        self.options = options
        self.prog_struct = prog_struct
        self.error = 'n/a'
        self.var_map = {}
        self.max_stack_oft = 8
        self.add_var(SGSConfig.VT_REG, SGSConfig.SV_RR, None, 32, 0)
        self.add_var(SGSConfig.VT_REG, SGSConfig.SV_RF, None, 32, 4)

    def assemble(self):
        (status, data_section) = self.assemble_data()
        if not status:
            self.error = 'Failed to assemble data section.\n' + self.error
            return False
        if not self.finalize_stack_layout():
            self.error = 'Failed to finalize stack layout.\n' + self.error
            return False
        if not self.finalize_asm():
            self.error = 'Failed to finalize asm.\n' + self.error
            return False
        (status, code_section) = self.assemble_script()
        if not status:
                self.error = 'Failed to assemble script section.\n' + self.error
                return False
        with open(self.outfile, 'wb') as f:
            if SGSConfig.RT_ENCRYPT:
                f.write(SGSConfig.BS_SIGN_ENC)
                f.write(self.prog_struct['options']['key'])
            else:
                f.write(SGSConfig.BS_SIGN)
            f.write(SGSConfig.BS_CODE)
            f.write(code_section)
            f.write(SGSConfig.BS_DATA)
            f.write(data_section)
        return True

    def assemble_data(self):
        data = self.prog_struct['data']
        data_section = bytes()
        global_offset = 0
        # compile booleans
        (data_subsection, offset) = self.assemble_bool_data(data['bool'], global_offset)
        data_section += data_subsection
        global_offset = offset
        SGSConfig.dbg('bool section ends (global offset is %d)' % global_offset)
        # compile integers
        (data_subsection, offset) = self.assemble_int_data(data['int'], global_offset)
        data_section += data_subsection
        global_offset = offset
        SGSConfig.dbg('int section ends (global offset is %d)' % global_offset)
        # compile char
        (data_subsection, offset) = self.assemble_char_data(data['char'], global_offset)
        data_section += data_subsection
        global_offset = offset
        SGSConfig.dbg('char section ends (global offset is %d)' % global_offset)
        # write data section to file if necessary
        if len(data_section) > 0: 
            # encrypt if necessary
            if SGSConfig.RT_ENCRYPT:
                SGSConfig.dbg('data section encrypted')
                data_section = self.encrypt_data(data_section)
        return (True, data_section)

    def assemble_bool_data(self, bool_data, global_offset):
        offset = None
        data_section = bytes()
        for var in bool_data:
            length = 0
            t = var['val']
            if t is not None:
                bbstring = 0x00
                offset = global_offset
                # create boolean initialization bit string
                for v in t:
                    v = (0 if v == 'false' else 1)
                    bbstring |= v << 1
                    bbstring = bbstring << 2
                # add end marker
                bbstring|=3
                # pad bit string
                bbstring = bbstring << ((len(bin(bbstring))-2) % 8)
                # write byte per byte
                bbstring=bin(bbstring)[2:]
                while len(bbstring) > 0:
                    length += 8
                    global_offset += 8
                    data_section += bytes([int(bbstring[:8], 2)])
                    bbstring = bbstring[8:]
            else:
                offset = None
                length = 8
            self.add_var(SGSConfig.VT_BOOL, '@'+var['name'], offset, length)
        return (data_section, global_offset)

    def assemble_int_data(self, int_data, global_offset):
        offset = None
        data_section = bytes()
        int_buffer = ctypes.create_string_buffer(4)
        for var in int_data:
            length = 0
            t = var['val']
            if t is not None:
                offset = global_offset
                for v in t:
                    struct.pack_into('>i', int_buffer, 0, v)
                    data_section += int_buffer
                    global_offset += 32
                    length += 32
                struct.pack_into('>I', int_buffer, 0, 0xffffffff)
                data_section += int_buffer
                global_offset += 32
                length += 32
            else:
                offset = None
                length = 32
            self.add_var(SGSConfig.VT_INT, '@'+var['name'], offset, length)
        return (data_section, global_offset)

    def assemble_char_data(self, char_data, global_offset):
        offset = None
        data_section = bytes()
        for var in char_data:
            length = 0
            v = var['val']
            if v is not None:
                data_section += bytes(v, encoding=SGSConfig.RT_ENCODING) + bytes([0])
                offset = global_offset
                global_offset += (len(v)+1)*8
                length += (len(v)+1)*8
            else:
                offset = None
                length = 8
            self.add_var(SGSConfig.VT_CHAR, '@'+var['name'], offset, length)
        return (data_section, global_offset)

    def add_var(self, typ, name, data_oft, length, stack_oft=None):
        self.var_map[name] = {
            'type': typ, 
            'data_oft': data_oft, 
            'len':length, 
            'stack_oft': stack_oft
        }

    def encrypt_data(self, data_section):
        if self.prog_struct['options'].get('key', None) is None:
            self.prog_struct['options']['key'] = self.keygen(len(data_section))
        if isinstance(self.prog_struct['options']['key'], str):
            self.prog_struct['options']['key'] = bytes(self.prog_struct['options']['key'], 
                encoding=SGSConfig.RT_ENCODING)
        key = self.prog_struct['options']['key']
        ksz = len(key)
        edata_section = bytes()
        for k in range(0, len(data_section)):
            edata_section += bytes([data_section[k]^key[k%ksz]])
        return edata_section

    def keygen(self, data_sz):
        key = os.urandom(data_sz)
        return key

    def finalize_stack_layout(self):
        SGSConfig.dbg('---------- var map before finalization ----------')
        SGSConfig.dbg(json.dumps(self.var_map, indent=2, sort_keys=True), True)
        for var, info in self.var_map.items():
            if info['stack_oft'] is None:
                typ = info['type']
                if info['data_oft'] is None: 
                        info['stack_oft'] = self.max_stack_oft
                        self.max_stack_oft += 4
                else:
                    l = info['len']
                    while l % 32 != 0:
                        l += 1
                    info['stack_oft'] = self.max_stack_oft
                    self.max_stack_oft += int(l/8)
            if self.max_stack_oft > SGSConfig.MAX_SGS_UINT:
                self.error = 'Max stack size reached!'
                return False 
        SGSConfig.dbg('---------- var map after finalization -----------')
        SGSConfig.dbg(json.dumps(self.var_map, indent=2, sort_keys=True), True)
        return True

    def finalize_asm(self):
        SGSConfig.dbg('------------ asm before finalization ------------')
        SGSConfig.dbg(SGSConfig.format_asm(self.prog_struct['asm']), True)
        final_asm = []
        # add stack setup instructions
        final_asm.append(SGSConfig.asm_instr(SGSConfig.ASM_RES, 
            [ self.max_stack_oft ]))
        for var, info in self.var_map.items():
            if info['data_oft'] is not None:
                final_asm.append(SGSConfig.asm_instr(SGSConfig.ASM_CPY, [ 
                    SGSConfig.TYPE_MAP[info['type']],
                    info['data_oft'], info['stack_oft']
                ]))
        # process actual instructions
        for instr in self.prog_struct['asm']:
            ops = []
            code = instr['code']
            add_layout = (code in SGSConfig.ASM_REQ_LAYOUT)
            layout = ''
            for op in instr['ops']:
                if isinstance(op, str):
                    layout += 's'
                    op = self.var_map[op]['stack_oft']
                    if op > SGSConfig.MAX_SGS_UINT:
                        self.error = 'Unsigned integer overflow (13bits)'
                        return False
                else:
                    layout += 'v'
                    if op > SGSConfig.MAX_SGS_INT:
                        self.error = 'Signed integer overflow (12bits)'
                        return (False, None)
                    if op < 0:
                        oop=-op
                        op=1<<12
                        op|=oop
                ops.append(op)
            if add_layout:
                ops = [ SGSConfig.asm_layout(layout) ] + ops
            final_asm.append(SGSConfig.asm_instr(code, ops))
        self.prog_struct['asm'] = final_asm
        SGSConfig.dbg('------------ asm after finalization -------------')
        SGSConfig.dbg(SGSConfig.format_asm(self.prog_struct['asm']), True)
        return True

    def assemble_script(self):
        asm = self.prog_struct['asm']
        # init instructions
        code_section = bytes()
        int_buffer = ctypes.create_string_buffer(4)
        for instr in asm:
            code = instr['code']
            ops = instr['ops']
            i = 0x00000000
            i |= (SGSConfig.ASM_MAP[code] << 28)
            if code == SGSConfig.ASM_RES:
                i |= (ops[0] << 15)
            elif code == SGSConfig.ASM_CPY:
                i |= (ops[0] << 26)
                i |= (ops[1] << 13)
                i |= (ops[2])
            elif code == SGSConfig.ASM_RED:
                i |= (ops[0] << 15)
            elif code == SGSConfig.ASM_ECH:
                i |= (ops[0] << 15)
            elif code == SGSConfig.ASM_EXT:
                i |= (ops[0] << 26)
                i |= (ops[1] << 13)
            elif code == SGSConfig.ASM_LOD:
                i |= (ops[0] << 26)
                i |= (ops[1] << 13)
                i |= (ops[2])
            elif code == SGSConfig.ASM_AFT:
                i |= (ops[0] << 26)
                i |= (ops[1] << 13)
                i |= (ops[2])
            elif code == SGSConfig.ASM_EQU:
                i |= (ops[0] << 26)
                i |= (ops[1] << 13)
                i |= (ops[2])
            elif code == SGSConfig.ASM_GTH:
                i |= (ops[0] << 26)
                i |= (ops[1] << 13)
                i |= (ops[2])
            elif code == SGSConfig.ASM_LTH:
                i |= (ops[0] << 26)
                i |= (ops[1] << 13)
                i |= (ops[2])
            elif code == SGSConfig.ASM_NOT:
                i |= (ops[0] << 26)
                i |= (ops[1] << 13)
            elif code == SGSConfig.ASM_JMP:
                if ops[0] < 0:
                    op = - ops[0]
                    op |= (1<<12)
                else:
                    i |= (ops[0] << 15)
            elif code == SGSConfig.ASM_ADD:
                i |= (ops[0] << 26)
                i |= (ops[1] << 13)
                i |= (ops[2])
            elif code == SGSConfig.ASM_SUB:
                i |= (ops[0] << 26)
                i |= (ops[1] << 13)
                i |= (ops[2])
            elif code == SGSConfig.ASM_NOP:
                i=i
            else:
                self.error = 'Unknown instruction code: %s' % code
                return (False, None)
            struct.pack_into('>I', int_buffer, 0, i)
            SGSConfig.dbg('translation: %40s -> %s (%s)' % (instr, bin(i), list(int_buffer)))
            code_section += int_buffer
        return (True, code_section)
