
from pyRaven import rvh_hru

# build HRU/Basin Definition file (.rvh)
def write(root, nam, desc, builder, ver, wshd, hru, res, par):

    rvh_hru.writeSemiDistributed(root, nam, desc, builder, ver, wshd, hru, res, "default_trap")
    
    with open(root + nam + ".rvh","a") as f:    
        f.write('# Set subbasin parameters, notes: TIME_CONC=MAXBAS in HBV (TIME_TO_PEAK=TIME_CONC/2 for HBV replication)\n')
        f.write(':SBGroupPropertyOverride AllLandSubbasins TIME_CONC {}\n'.format(par.TIME_CONC))
        f.write(':SBGroupPropertyOverride AllLandSubbasins TIME_TO_PEAK {}\n'.format(par.TIME_CONC/2))
        f.write(':SBGroupPropertyOverride AllLandSubbasins TIME_LAG {}\n'.format(par.TIME_LAG))
        f.write('\n')