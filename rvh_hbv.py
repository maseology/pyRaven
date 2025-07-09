
import shutil
from pymmio import files as mmio
from pyRaven import rvh_hru
from pyRaven.flags import flg

# build HRU/Basin Definition file (.rvh)
def write(root, nam, desc, builder, ver, wshd, hru, res, par):

    if wshd.haschans:
        rvh_hru.writeSemiDistributed(root, nam, desc, builder, ver, wshd, hru, res)
    else:
        rvh_hru.writeSemiDistributed(root, nam, desc, builder, ver, wshd, hru, res, "default_trap")
    
    if flg.calibrationmode:
        shutil.copyfile(root + nam + ".rvh", mmio.getFileDir(root) +"/" + nam + ".rvh.tpl")
        with open(mmio.getFileDir(root) +"/" + nam + ".rvh.tpl","a") as f:    
            f.write('# Set global sub-basin parameters  xLogMAX_PERC_RATE_MULT\n')
            f.write(':SBGroupPropertyOverride AllLandSubbasins TIME_CONC xTIME_CONC\n')
            f.write(':SBGroupPropertyOverride AllLandSubbasins TIME_TO_PEAK xHalfTIME_CONC\n')
            f.write(':SBGroupPropertyOverride AllLandSubbasins TIME_LAG xTIME_LAG\n')
            f.write(':SBGroupPropertyMultiplier  AllLandSubbasins  MAX_PERC_RATE xMAX_PERC_RATE_MULT\n')
            f.write(':SBGroupPropertyMultiplier  AllLandSubbasins  MANNINGS_N {}\n'.format(1.0))
            f.write(':SBGroupPropertyMultiplier  AllLakeSubbasins  RESERVOIR_CREST_WIDTH {}\n'.format(1.0))
            f.write('\n')
    else:
        with open(root + nam + ".rvh","a") as f:    
            f.write('# Set subbasin parameters, notes: TIME_CONC=MAXBAS in HBV (TIME_TO_PEAK=TIME_CONC/2 for HBV replication)\n')
            f.write(':SBGroupPropertyOverride AllLandSubbasins TIME_CONC {}\n'.format(par.TIME_CONC))
            f.write(':SBGroupPropertyOverride AllLandSubbasins TIME_TO_PEAK {}\n'.format(par.TIME_CONC/2))
            f.write(':SBGroupPropertyOverride AllLandSubbasins TIME_LAG {}\n'.format(par.TIME_LAG))
            f.write(':SBGroupPropertyMultiplier  AllLandSubbasins  MAX_PERC_RATE {}\n'.format(par.MAX_PERC_RATE_MULT))
            f.write('#:SBGroupPropertyMultiplier  AllLandSubbasins  MANNINGS_N {}\n'.format(1.0))
            f.write('#:SBGroupPropertyMultiplier  AllLakeSubbasins  RESERVOIR_CREST_WIDTH {}\n'.format(1.0))            
            f.write('\n')