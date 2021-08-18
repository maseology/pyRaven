

# build HRU/Basin Definition file (.rvh)
def write(root, nam, desc, builder, ver, wshd):
    if len(wshd.xr) > 1:
        writeMany(root, nam, desc, builder, ver, wshd)        
    else:
        writeOne(root, nam, desc, builder, ver)

def writeOne(root, nam, desc, builder, ver):
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
        f.write('           1           station          -1           none             km              1\n')
        f.write(':EndSubBasins\n\n')

        f.write('####\n')
        f.write(':HRUs\n')
        f.write(' :Attributes      AREA ELEVATION  LATITUDE LONGITUDE  BASIN_ID  LAND_USE_CLASS      VEG_CLASS   SOIL_PROFILE   AQUIFER_PROFILE   TERRAIN_CLASS     SLOPE    ASPECT\n')
        f.write(' :Units            km2         m       deg       deg      none            none           none           none              none            none       rad       rad\n')
        f.write('  {:<10}{:10.3f}{:10.1f}{:10.3f}{:10.3f}{:10}          LU_ALL        VEG_ALL      DEFAULT_P            [NONE]          [NONE]{:10.3f}{:10.3f}\n'.format(1,0.01,250,44.185,-79.479,1,0,0))
        f.write(':EndHRUs\n\n')       

def writeMany(root, nam, desc, builder, ver, wshd):
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
        for k in reversed(list(wshd.t.keys())):
            t = wshd.t[k]
            tt.add(t[0])
            f.write('  {:<10}{:>15}{:15}{:>15}{:15.3f}{:15}\n'.format(t[0],"s" + str(t[0]),t[1],'NONE',wshd.s[t[0]].rchlen,0))
        for t in wshd.xr:
            if t in tt: continue
            f.write('  {:<10}{:>15}{:15}{:>15}{:15.3f}{:15}\n'.format(t,"s" + str(t),-1,'NONE',wshd.s[t].rchlen,0))
        f.write(':EndSubBasins\n\n')

        f.write('####\n')
        f.write(':HRUs\n')
        f.write(' :Attributes      AREA ELEVATION  LATITUDE LONGITUDE  BASIN_ID  LAND_USE_CLASS      VEG_CLASS   SOIL_PROFILE  AQUIFER_PROFILE  TERRAIN_CLASS     SLOPE    ASPECT\n')
        f.write(' :Units            km2         m       deg       deg      none            none           none           none             none           none       rad       rad\n')
        for t in wshd.xr:
            s = wshd.s[t]            
            f.write('  {:<10}{:10.3f}{:10.1f}{:10.3f}{:10.3f}{:10}          LU_ALL        VEG_ALL      DEFAULT_P            [NONE]          [NONE]{:10.3f}{:10.3f}\n'.format(t,s.km2,s.elv,s.ylat,s.xlng,t,s.slp,s.asp))
        f.write(':EndHRUs\n\n')
