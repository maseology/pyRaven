
import math
from pyRaven import print, rvh_lakes
from pyRaven.flags import flg

# build HRU/Basin Definition file (.rvh)
def write(root, nam, desc, builder, ver, wshd):
    if len(wshd.xr) > 1:
        writeLumped(root, nam, desc, builder, ver, wshd)        
    else:
        writeOne(root, nam, desc, builder, ver)

# 1 basin, 1 HRU
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

# Many basins, 1 HRU per basin
def writeLumped(root, nam, desc, builder, ver, wshd):
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

# Many basin, land and lake HRUs only
def writeLandLake():
    pass # TODO

def writeSemiDistributed(root, nam, desc, builder, ver, wshd, hru, res, chanprofile=''):
    hrulakes = dict()
    with open(root + nam + ".rvh","w") as f:    
        f.write('# --------------------------------------------\n')
        f.write('# Raven HRU Definition (.rvh) file\n')
        f.write('# ' + desc + '\n')
        f.write('# written by ' + builder + '\n')
        f.write('# using pyRaven builder\n')
        f.write('# Raven version: ' + ver + '\n')
        f.write('# --------------------------------------------\n\n')

        # ID:            A positive long integer identifier unique to this subbasin.
        # NAME:          A nickname for subbasin. DEFAULT string("sub_" + ID).
        # DOWNSTREAM_ID: The ID of the subbasin that receives this subbasins outflowing waters.
        # PROFILE:       The representative channel profile code (channel profiles specified in the channel_properties.rvp file). DEFAULT string("chn_" + ID)
        # REACH_LENGTH:  The length of the primary reach channel in the basin (in km). If set to _AUTO, the reach length will be estimated from total subbasin area.
        # GAUGED:        Flag which determines whether modeled hydrographs for this subbasin are generated as output from the model (either 1 or 0, true or false). In this routing model, both the subbasins with reservoir and flow gauge are set as GAUGED = 1.
        f.write('####\n')
        f.write(':SubBasins\n')
        f.write(' :Attributes                               NAME  DOWNSTREAM_ID        PROFILE   REACH_LENGTH    GAUGED\n')
        f.write(' :Units                                    none           none           none             km      none\n')

        for usid,h in hru.hrus.items():
            dsid = -1
            if usid in wshd.t: dsid = wshd.t[usid]
            if not dsid in hru.hrus: dsid = -1

            # gauged?
            gag = 0
            if len(wshd.gag)>0: 
                if len(wshd.gag[usid])>0: gag = 1

            if res is not None and usid in res: gag = 1 # watershed is reservoir

            # watershed name
            wnam = wshd.nam[usid]
            cmnt = '' # comment
            if len(wshd.gag[usid])>0: cmnt = '  # '+wshd.gag[usid]

            if len(chanprofile) > 0:
                if h=="lake":
                    f.write('  {:<10}{:>35}{:15}{:>15}{:>15}{:10}{}\n'.format(usid,wnam,dsid,chanprofile,'ZERO-',gag,cmnt))
                else:
                    f.write('  {:<10}{:>35}{:15}{:>15}{:15.3f}{:10}{}\n'.format(usid,wnam,dsid,chanprofile,wshd.s[usid].rchlen,gag,cmnt))
            else:
                if h=="lake":
                    f.write('  {:<10}{:>35}{:15}{:>15}{:>15}{:10}{}\n'.format(usid,wnam,dsid,'lak_{}'.format(usid),'ZERO-',gag,cmnt))
                else:
                    f.write('  {:<10}{:>35}{:15}{:>15}{:15.3f}{:10}{}\n'.format(usid,wnam,dsid,'chn_{}'.format(usid),wshd.s[usid].rchlen,gag,cmnt))


        # tt = set()
        # for usid,dsid in wshd.t.items():
        #     if dsid<=0: continue
        #     tt.add(usid)
        #     f.write('  {:<10}{:>15}{:15}{:>15}{:15.3f}{:10}\n'.format(usid,wnam,dsid,chanprofile,wshd.s[usid].rchlen,0))
        # for t in wshd.xr:
        #     if t in tt: continue
        #     f.write('  {:<10}{:>15}{:15}{:>15}{:15.3f}{:10}\n'.format(t,"s"+str(t),-1,chanprofile,wshd.s[t].rchlen,1))
        f.write(':EndSubBasins\n\n')


        # f.write('####\n') # parameter set uniformly, see SBGroupPropertyOverride below
        # f.write(':SubBasinProperties\n')
        # f.write('# notes: t_conc=MAX_BAS in HBV (t_peak=t_conc/2 for HBV replication)\n')
        # f.write(' :Parameters      TIME_CONC   TIME_TO_PEAK  TIME_LAG\n')
        # f.write(' :Units                   d              d         d\n')
        # for t in wshd.xr:
        #     f.write('  {:<10}{:>15}{:15}{:10}\n'.format(t,par.MAX_BAS,par.MAX_BAS/2,par.TIME_LAG))
        # f.write(':EndSubBasinProperties\n\n')


        # HRU ID:          A positive integer unique to this HRU. Note that More than one HRUs may have the same subbasin ID, but HRU ID is unique.
        # AREA:            HRU area value, in km2.
        # ELEVATION:       HRU mean elevation, in m.
        # LATITUDE:        Lattitude of HRU centroid, in decimal degrees.
        # LONGITUDE:       longitude of HRU centroid, in decimal degrees.
        # BASIN_ID:        The ID of the subbasin in which the HRU is located (as defined in the :SubBasins command).
        # LAND_USE_CLASS:  Land use classes defined in Lievre.rvp file. DEFAULT LandHRU_landuse_class or LakeHRU_landuse_class for land and lake HRU, respectively.
        # VEG_CLASS:       Vegetation classes defined in Lievre.rvp file. DEFAULT LandHRU_vege_class or LakeHRU_vege_class for land and lake HRU, respectively.
        # SOIL_PROFILE:    Soil profile defined in Lievre.rvp file. DEFAULT LandHRU_soil_profile or LAKE                 for land and lake HRU, respectively.
        # AQUIFER_PROFILE: Aquifer classes defined in Lievre.rvp file. DEFAULT [NONE] in this routing model.
        # TERRAIN_CLASS:   Terrain classes defined in Lievre.rvp file. DEFAULT [NONE] in this routing model.
        # SLOPE:           HRU mean slope, in degrees.
        # ASPECT:          HRU mean aspect, in degrees. Northern:0°, western: 90°, southern: 180°, eastern: 270°. 
        f.write('####\n')
        f.write(':HRUs\n')
        f.write(' :Attributes      AREA ELEVATION  LATITUDE LONGITUDE  BASIN_ID      LAND_USE_CLASS           VEG_CLASS        SOIL_PROFILE AQUIFER_PROFILE  TERRAIN_CLASS     SLOPE    ASPECT\n') # aspect deg CCWN (west=90°)
        f.write(' :Units            km2         m       deg       deg      none                none                none                none            none           none       deg      degN\n')
        c = 0
        # for t in wshd.xr:
        #     c += 1
        #     s = wshd.s[t]            
        #     f.write('  {:<10}{:10.3f}{:10.1f}{:10.1f}{:10.1f}{:10}         LU_ALL        VEG_ALL      DEFAULT_P          [NONE]         [NONE]{:10.3f}{:10.3f}\n'.format(c,s.km2,s.elv,s.ylat,s.xlng,t,s.slp,s.asp))
        def rad2deg(rad): return (rad/math.pi*180.) % 360
        
        for t,lusg in hru.hrus.items(): # write lake hrus first to enable simple alternative land use mapping changes
            if lusg=='lake':
                s = wshd.s[t]
                c+=1
                hrulakes[t]=c
                f.write('  {:<10}{:10.4f}{:10.1f}{:10.4f}{:10.4f}{:10}{:>20}{:>20}{:>20}          [NONE]         [NONE]{:10.3f}{:10.3f}\n'.format(c,s.km2,s.elv,s.ylat,s.xlng,t,'LAKE','LAKE','LAKE',0.,0.))

        for t,lusg in hru.hrus.items():            
            if lusg=='lake': continue
            xyz = hru.xyzga[t]
            s = wshd.s[t]
            for k,frac in lusg.items():
                c += 1
                zz = k[1][0]
                if flg.gwzonemode: zz+=str(k[1][1]) # soiltype + zone
                f.write('  {:<10}{:10.4f}{:10.1f}{:10.4f}{:10.4f}{:10}{:>20}{:>20}{:>20}          [NONE]         [NONE]{:10.3f}{:10.3f}\n'.format(c,s.km2*frac,xyz[k][2],xyz[k][1],xyz[k][0],t,k[0][0],k[0][1],zz,rad2deg(xyz[k][3]),rad2deg(xyz[k][4]-math.pi/2)))
        
        f.write(':EndHRUs\n\n')

        # f.write('# create all HRU group\n')
        # f.write(':HRUGroup AllHRUs\n')
        # f.write('  1-{}\n'.format(c))
        # f.write(':EndHRUGroup\n\n')

        if len(hrulakes)>0:
            f.write('# create HRU group for lake-types\n')
            f.write(':PopulateHRUGroup LakeHRUs With LANDUSE EQUALS LAKE\n\n')
            f.write('# create HRU group for non-lake HRUs\n')
            f.write(':PopulateHRUGroup LandHRUs With LANDUSE NOTEQUALS LAKE\n\n')

            f.write('# create SubBasin group for lake-types\n')
            f.write(':SubBasinGroup   AllLakeSubbasins\n')
            print.columns(f,list(hrulakes.keys()))
            f.write(':EndSubBasinGroup\n\n')
            f.write('# create SubBasin group for non-lake HRUs\n')
            f.write(':PopulateSubBasinGroup AllLandSubbasins With SUBBASINS NOTWITHIN AllLakeSubbasins\n\n')

            f.write(':RedirectToFile {}-lakes.rvh\n\n'.format(nam))
            rvh_lakes.write(root, nam, desc, builder, ver, wshd, hru, hrulakes, res)
        else:
            f.write(':SubBasinGroup   AllLandSubbasins\n')
            print.columns(f,list(wshd.s.keys()))
            f.write(':EndSubBasinGroup\n\n')      

        if len(wshd.zon)>0:
            grps = [int(i) for i in list(set(wshd.zon.values()))]
            grps.sort()
            for g in grps:
                ll = list()
                for si,zi in wshd.zon.items():
                    if zi==g: ll.append(si)
                f.write(':SubBasinGroup   UserGroup{:03d}\n'.format(g))
                print.columns(f,ll)
                f.write(':EndSubBasinGroup\n\n')