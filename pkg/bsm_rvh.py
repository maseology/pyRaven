

# build HRU/Basin Definition file (.rvh)
def write(root, nam, desc, builder, ver, wshd):
    with open(root + nam + ".rvh","w") as f:
        f.write('# --------------------------------------------\n')
        f.write('# Raven HRU Definition (.rvh) file\n')
        f.write('# ' + desc + '\n')
        f.write('# written by ' + builder + '\n')
        f.write('# using pyRaven builder\n')
        f.write('# Raven version: ' + ver + '\n')
        f.write('# --------------------------------------------\n\n')

        f.write('####\n')
        f.write(':SubBasins\n')
        f.write(' :Attributes           NAME  DOWNSTREAM_ID        PROFILE   REACH_LENGTH         GAUGED\n')
        f.write(' :Units                none           none           none             km           none\n')
        tt = set()
        for _,t in wshd.t.items():
            tt.add(t[0])
            f.write('  {:<10}{:>15}{:15}{:>15}{:15.3f}{:15}\n'.format(t[0],"s" + str(t[0]),t[1],'default_trap',wshd.s[t[0]].rchlen,0))
        for t in wshd.xr:
            if t in tt: continue
            f.write('  {:<10}{:>15}{:15}{:>15}{:15.3f}{:15}\n'.format(t,"s" + str(t),-1,'default_trap',wshd.s[t].rchlen,0))
        f.write(':EndSubBasins\n\n')
