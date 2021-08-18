
# import os
from datetime import datetime, timedelta
import re
from timeit import default_timer as timer
import pandas as pd
from pymmio import files as mmio
from pyMet.met import Met
# from pyGrid.hdem import HDEM
from pyGrid.sws import Watershed
from pkg import rvi_snowmelt, rvp_OneBareLayer, rvh_hru, rvt_dailyJSON, rvc_allZero, rvbat #, sta_rvh, sta_rvp, RVT_dailyAPI, sta_rvc, rvbat


def convertDailyYCDB(jsonFP):
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
    ver = "3.0"

    # # read options
    # # params = sta_params.Params
    # writemetfiles = not os.path.exists(root + "input")
    # if 'options' in ins.params:
    #     if 'overwritetemporalfiles' in ins.params['options']:
    #         writemetfiles = ins.params['options']['overwritetemporalfiles'] 

    # load data
    print("\n\n=== Loading data..")
    met = convertDailyYCDB(ins.params['json'])
    # print(met.dftem)    

    wshd = Watershed()

    # make directories   
    mmio.mkDir(root)
    mmio.mkDir(root + "output")


    print("\n=== Writing model files..")
    rvi_snowmelt.write(root, nam, builder, ver, wshd, met)
    rvp_OneBareLayer.write(root, nam, desc, builder, ver) # parameters
    rvh_hru.write(root, nam, desc, builder, ver, wshd) # HRUs    
    rvt_dailyJSON.write(root, nam, desc, builder, ver, met) # temporal
    rvc_allZero.write(root, nam, desc, builder, ver)
    rvbat.write(root, nam, ver)


    endtime = str(timedelta(seconds=round(timer() - b0,0)))
    print('\ntotal elapsed time: ' + endtime)