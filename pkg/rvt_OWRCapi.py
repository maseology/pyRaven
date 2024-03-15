import os
import pandas as pd
from datetime import datetime
from tqdm import tqdm
from pymmio import files as mmio
from pkg.rvt_Obs import writeDailyObs


def getDailyAPI(lat,lng,fp):
    df = pd.read_json("http://fews.oakridgeswater.ca:8080/dymetp/{}/{}".format(lat,lng)) #("http://golang.oakridgeswater.ca:8080/cmet/{}/{}".format(lat,lng))
    dtb = df['Date'].iloc[0]
    dte = df['Date'].iloc[-1]
    with open(fp,"w") as f:
        f.write(':MultiData\n')
        f.write(' {} {} {}\n'.format(dtb.strftime("%Y-%m-%d %H:%M:%S"), 1, len(df.index)))
        f.write(' :Parameters  TEMP_MAX  TEMP_MIN  RAINFALL  SNOWFALL\n') # *** wbdc ordered ***
        f.write(' :Units              C         C      mm/d      mm/d\n')

        for _, row in df.iterrows():
            # NOTE: "+0"   https://stackoverflow.com/questions/11010683/how-to-have-negative-zero-always-formatted-as-positive-zero-in-a-python-string
            f.write('            {:>10.2f}{:>10.2f}{:>10.1f}{:>10.1f}\n'.format(round(row['Tx'],2)+0, round(row['Tn'],2)+0, row['Rf'], row['Sf']))
        f.write(':EndMultiData\n\n')        
    return dtb, dte


def get6hourlyAPI(lat,lng,fp):
    df = pd.read_json("http://fews.oakridgeswater.ca:8080/h6metp/{}/{}".format(lat,lng)) #("http://golang.oakridgeswater.ca:8080/cmet/{}/{}".format(lat,lng))
    dtb = df['Date'].iloc[0]
    dte = df['Date'].iloc[-1]
    with open(fp,"w") as f:
        f.write(':MultiData\n')
        f.write(' {} {} {}\n'.format(dtb.strftime("%Y-%m-%d %H:%M:%S"), 0.25, len(df.index)))
        f.write(' :Parameters  TEMP_AVE  AIR_PRES   REL_HUMIDITY  WIND_VEL       PET  RAINFALL  SNOWFALL POTENTIAL_MELT\n') # *** wbdc ordered ***
        f.write(' :Units              C       kPa              -       m/s      mm/d      mm/d      mm/d           mm/d\n')

        for _, row in df.iterrows():
            # NOTE: "+0"   https://stackoverflow.com/questions/11010683/how-to-have-negative-zero-always-formatted-as-positive-zero-in-a-python-string
            f.write('            {:>10.1f}{:>10.2f}{:>15.3f}{:>10.2f}{:>10.1f}{:>10.1f}{:>10.1f}{:>15.1f}\n'.format(round(row['Ta'],2)+0, round(row['Pa'],2), row['Rh'], row['Us'], row['Pe']*4, row['Rf']*4, row['Sf']*4, row['Sm']*4))
        f.write(':EndMultiData\n\n')        
    return dtb, dte


def writeGaugeWeightTable(root, wshd):
    c = 0
    n = len(wshd.xr)
    with open(root + 'GaugeWeightTable.txt',"w") as f:
        f.write(':GaugeWeightTable\n')
        f.write(' {} {}\n'.format(n,n))
        for _ in wshd.xr:
            a = [0.] * n
            a[c] = 1.
            f.write(' ' + ' '.join([str(v) for v in a]) + '\n')
            c += 1
        f.write(':EndGaugeWeightTable\n')

# build Time Series Input file (.rvt)
def write(root, nam, desc, builder, ver, wshd, obsFP, ts, writemetfiles=False):
    writeGaugeWeightTable(root, wshd)
    with open(root + nam + ".rvt","w") as f:
        f.write('# --------------------------------------------\n')
        f.write('# Raven temporal data (.rvt) file\n')
        f.write('# ' + desc + '\n')
        f.write('# built from OWRC-API accessed: {}\n'.format(datetime.now().strftime("%Y-%m-%d")))
        f.write('# written by ' + builder + '\n')
        f.write('# using pyRaven builder\n')
        f.write('# Raven version: ' + ver + '\n')
        f.write('# --------------------------------------------\n\n')

        mmio.mkDir(root + "input")
        pbar = tqdm(total=len(wshd.s), desc='writing forcings')            
        for t in wshd.xr:
            s = wshd.s[t] 
            f.write(':Gauge met{}\n'.format(t))
            f.write(' :Latitude {}\n'.format(s.ylat))
            f.write(' :Longitude {}\n'.format(s.xlng))
            f.write(' :Elevation {}\n'.format(s.elv))
            f.write(' :RedirectToFile input\\m{}.rvt\n'.format(t))
            f.write(':EndGauge\n\n')
            if writemetfiles: 
                if ts==84600:
                    getDailyAPI(s.ylat, s.xlng, root+'input\\m{}.rvt'.format(t))
                elif ts==21600:
                    get6hourlyAPI(s.ylat, s.xlng, root+'input\\m{}.rvt'.format(t))
            pbar.update()                
        pbar.close()

        if len(obsFP)>0:
            ofp = "input\\o{}.rvt".format(mmio.getFileName(obsFP))
            f.write(' :RedirectToFile {}\n'.format(ofp))
            swsID = wshd.outlets()[0]
            if not os.path.exists(ofp): writeDailyObs(obsFP, root+ofp, swsID)