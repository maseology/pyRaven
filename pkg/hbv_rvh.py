

# build HRU/Basin Definition file (.rvh)
def write(root, nam, desc, builder, ver, wshd, hrus, par):
    with open(root + nam + ".rvh","w") as f:
        f.write('# --------------------------------------------\n')
        f.write('# Raven HRU Definition (.rvh) file\n')
        # f.write('# HBV-EC semi-distributed watershed model\n')
        f.write('# ' + desc + '\n')
        f.write('# written by ' + builder + '\n')
        f.write('# using pyRaven builder\n')
        f.write('# Raven version: ' + ver + '\n')
        f.write('# --------------------------------------------\n\n')

        f.write('####\n')
        f.write(':SubBasins\n')
        f.write(' :Attributes           NAME  DOWNSTREAM_ID        PROFILE   REACH_LENGTH    GAUGED\n')
        f.write(' :Units                none           none           none             km      none\n')
        tt = set()
        for _,t in wshd.t.items():
            tt.add(t[0])
            f.write('  {:<10}{:>15}{:15}{:>15}{:15.3f}{:10}\n'.format(t[0],"s" + str(t[0]),t[1],'default_trap',wshd.s[t[0]].rchlen,0))
        for t in wshd.xr:
            if t in tt: continue
            f.write('  {:<10}{:>15}{:15}{:>15}{:15.3f}{:10}\n'.format(t,"s" + str(t),-1,'default_trap',wshd.s[t].rchlen,1))
        f.write(':EndSubBasins\n\n')

        f.write('####\n')
        f.write(':SubBasinProperties\n')
        f.write('# notes: t_conc=MAX_BAS in HBV (t_peak=t_conc/2 for HBV replication)\n')
        f.write(' :Parameters      TIME_CONC   TIME_TO_PEAK  TIME_LAG\n')
        f.write(' :Units                   d              d         d\n')
        for t in wshd.xr:
            f.write('  {:<10}{:>15}{:15}{:10}\n'.format(t,par.MAX_BAS,par.MAX_BAS/2,par.TIME_LAG))
        f.write(':EndSubBasinProperties\n\n')

        f.write('####\n')
        f.write(':HRUs\n')
        f.write(' :Attributes      AREA ELEVATION  LATITUDE LONGITUDE  BASIN_ID      LAND_USE_CLASS           VEG_CLASS        SOIL_PROFILE AQUIFER_PROFILE  TERRAIN_CLASS     SLOPE    ASPECT\n')
        f.write(' :Units            km2         m       deg       deg      none                none                none                none            none           none       rad       rad\n')
        c = 0
        # for t in wshd.xr:
        #     c += 1
        #     s = wshd.s[t]            
        #     f.write('  {:<10}{:10.3f}{:10.1f}{:10.1f}{:10.1f}{:10}         LU_ALL        VEG_ALL      DEFAULT_P          [NONE]         [NONE]{:10.3f}{:10.3f}\n'.format(c,s.km2,s.elv,s.ylat,s.xlng,t,s.slp,s.asp))
        for t,lusg in hrus.items():
            s = wshd.s[t]
            for k,frac in lusg.items():
                c += 1
                f.write('  {:<10}{:10.3f}{:10.1f}{:10.1f}{:10.1f}{:10}{:>20}{:>20}{:>20}          [NONE]         [NONE]{:10.3f}{:10.3f}\n'.format(c,s.km2*frac,s.elv,s.ylat,s.xlng,t,k[0][0],k[0][1],k[1],s.slp,s.asp))
        f.write(':EndHRUs\n\n')

        f.write('####\n')
        f.write(':HRUGroup AllHRUs\n')
        f.write(' 1-{}'.format(c))
        f.write(':EndHRUGroup\n\n')