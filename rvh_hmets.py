
from pyRaven import rvh_hru

# build HRU/Basin Definition file (.rvh)
def write(root, nam, desc, builder, ver, wshd, hru, res, calibrationmode=False):

    if wshd.haschans:
        rvh_hru.writeSemiDistributed(root, nam, desc, builder, ver, wshd, hru, res)
    else:
        rvh_hru.writeSemiDistributed(root, nam, desc, builder, ver, wshd, hru, res, "default_trap")
    
    if calibrationmode:
        with open(root + nam + ".rvh","a") as f:    
            f.write('# Set global subbasin parameters\n')
            f.write(':SBGroupPropertyMultiplier  AllLandSubbasins  MAX_PERC_RATE {}\n'.format(1.0))
            f.write(':SBGroupPropertyMultiplier  AllLandSubbasins  MANNINGS_N {}\n'.format(1.0))
            f.write(':SBGroupPropertyMultiplier  AllLakeSubbasins  RESERVOIR_CREST_WIDTH {}\n'.format(1.0))
            f.write('\n')