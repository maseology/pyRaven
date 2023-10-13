
import pandas as pd
from datetime import datetime
from tqdm import tqdm
from pymmio import files as mmio

def getDailyAPI(lat,lng,fp):
    df = pd.read_json("http://golang.oakridgeswater.ca:8080/cmet/{}/{}".format(lat,lng))
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
def write(root, nam, desc, builder, ver, wshd, writemetfiles=False):
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
            f.write(' :Elevation {}\n'.format(s.elev))
            f.write(' :RedirectToFile input\\m{}.rvt\n'.format(t))
            f.write(':EndGauge\n\n')
            if writemetfiles: getDailyAPI(s.ylat, s.xlng, root+'input\\m{}.rvt'.format(t))
            pbar.update()                
        pbar.close()