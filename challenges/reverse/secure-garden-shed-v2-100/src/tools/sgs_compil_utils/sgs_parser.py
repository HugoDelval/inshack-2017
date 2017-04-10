# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    sgs_parser.py
# date:    2017-01-05
# author:  paul dautry
# purpose:
#       Classe du parser de source SGS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from sgs_compil_utils.sgs_config import SGSConfig

class SGSParser(object):
    """docstring for SGSParser"""
    def __init__(self, infile, options):
        super(SGSParser, self).__init__()
        self.infile = infile
        self.options = options
        self.error = 'n/a'
        self.lnum = 0
        self.prog_struct = {
            'options': {},
            'data': {
                SGSConfig.VT_BOOL: [],
                SGSConfig.VT_INT: [],
                SGSConfig.VT_CHAR: []
            },
            'instructions': None,
            'asm': None
        }

    def parse(self):
        step = None
        script = []
        with open(self.infile, 'r') as f:
            for line in f:
                self.lnum += 1
                line = line.strip()
                if SGSConfig.SYM_COM in line:
                    line = ''.join(line.split(SGSConfig.SYM_COM)[:1]).strip()
                if len(line) == 0:
                    continue
                if line[0] == SGSConfig.SYM_SCT:
                    step = line.strip()
                    continue
                elif step == SGSConfig.SCS_OPT:
                    if not self.parse_option_line(line):
                        self.error = 'An error occured while parsing an option line.\n' + self.error
                        return False
                elif step == SGSConfig.SCS_VAR:
                    if not self.parse_variable_line(line):
                        self.error = 'An error occured while parsing a vardecl line.\n' + self.error
                        return False
                elif step == SGSConfig.SCS_SCR:
                    script.append(line)
                elif step is None:
                    continue
                else:
                    self.error = 'Invalid step value: %s' % step
                    return False
            # parse program instructions
            (script, instructions) = self.parse_script(script)
            if len(script) != 0:
                self.error = 'Script array should be empty now...'
                return False
            self.prog_struct['instructions'] = instructions 
        return True

    def parse_option_line(self, line):
        parts = line.split(SGSConfig.SYM_SEP)
        if len(parts) == 1:
            self.error = 'Option key found without value: %s' % parts[0]
            return False
        elif len(parts) == 2:
            self.prog_struct['options'][parts[0]] = parts[1]
        else:
            self.error = 'Invalid option line at line %d' % self.lnum
            return False
        return True

    def parse_variable_line(self, line):
        is_tab = False
        parts = line.split(SGSConfig.SYM_PSEP)
        if parts[0] == SGSConfig.LK_TAB:
            is_tab = True
            parts = parts[1:]
        if len(parts) < 2:
            self.error = 'Missing data type or identifier!'
            return False
        if self.prog_struct['data'].get(parts[0], None) is not None:
            variable = {
                'tab': is_tab,
                'name': parts[1],
                'val': self.extract_val(parts, is_tab)
            }
            if is_tab and variable['val'] is None:
                self.error = 'Illegal tab declaration (tab vars must have an initial value).'
                return False         
            self.prog_struct['data'][parts[0]].append(variable)
        else:
            self.error = 'Invalid data type: %s' % parts[0]
            return False
        return True
    
    def extract_val(self, parts, is_tab):
        if len(parts) < 3:
            return None
        val = SGSConfig.SYM_PSEP.join(parts[2:]).strip()
        if val[0] == SGSConfig.SYM_SBND and val[-1] == SGSConfig.SYM_SBND:
            val = val[1:-1]
        else:
            val = [ e.strip() for e in val.split(SGSConfig.SYM_VSEP) ]
        if len(val) == 0:
            val = None
        elif parts[0] == SGSConfig.VT_INT:
            buf = []
            for e in val:
                if not e.isdigit():
                    SGSConfig.fat('Initialization value must be an integer value!')
                ev = int(e)
                if abs(ev) > SGSConfig.MAX_INT_32:
                    SGSConfig.fat('Signed 32-bits-integer max. value exceeded! (%d > %d)' % (v, SGSConfig.MAX_INT_32))
                buf.append(ev)
            val = buf
        elif parts[0] == SGSConfig.VT_BOOL:
            for e in val:
                if e not in SGSConfig.BOOL_VALUES:
                    SGSConfig.fat('Illegal boolean initialization value! Should be one of %s.' % SGSConfig.BOOL_VALUES)
        return val

    def parse_script(self, script):
        bloc_parsed = False
        instr_list = []
        while len(script) > 0:
            line = script[0]
            script = script[1:]
            if SGSConfig.LK_END == line.strip():
                return (script, instr_list)
            for keyword in SGSConfig.BLOC_KEYWORDS:
                if keyword in line:
                    (script, instructions) = self.parse_script(script)
                    instr_list.append({
                            'type': SGSConfig.CST_BLOC,
                            'keyword': keyword,
                            'condition': line.replace(keyword, '').strip(),
                            'instructions': instructions
                        })
                    bloc_parsed = True
                    break
            if bloc_parsed:
                bloc_parsed = False
                continue
            instr = self.parse_instr(line)
            if instr is None:
                SGSConfig.fat('An error occured while parsing instruction!')
            instr_list.append(instr)
        return (script, instr_list)

    def build_instr(self, func, operands):
            if not isinstance(operands, list):
                SGSConfig.fat('operands must be a list!')
            if not isinstance(func, str):
                SGSConfig.fat('func must be a list!')
            return {
                'type': SGSConfig.CST_INST,
                'func': func,
                'operands': operands
            }

    def parse_instr(self, line):
        instr = None
        if  SGSConfig.SYM_AFCT in line:
            parts = line.split(SGSConfig.SYM_AFCT)
            if len(parts) > 2:
                afct = self.find_appropriate_affect(parts[-1].strip())
                instr = self.build_instr(afct, [
                    self.parse_instr(SGSConfig.SYM_AFCT.join(parts[:-1])), 
                    parts[-1].strip()
                ])
            else:
                fop = parts[0].strip()
                sop = parts[1].strip()
                afct = self.find_appropriate_affect(sop)
                instr = self.build_instr(afct, [])
                recurse = False
                for operator in SGSConfig.SUB_OPS:
                    if operator in fop:
                        recurse = True
                if recurse:
                    instr['operands'].append(self.parse_instr(fop))
                    instr['operands'].append(sop)
                else:
                    instr['operands'] = [ e.strip() for e in parts ]
        else:
            if SGSConfig.SYM_LOAD in line:
                parts = line.strip().split(SGSConfig.SYM_LOAD)
                instr = self.build_instr(SGSConfig.OP_LOAD, [
                    parts[0], 
                    parts[-1].strip()[:-1]
                ]) 
            elif SGSConfig.SYM_ADD in line:
                parts = line.split(SGSConfig.SYM_ADD)
                instr = self.build_instr(SGSConfig.OP_ADD, [
                    e.strip() for e in parts
                ])
            else:
                parts = line.split(SGSConfig.SYM_PSEP)
                instr = self.build_instr(parts[0], parts[1:])
        return instr

    def find_appropriate_affect(self, identifier):
        return SGSConfig.OP_AFCT
        #for e in self.prog_struct['data'][SGSConfig.VT_BOOL]:
        #    if e['name'] == identifier:
        #        return SGSConfig.OP_AFCTB
        #for e in self.prog_struct['data'][SGSConfig.VT_INT]:
        #    if e['name'] == identifier:
        #        return SGSConfig.OP_AFCT
        #for e in self.prog_struct['data'][SGSConfig.VT_CHAR]:
        #    if e['name'] == identifier:
        #        return SGSConfig.OP_AFCTB