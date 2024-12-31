
from pyRaven import rvh_hru

# build HRU/Basin Definition file (.rvh)
def write(root, nam, desc, builder, ver, wshd, hru, res, par):

    rvh_hru.writeSemiDistributed(root, nam, desc, builder, ver, wshd, hru, res, "default_trap")
    
    with open(root + nam + ".rvh","a") as f:    
        f.write('# Set global subbasin parameters\n')
        f.write(':SBGroupPropertyMultiplier  Allsubbasins      MANNINGS_N {}\n'.format(1.0))
        f.write(':SBGroupPropertyMultiplier  AllLakesubbasins  RESERVOIR_CREST_WIDTH {}\n'.format(1.0))
        f.write('\n')