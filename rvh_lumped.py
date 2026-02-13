
import time
from pyRaven.flags import flg

# build lumped hru file (.rvh)
def write(root, nam, desc, builder, ver, wshd):

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
        s = wshd.s[1]
        f.write('####\n')
        f.write(':SubBasins\n')
        f.write(' :Attributes                               NAME  DOWNSTREAM_ID        PROFILE   REACH_LENGTH    GAUGED\n')
        f.write(' :Units                                    none           none           none             km      none\n')
        f.write('  {:<10}{:>35}{:15}{:>15}{:15}{:10}\n'.format(1,nam,-1,'NONE','_AUTO',1))
        f.write(':EndSubBasins\n\n')


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
        f.write('  {:<10}{:10.4f}{:10.1f}{:10.4f}{:10.4f}{:10}{:>20}{:>20}{:>20}          [NONE]         [NONE]{:10.3f}{:10.3f}\n'.format(1,s.km2,s.elv,s.ylat,s.xlng,1,'luclass','vegclass','soilclass',s.slp,s.asp))
        f.write(':EndHRUs\n\n')

        # f.write('####\n')
        # f.write(':HRUGroup AllHRUs\n')
        # f.write('  1-{}\n'.format(c))
        # f.write(':EndHRUGroup\n\n')

