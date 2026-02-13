
import os, shutil
import pandas as pd
import numpy as np
from datetime import datetime
from pymmio import files as mmio
from pyRaven.flags import flg

def writeDailyMet(met, outfp):
    dtb = met.index.min()

    with open(outfp,"w") as f:
        f.write(':MultiData\n')
        f.write(' {} {} {}\n'.format(dtb.strftime("%Y-%m-%d %H:%M:%S"), 1, len(met.index)))
        if flg.preciponly or flg.precipactive:
            f.write(' :Parameters  TEMP_MAX  TEMP_MIN    PRECIP\n')
            f.write(' :Units              C         C      mm/d\n')
        else:
            f.write(' :Parameters  TEMP_MAX  TEMP_MIN  RAINFALL  SNOWFALL\n') # *** wbdc ordered ***
            f.write(' :Units              C         C      mm/d      mm/d\n')

        for _, row in met.iterrows():
            # NOTE: "+0"   https://stackoverflow.com/questions/11010683/how-to-have-negative-zero-always-formatted-as-positive-zero-in-a-python-string
            if flg.precipactive:
                f.write('            {:>10.2f}{:>10.2f}{:>10.1f}\n'.format(round(row['Tx'],2)+0, round(row['Tn'],2)+0, row['Rf']+row['Sm']))
            elif flg.preciponly:
                f.write('            {:>10.2f}{:>10.2f}{:>10.1f}\n'.format(round(row['Tx'],2)+0, round(row['Tn'],2)+0, row['Rf']+row['Sf']))
            else:
                f.write('            {:>10.2f}{:>10.2f}{:>10.1f}{:>10.1f}\n'.format(round(row['Tx'],2)+0, round(row['Tn'],2)+0, row['Rf'], row['Sf']))       
            
        f.write(':EndMultiData\n\n')        


def writeDailyObs(hyd, outfp):
    # hyd = pd.read_csv(infp, parse_dates=["Date"])[['Date','Flow']].set_index('Date')

    dtb = hyd.index.min()
    dte = hyd.index.max()
    hyd = hyd.reindex(pd.date_range(dtb,dte), fill_value=-1.2345)
    with open(outfp,"w") as f:
        f.write(":ObservationData HYDROGRAPH 1 m3/s\n")
        f.write(' {} 1.0 {}\n'.format(dtb.strftime("%Y-%m-%d %H:%M:%S"), len(hyd)))
        for v in hyd.Flow:
            if np.isnan(v):
                f.write('  -1.2345\n')
            else:
                # NOTE: "+0"   https://stackoverflow.com/questions/11010683/how-to-have-negative-zero-always-formatted-as-positive-zero-in-a-python-string
                vv=round(v,3)+0
                if vv<0:
                    f.write('  -1.2345\n')
                else:
                    f.write('  {:.4f}\n'.format(vv))        
        f.write(':EndObservationData')


# append to Time Series Input file (.rvt)
#   Note: dftem read from csv file "S:\lumped\dat\02EC010.csv"  "Date","Flow","Flag","Tx","Tn","Rf","Sf","Sm"
def write(root, nam, desc, builder, ver, wshd, dftem, submdl=False):
    if dftem.empty: return
    indir = 'input'
    if submdl: indir = '..\\'+indir
    with open(root + nam + ".rvt","w") as f:
        f.write('# --------------------------------------------\n')
        f.write('# Raven temporal data (.rvt) file\n')
        f.write('# ' + desc + '\n')
        # f.write('# built from OWRC-API accessed: {}\n'.format(datetime.now().strftime("%Y-%m-%d")))
        f.write('# written by ' + builder + '\n')
        f.write('# using pyRaven builder\n')
        f.write('# Raven version: ' + ver + '\n')
        f.write('# --------------------------------------------\n\n')

        ofp = '{}\\met.rvt'.format(indir)
        f.write(':Gauge met\n')
        f.write(' :Latitude     {:10.3f}\n'.format(wshd.s[1].ylat))
        f.write(' :Longitude    {:10.3f}\n'.format(wshd.s[1].xlng))
        f.write(' :Elevation    {:10.3f}\n'.format(wshd.s[1].elv))
        f.write(' :RedirectToFile   {}\n'.format(ofp))
        f.write(':EndGauge\n\n')
        writeDailyMet(dftem, root+ofp)

        ofp = '{}\\gag.rvt'.format(indir)
        f.write(':RedirectToFile    '+ofp+'\n')
        if not os.path.exists(ofp): writeDailyObs(dftem, root+ofp)
