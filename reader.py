
from datetime import datetime
import pandas as pd
import numpy as np

from pymmio import ascii
from pyGrid.indx import INDX
from pyGrid.hdem import HDEM
from pyGrid.sws import Watershed
from pyInstruct import instruct

from pkg import hbv_params, hru, solris3, surfgeo_OGS



insfp = "M:/OWRC-Raven/OWRC23.raven" # "M:\\Peel\\Raven-PWRMM21\\PWRMM21.raven"



ins = instruct.build(insfp)
ofp = ins.root+"{}/output/{}_TO_SOIL[2]_Monthly_Average_ByHRU.csv".format(ins.nam,ins.nam)
params = hbv_params.Params
if 'options' in ins.params:
    if 'minhrufrac' in ins.params['options']:
        params.hru_minf = float(ins.params['options']['minhrufrac'])
    if 'lakehruthresh' in ins.params['options']:
        params.hru_min_lakef = float(ins.params['options']['lakehruthresh']) 


dateparser = lambda x: datetime.strptime(x, "%Y-%m") # lambda x: datetime.strptime(x, "%b-%y")
df = pd.read_csv(ofp, skiprows=1, parse_dates=['month'], date_parser=dateparser)
# df = pd.read_csv(ofp, skiprows=1, parse_dates=['month'], date_format="%b-%y")

df['month'] = df['month'].dt.month

# change accumulation to discreet monthly values
df2 = df.diff()
df2['month'] = np.NaN
df2 = df2.fillna(df)
print(df2)


dmonth = df2.groupby(['month']).mean().to_dict()
dall = df2.groupby(['month']).mean().sum().to_dict()
# print(dall)


hdem = HDEM(ins.params['hdem'], True)
lu = INDX(ins.params['lu'], hdem.gd).x # must be the same grid definition
sg = INDX(ins.params['sg'], hdem.gd).x # must be the same grid definition
sg = surfgeo_OGS.convertOGStoRelativeK(sg) # converts OGS surficial geology index to relative permeabilities

# # check
# lu.saveAs("M:\\Peel\\Raven-PWRMM21\\PWRMM21\\lu.indx")
# sg.saveAs("M:\\Peel\\Raven-PWRMM21\\PWRMM21\\sg.indx")

lu = {k: solris3.xr(v) for k, v in lu.items()}
sg = {k: surfgeo_OGS.xr(v) for k, v in sg.items()}


sel = None
if 'cid0' in ins.params: sel = int(ins.params['cid0'])
if 'selwshd' in ins.params: sel = set(ascii.readInts(ins.params['selwshd']))
wshd = Watershed(ins.params['wshd'], hdem, sel)
hrus = hru.HRU(wshd,lu,sg,params.hru_minf,params.hru_min_lakef).hrus

# # check
# wshd.saveToIndx("M:\\Peel\\Raven-PWRMM21\\PWRMM21\\wshd.indx")
# dhru = dict()
# c=0
# for sid,lusg in hrus.items(): # swsid: (lu,sg): frac    
#     for t,frac in lusg.items():
#         c += 1
#         dhru[(sid,t[0],t[1])] = c
# uid = dict()
# for sid,cids in wshd.xr.items():
#     for cid in cids:
#         if not cid in lu: continue
#         if not cid in sg: continue
#         t = (sid,lu[cid],sg[cid])
#         # uid[cid] = sid
#         if t in dhru: uid[cid] = dhru[t]         
# hdem.gd.saveBinaryInt("M:\\Peel\\Raven-PWRMM21\\PWRMM21\\hrus.indx",uid)



# # with open("M:\\Peel\\Raven-PWRMM21\\PWRMM21\\PWRMM21---------.rvh","w") as f:
# #     c=0
# #     for t,lusg in hrus.items():
# #         s = wshd.s[t]
# #         for k,frac in lusg.items():
# #             c += 1
# #             f.write('  {:<10}{:10.3f}{:10.1f}{:10.1f}{:10.1f}{:10}{:>20}{:>20}{:>20}          [NONE]         [NONE]{:10.3f}{:10.3f}\n'.format(c,s.km2*frac,s.elv,s.ylat,s.xlng,t,k[0][0],k[0][1],k[1],s.slp,s.asp))





i=0
dallC = dict() # simulated value collection
dw = dict() # weights
for k,v in hrus.items():
    if v=='lake':
        cnam = 'mean.' + str(i)
        if i == 0: cnam = 'mean'
        t = (k,'LAKE','LAKE')
        dallC[t] = dall[cnam]
        dw[t] = 1.
        i += 1
    else:
        for kk,w in v.items():
            cnam = 'mean.' + str(i)
            if i == 0: cnam = 'mean'
            t = (k,kk[0],kk[1])
            dallC[t] = dall[cnam]
            dw[t] = w
            i += 1

# for k,v in dallC.items():
#     print(k,v)

rch = dict()
dsum = dict()
dwgh = dict()
for sid,cids in wshd.xr.items():
    dsum[sid] = 0.0
    dwgh[sid] = 0.0
    for cid in cids:
        if not cid in lu: continue
        if lu[cid] == -9999: continue
        if not cid in sg: continue
        if sg[cid] == -9999: continue
        if hrus[sid]=='lake':
            t = (sid,'LAKE','LAKE')
        else:
            t = (sid,lu[cid],sg[cid])
        if t in dallC:
            rch[cid] = dallC[t]
            dsum[sid] += dallC[t]*dw[t]
            dwgh[sid] += dw[t]

for sid,cids in wshd.xr.items():
    dsum[sid] /= dwgh[sid] 
    for cid in cids:
        if not cid in lu or lu[cid] == -9999 or not cid in sg or sg[cid] == -9999: 
            rch[cid] = dsum[sid]
        else:    
            t = (sid,lu[cid],sg[cid])
            if not t in dallC: rch[cid] = dsum[sid]

print(' printing..')
hdem.gd.saveBinary(ofp+".bil",rch)