

from pymmio import ascii


class feasibleRange:
    pnam=None
    low=-9999
    high=-9999
    opt=None
    
def getPranges(ostInFp):
    on = False
    fr = dict()
    for ln in ascii.readLines(ostInFp):
        if on or ln.lower()=='beginparams':
            if not on:
                on=True
            elif ln[0]=='#':
                pass
            elif ln.lower()=='endparams':
                on=False
            else:
                stp = ascii.splitSpaceTabLine(ln)
                fr[stp[0]] = feasibleRange()
                fr[stp[0]].low=float(stp[2])
                fr[stp[0]].high=float(stp[3])
                fr[stp[0]].opt=dict()
                if stp[-1]!='none': fr[stp[0]].pnam=ln[ln.rfind('#')+1:].strip()
    return fr

def getPoptimum(OstOutput0Fp, fr):
    bestobjfnc=None
    for ln in ascii.readLines(OstOutput0Fp):
        stp = ascii.splitSpaceTabLine(ln)
        if 'Objective Function :' in ln:
            bestobjfnc=float(stp[-1])
        elif stp[0] in fr:
            fr[stp[0]].opt[OstOutput0Fp] = float(stp[-1])
    return bestobjfnc