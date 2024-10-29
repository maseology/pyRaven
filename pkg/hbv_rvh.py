
from pkg import rvprint, lakes_rvh

# build HRU/Basin Definition file (.rvh)
def write(root, nam, desc, builder, ver, wshd, hrus, par):

    dlakes = dict()
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
        f.write(' :Attributes                            NAME  DOWNSTREAM_ID        PROFILE   REACH_LENGTH    GAUGED\n')
        f.write(' :Units                                 none           none           none             km      none\n')
        for usid,h in hrus.items():
            dsid = -1
            if usid in wshd.t: dsid = wshd.t[usid]
            if not dsid in hrus: dsid = -1

            # gauged?
            gag = 0
            if len(wshd.gag)>0: 
                if len(wshd.gag[usid])>0: gag = 1

            # watershed name
            if len(wshd.nam)==0:
                nam = 's'+str(usid)
            else:
                if len(wshd.gag[usid])>0:
                    nam = wshd.gag[usid]
                else:
                    nam = wshd.nam[usid].replace(' ','_')+'_'+str(usid)

            if h=="lake":
                f.write('  {:<10}{:>32}{:15}{:>15}{:>15}{:10}\n'.format(usid,nam,dsid,'default_trap','ZERO-',gag))
            else:
                f.write('  {:<10}{:>32}{:15}{:>15}{:15.3f}{:10}\n'.format(usid,nam,dsid,'default_trap',wshd.s[usid].rchlen,gag))
        # tt = set()
        # for usid,dsid in wshd.t.items():
        #     if dsid<=0: continue
        #     tt.add(usid)
        #     f.write('  {:<10}{:>15}{:15}{:>15}{:15.3f}{:10}\n'.format(usid,nam,dsid,'default_trap',wshd.s[usid].rchlen,0))
        # for t in wshd.xr:
        #     if t in tt: continue
        #     f.write('  {:<10}{:>15}{:15}{:>15}{:15.3f}{:10}\n'.format(t,"s"+str(t),-1,'default_trap',wshd.s[t].rchlen,1))
        f.write(':EndSubBasins\n\n')


        # f.write('####\n') # parameter set uniformly, see SBGroupPropertyOverride below
        # f.write(':SubBasinProperties\n')
        # f.write('# notes: t_conc=MAX_BAS in HBV (t_peak=t_conc/2 for HBV replication)\n')
        # f.write(' :Parameters      TIME_CONC   TIME_TO_PEAK  TIME_LAG\n')
        # f.write(' :Units                   d              d         d\n')
        # for t in wshd.xr:
        #     f.write('  {:<10}{:>15}{:15}{:10}\n'.format(t,par.MAX_BAS,par.MAX_BAS/2,par.TIME_LAG))
        # f.write(':EndSubBasinProperties\n\n')


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
            if lusg=='lake':
                c+=1
                dlakes[t]=c
                f.write('  {:<10}{:10.3f}{:10.1f}{:10.4f}{:10.4f}{:10}{:>20}{:>20}{:>20}          [NONE]         [NONE]{:10.3f}{:10.3f}\n'.format(c,s.km2,s.elv,s.ylat,s.xlng,t,'LAKE','LAKE','LAKE',s.slp,s.asp))
            else:
                for k,frac in lusg.items():
                    c += 1
                    f.write('  {:<10}{:10.3f}{:10.1f}{:10.4f}{:10.4f}{:10}{:>20}{:>20}{:>20}          [NONE]         [NONE]{:10.3f}{:10.3f}\n'.format(c,s.km2*frac,s.elv,s.ylat,s.xlng,t,k[0][0],k[0][1],k[1],s.slp,s.asp))
        f.write(':EndHRUs\n\n')

        # f.write('####\n')
        # f.write(':HRUGroup AllHRUs\n')
        # f.write('  1-{}\n'.format(c))
        # f.write(':EndHRUGroup\n\n')

        if len(dlakes)>0:
            f.write('# create HRU group for lake-types\n')
            f.write(':PopulateHRUGroup LakeHRUs With LANDUSE EQUALS LAKE\n\n')
            f.write('# create HRU group for non-lake HRUs\n')
            f.write(':PopulateHRUGroup LandHRUs With LANDUSE NOTEQUALS LAKE\n\n')
            f.write(':RedirectToFile {}-lakes.rvh\n\n'.format(nam))
            lakes_rvh.write(root, nam, desc, builder, ver, wshd, hrus, dlakes)

            f.write(':SubBasinGroup   AllLakeSubbasins\n')
            rvprint.columns(f,list(dlakes.keys()))
            f.write(':EndSubBasinGroup\n\n')

            f.write(':PopulateSubBasinGroup AllLandSubbasins With SUBBASINS NOTWITHIN AllLakeSubbasins\n\n')
        else:
            f.write(':SubBasinGroup   AllLandSubbasins\n')
            rvprint.columns(f,list(wshd.s.keys()))
            f.write(':EndSubBasinGroup\n\n')           

        f.write('# Set subbasin parameters, notes: t_conc=MAX_BAS in HBV (t_peak=t_conc/2 for HBV replication)\n')
        f.write(':SBGroupPropertyOverride AllLandSubbasins TIME_CONC {}\n'.format(par.MAX_BAS))
        f.write(':SBGroupPropertyOverride AllLandSubbasins TIME_TO_PEAK {}\n'.format(par.MAX_BAS/2))
        f.write(':SBGroupPropertyOverride AllLandSubbasins TIME_LAG {}\n'.format(par.TIME_LAG))
        f.write('\n')