
import os
import pandas as pd
from datetime import datetime
from tqdm import tqdm
from pyRaven.flags import flg


def getDailyAPI(fp,lat=None,lng=None,cid=None):
    if cid is not None:
        url = "http://fews.oakridgeswater.ca:8080/dymetp/{}".format(cid)
        try:
            df = pd.read_json(url)
        except:
            url = "http://fews.oakridgeswater.ca:8080/dymetp/{}/{}".format(lat,lng)
            df = pd.read_json(url)        
    else:
        url = "http://fews.oakridgeswater.ca:8080/dymetp/{}/{}".format(lat,lng)
        df = pd.read_json(url)

    dtb = df['Date'].iloc[0]
    dte = df['Date'].iloc[-1]
    with open(fp,"w") as f:
        f.write(':MultiData\n')
        f.write(' {} {} {}\n'.format(dtb.strftime("%Y-%m-%d %H:%M:%S"), 1, len(df.index)))
        if flg.preciponly:
            f.write(' :Parameters  TEMP_MAX  TEMP_MIN    PRECIP\n')
            f.write(' :Units              C         C      mm/d\n')
        else:
            f.write(' :Parameters  TEMP_MAX  TEMP_MIN  RAINFALL  SNOWFALL\n') # *** wbdc ordered ***
            f.write(' :Units              C         C      mm/d      mm/d\n')

        for _, row in df.iterrows():
            # NOTE: "+0"   https://stackoverflow.com/questions/11010683/how-to-have-negative-zero-always-formatted-as-positive-zero-in-a-python-string
            if flg.preciponly:
                f.write('            {:>10.2f}{:>10.2f}{:>10.1f}\n'.format(round(row['Tx'],2)+0, round(row['Tn'],2)+0, row['Rf']+row['Sf']))
            else:
                f.write('            {:>10.2f}{:>10.2f}{:>10.1f}{:>10.1f}\n'.format(round(row['Tx'],2)+0, round(row['Tn'],2)+0, row['Rf'], row['Sf']))       
            
        f.write(':EndMultiData\n\n')        
    return dtb, dte


def get6hourlyAPI(fp,lat=None,lng=None,cid=None):
    if cid is None:
        df = pd.read_json("http://fews.oakridgeswater.ca:8080/h6metp/{}/{}".format(lat,lng)) #("http://golang.oakridgeswater.ca:8080/cmet/{}/{}".format(lat,lng))
    else:
        df = pd.read_json("http://fews.oakridgeswater.ca:8080/h6metp/{}".format(cid))
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


def writeGaugeWeightTable(root, nam, wshd, hru):
    def buildXR():
        c = 0
        xr = dict()
        for t in wshd.xr:
            xr[t]=c
            c += 1
        return xr
    xr = buildXR()
    ng=len(hru.hrus)
    with open(root + nam + "-GaugeWeightTable.txt","w") as f:
        f.write(':GaugeWeightTable\n')
        f.write(' {} {}\n'.format(ng,hru.nhru))
        for t,a in hru.hrus.items():
            a = [0.] * ng
            a[xr[t]] = 1.            
            for _ in a:
                f.write(' ' + ' '.join([str(v) for v in a]) + '\n')
        f.write(':EndGaugeWeightTable\n')
    # c = 0
    # n = len(wshd.xr)
    # with open(root + nam + "-GaugeWeightTable.txt","w") as f:
    #     f.write(':GaugeWeightTable\n')
    #     f.write(' {} {}\n'.format(n,n))
    #     for _ in wshd.xr:
    #         a = [0.] * n
    #         a[c] = 1.
    #         f.write(' ' + ' '.join([str(v) for v in a]) + '\n')
    #         c += 1
    #     f.write(':EndGaugeWeightTable\n')


# build Time Series Input file (.rvt)
def write(root, nam, desc, builder, ver, wshd, hru, ts, submdl=False):
    # writeGaugeWeightTable(root, nam, wshd, hru)
    indir = 'input'
    if submdl: indir = '..\\'+indir
    with open(root + nam + ".rvt","w") as f:
        f.write('# --------------------------------------------\n')
        f.write('# Raven temporal data (.rvt) file\n')
        f.write('# ' + desc + '\n')
        f.write('# built from OWRC-API accessed: {}\n'.format(datetime.now().strftime("%Y-%m-%d")))
        f.write('# written by ' + builder + '\n')
        f.write('# using pyRaven builder\n')
        f.write('# Raven version: ' + ver + '\n')
        f.write('# --------------------------------------------\n\n')

        for t,s in wshd.s.items():
            # s = wshd.s[t] 
            f.write(':Gauge met{}\n'.format(t))
            f.write(' :Latitude  {:10.3f}\n'.format(s.ylat))
            f.write(' :Longitude {:10.3f}\n'.format(s.xlng))
            f.write(' :Elevation {:10.3f}\n'.format(s.elv))
            f.write(' :RedirectToFile {}\\m{}.rvt\n'.format(indir,t))
            f.write(':EndGauge\n\n')

        # flg.writemetfiles = True
        if flg.writemetfiles:
            pbar = tqdm(total=len(wshd.s), desc='writing forcings')            
            for t,s in wshd.s.items():
                # if os.path.exists(root+'input\\m{}.rvt'.format(t)) : continue
                # s = wshd.s[t] 
                if ts==86400:
                    # getDailyAPI(root+'input\\m{}.rvt'.format(t), cid=t)
                    # getDailyAPI(root+'input\\m{}.rvt'.format(t), lat=s.ylat, lng=s.xlng) #, cid=t)
                    getDailyAPI(root+'input\\m{}.rvt'.format(t), lat=s.ylat, lng=s.xlng, cid=t)
                elif ts==21600:
                    if flg.preciponly: print("----------- preciponly TODO")
                    get6hourlyAPI(root+'input\\m{}.rvt'.format(t), s.ylat, s.xlng)
                else:
                    print("rvt_OWRCapi.write WARNING: unsupported timestep {}".format(ts))
                pbar.update()                
            pbar.close()