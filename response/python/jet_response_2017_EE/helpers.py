''' Helper functions for EE study
'''

def cut_string( var, b):
    cs = []
    if b[0]>=0: cs.append("%s>=%f"%(var, b[0]))
    if b[1]>=0: cs.append("%s<%f"%(var, b[1]))
    ret = "&&".join( cs )
    if ret=="":
        return "(1)" 
    else:
        return ret

def pt_tex_string( var, b):
    cs = []
    if b[0]>=0: cs.append("%i #leq %s"%(b[0], var))
    if b[1]>=0: cs.append("< %i"%( b[1]))
    return "".join( cs )

def eta_tex_string( var, b):
    cs = []
    if b[0]>=0: cs.append("%3.2f #leq %s"%(b[0], var))
    if b[1]>=0: cs.append("< %3.2f"%( b[1]))
    return "".join( cs )
