
from datetime import datetime, timedelta
from timeit import default_timer as timer
import pandas as pd
from pymmio import files as mmio
from pyMet.met import Met
from pyGrid.sws import Watershed
from pyRaven import batchfile, rvi_snowmelt, rvp_OneBareLayer, rvh_hru, rvt_dailyJSON, rvc_allZero, parameters #, sta_rvh, sta_rvp, RVT_dailyAPI, sta_rvc, rvbat
from pyRaven.flags import flg

def StationMelt(ins):    

    stmsg = "=== Raven Station Snowmelt builder ==="
    desc = ins.desc
    print("\n" + "="*len(stmsg))
    print(stmsg)
    print("="*len(stmsg) + "\n")
    if len(desc) > 0: print(desc) #"\n{}\n".format(desc))
    b0 = timer()


    # general notes
    root0 = ins.root
    nam = ins.nam
    root = root0 + nam + "\\"
    now = datetime.now()
    builder = 'M. Marchildon ' + now.strftime("%Y-%m-%d %H:%M:%S")
    ver = "3.8"


    # load data
    print("\n\n=== Loading data..")
    if 'station' in ins.params:
        met = importDaily(ins.params['station'])
    elif 'json' in ins.params: # OLD
        met = convertDailyYCDB(ins.params['json'])
    else:
        print('error: need to define input data')
        quit()

    if 'preciponly' in ins.params['options']: flg.preciponly=True

    pars = parameters.getParameters(ins.params)

    # print(met.dftem)    

    wshd = Watershed()

    # make directories   
    mmio.mkDir(root)
    mmio.mkDir(root + "output")


    print("\n=== Writing model files..")
    rvi_snowmelt.write(root, nam, builder, ver, wshd, met)
    rvp_OneBareLayer.write(root, nam, desc, builder, ver, pars) # parameters
    rvh_hru.write(root, nam, desc, builder, ver, wshd) # HRUs    
    rvt_dailyJSON.write(root, nam, desc, builder, ver, met) # temporal
    rvc_allZero.write(root, nam, desc, builder, ver)
    batchfile.write(root, nam, ver)


    endtime = str(timedelta(seconds=round(timer() - b0,0)))
    print('\ntotal elapsed time: ' + endtime)



def convertDailyYCDB(jsonFP):
    # This is old, may need to check
    df = pd.read_json(jsonFP) #  Date  Val  RDNC  RDTC  unit
    df = df.pivot('Date','RDNC','Val').reset_index()
    df['Date'] = df['Date'].dt.date # ASSUMES daily data being injested
    df.columns.name = None
    if not 552 in df: return None

    df.rename(columns={546:'Tx',547:'Tn',548:'Tm',549:'Rf',550:'Sf',551:'Pr',552:'SD'},inplace=True)
    df.set_index('Date',inplace=True)
    df.sort_index(inplace=True)

    met = Met()
    met.dtb = df.apply(pd.Series.first_valid_index)['SD']
    met.dte = df.apply(pd.Series.last_valid_index)['SD']
    dtrng = pd.date_range(met.dtb,met.dte)
    met.dftem = df[met.dtb:met.dte].reindex(dtrng)

    # infill
    met.dftem['Rf'].fillna(0, inplace=True)
    met.dftem['Sf'].fillna(0, inplace=True)
    met.dftem['Tx'].interpolate(inplace=True)
    met.dftem['Tn'].interpolate(inplace=True)

    return met


def importDaily(csvFP):

    df = pd.read_csv(csvFP)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.set_index('Date')
    # print(df)

    met = Met()
    met.dtb = df.apply(pd.Series.first_valid_index)['depth_of_surface_snow']
    met.dte = df.apply(pd.Series.last_valid_index)['depth_of_surface_snow']
    dtrng = pd.date_range(met.dtb,met.dte)
    met.dftem = df[met.dtb:met.dte].reindex(dtrng)

    met.dftem.fillna({'rainfall_amount':0}, inplace=True)
    met.dftem.fillna({'snowfall_amount':0}, inplace=True)
    met.dftem['max_air_temperature'] = met.dftem['max_air_temperature'].interpolate()
    met.dftem['min_air_temperature'] = met.dftem['min_air_temperature'].interpolate()

    met.dftem.rename(columns={"rainfall_amount": "Rf", "snowfall_amount": "Sf", "max_air_temperature": "Tx", "min_air_temperature": "Tn"}, inplace=True)

    return met