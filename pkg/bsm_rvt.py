
import re
import numpy as np
from tqdm import tqdm
from pymmio import files as mmio

def writeTimeseries(met,sid,fp):
    # def rnz(a): return a if a != 0 else abs(a) # remove negative zero

    if met.lc == 0:
        with open(fp,"w") as f:
            f.write(':MultiData\n')
            f.write(' {} {} {}\n'.format(met.dtb.strftime("%Y-%m-%d %H:%M:%S"), met.intvl/86400, len(met.dftem[sid])))
            f.write(' :Parameters  TEMP_MAX  TEMP_MIN  RAINFALL  SNOWFALL\n') # *** wbdc ordered ***
            f.write(' :Units              C         C      mm/d      mm/d\n')
        
            for t in met.dftem[sid]:
                # NOTE: "+0"   https://stackoverflow.com/questions/11010683/how-to-have-negative-zero-always-formatted-as-positive-zero-in-a-python-string
                f.write('            {:>10.2f}{:>10.2f}{:>10.1f}{:>10.1f}\n'.format(round(t[0],2)+0, round(t[0],2)+0, t[2]*1000, t[3]*1000))
            f.write(':EndMultiData\n\n')
    else:
        pass
        # # below was code used for data already interpolated to basins, dftem is a pandas df
        # ss = met.dftem[sid][['Rainfall','Snowfall','MinDailyT','MaxDailyT']]
        # sss = ss.to_numpy().round(3) +0  # https://stackoverflow.com/questions/11010683/how-to-have-negative-zero-always-formatted-as-positive-zero-in-a-python-string

        # # tupmet = [tuple(x) for x in ss.to_numpy()]        
        # tupmet = [tuple(x) for x in sss]

        # with open(fp,"w") as f:
        #     f.write(':MultiData\n')
        #     f.write(' {} {} {}\n'.format(met.dtb.strftime("%Y-%m-%d %H:%M:%S"), met.intvl/86400, len(tupmet)))
        #     f.write(' :Parameters  RAINFALL  SNOWFALL  TEMP_MIN  TEMP_MAX\n')
        #     f.write(' :Units           mm/d      mm/d         C         C\n')   
        #     c = 0
        #     for t in tupmet:
        #         # tn = round(t[2],3) +0 
        #         # tx = round(t[3],3) +0
        #         # if c>=12598: 
        #         #     print('{:>10.3f}'.format(t[3]))
        #         #     print()
        #         #     pass
        #         f.write('            {:>10.1f}{:>10.1f}{:>10.3f}{:>10.3f}\n'.format( t[0]*1000, t[1]*1000, t[2], t[3]))
        #         c += 1
        #     f.write(':EndMultiData\n\n')            

# build Time Series Input file (.rvt)
def write(root, nam, desc, builder, ver, met, wshd=None, writemetfiles=False):
    with open(root + nam + ".rvt","w") as f:
        f.write('# --------------------------------------------\n')
        f.write('# Raven temporal data (.rvt) file\n')
        f.write('# ' + desc + '\n')
        f.write('# built from ' + met.filepath +'\n')
        f.write('# written by ' + builder + '\n')
        f.write('# using pyRaven builder\n')
        f.write('# Raven version: ' + ver + '\n')
        f.write('# --------------------------------------------\n\n')

        if met.lc == 0:
            if writemetfiles: 
                mmio.mkDir(root + "input")
                pbar = tqdm(total=met.nloc, desc='writing forcings')
            for sid, row in met.dfloc.iterrows():
                f.write(':Gauge met{}\n'.format(sid))
                f.write(' :Latitude {}\n'.format(row['Lat']))
                f.write(' :Longitude {}\n'.format(row['Long']))
                f.write(' :Elevation 500\n')
                f.write(' :RedirectToFile input\\m{}.rvt\n'.format(sid))
                f.write(':EndGauge\n\n')
                if writemetfiles: 
                    writeTimeseries(met, sid, root+'input\\m{}.rvt'.format(sid))
                    pbar.update()
            if writemetfiles: pbar.close()
        else:
            pass
            ## below was code used for data already interpolated to basins
            # if met.nloc == len(wshd.a):
            #     if writemetfiles: 
            #         mmio.mkDir(root + "input")
            #         pbar = tqdm(total=met.nloc, desc='writing forcings')
            #     for sid in met.dfloc['id']:
            #         s = wshd.s[sid]
            #         f.write(':Gauge m{}\n'.format(sid))
            #         f.write(' :Latitude {}\n'.format(s.ylat))
            #         f.write(' :Longitude {}\n'.format(s.xlng))
            #         f.write(' :Elevation {}\n'.format(s.elv))
            #         f.write(' :RedirectToFile input\\m{}.rvt\n'.format(sid))
            #         f.write(':EndGauge\n\n')
            #         if writemetfiles: 
            #             writeTimeseries(met, sid, root+'input\\m{}.rvt'.format(sid))
            #             pbar.update()
            #     if writemetfiles: pbar.close()
            # else:
            #     pass


