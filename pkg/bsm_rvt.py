
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

# build Time Series Input file (.rvt)
def write(root, nam, desc, builder, ver, met, wshd, writemetfiles=False):
    with open(root + nam + ".rvt","w") as f:
        f.write('# --------------------------------------------\n')
        f.write('# Raven temporal data (.rvt) file\n')
        f.write('# ' + desc + '\n')
        f.write('# built from OWRC-API accessed: {}\n'.format(datetime.now().strftime("%Y-%m-%d")))
        f.write('# written by ' + builder + '\n')
        f.write('# using pyRaven builder\n')
        f.write('# Raven version: ' + ver + '\n')
        f.write('# --------------------------------------------\n\n')

        if writemetfiles:
            mmio.mkDir(root + "input")
            pbar = tqdm(total=len(wshd.s), desc='writing forcings')            
            for sid, s in wshd.s.items():
                f.write(':Gauge met{}\n'.format(sid))
                f.write(' :Latitude {}\n'.format(s.ylat))
                f.write(' :Longitude {}\n'.format(s.xlng))
                f.write(' :Elevation 500\n')
                f.write(' :RedirectToFile input\\m{}.rvt\n'.format(sid))
                f.write(':EndGauge\n\n')
                if writemetfiles: 
                    dtb, dte = getDailyAPI(s.ylat, s.xlng, root+'input\\m{}.rvt'.format(sid))
                    pbar.update()                
            if writemetfiles: pbar.close()

        met.nloc = len(wshd.s)
        met.dtb =  dtb #datetime(1980, 10, 1)
        met.dte =  dte


        # if met.lc == 0:
        #     if writemetfiles: 
        #         mmio.mkDir(root + "input")
        #         pbar = tqdm(total=met.nloc, desc='writing forcings')
        #     for sid, row in met.dfloc.iterrows():
        #         f.write(':Gauge met{}\n'.format(sid))
        #         f.write(' :Latitude {}\n'.format(row['Lat']))
        #         f.write(' :Longitude {}\n'.format(row['Long']))
        #         f.write(' :Elevation 500\n')
        #         f.write(' :RedirectToFile input\\m{}.rvt\n'.format(sid))
        #         f.write(':EndGauge\n\n')
        #         if writemetfiles: 
        #             writeTimeseries(met, sid, root+'input\\m{}.rvt'.format(sid))
        #             pbar.update()
        #     if writemetfiles: pbar.close()
        # else:
        #     pass
        #     ## below was code used for data already interpolated to basins
        #     # if met.nloc == len(wshd.a):
        #     #     if writemetfiles: 
        #     #         mmio.mkDir(root + "input")
        #     #         pbar = tqdm(total=met.nloc, desc='writing forcings')
        #     #     for sid in met.dfloc['id']:
        #     #         s = wshd.s[sid]
        #     #         f.write(':Gauge m{}\n'.format(sid))
        #     #         f.write(' :Latitude {}\n'.format(s.ylat))
        #     #         f.write(' :Longitude {}\n'.format(s.xlng))
        #     #         f.write(' :Elevation {}\n'.format(s.elv))
        #     #         f.write(' :RedirectToFile input\\m{}.rvt\n'.format(sid))
        #     #         f.write(':EndGauge\n\n')
        #     #         if writemetfiles: 
        #     #             writeTimeseries(met, sid, root+'input\\m{}.rvt'.format(sid))
        #     #             pbar.update()
        #     #     if writemetfiles: pbar.close()
        #     # else:
        #     #     pass


