
import os, shutil
import pandas as pd
from pymmio import files as mmio


def writeDailyObs(infp, outfp, swsID):
    hyd = pd.read_csv(infp, parse_dates=["Date"])[['Date','Flow']].set_index('Date')
    dtb = hyd.index.min()
    dte = hyd.index.max()
    hyd = hyd.reindex(pd.date_range(dtb,dte), fill_value=-1.2345)
    with open(outfp,"w") as f:
        f.write(":ObservationData HYDROGRAPH {} m3/s\n".format(swsID))
        f.write(' {} 1.0 {}\n'.format(dtb.strftime("%Y-%m-%d %H:%M:%S"), len(hyd)))
        for v in hyd.Flow:
            # NOTE: "+0"   https://stackoverflow.com/questions/11010683/how-to-have-negative-zero-always-formatted-as-positive-zero-in-a-python-string
            vv=round(v,3)+0
            if vv<0:
                f.write('  -1.2345\n')
            else:
                f.write('  {:.4f}\n'.format(vv))        
        f.write(':EndObservationData')


# append to Time Series Input file (.rvt)
def write(root, nam, wshd, obsFP, submdl=False):
    if len(obsFP)==0: return

    indir = 'input'
    if submdl: indir = '..\\'+indir
    if not os.path.exists(root + nam + ".rvt"): print('  **WARNING: appending to .rvt file that does not exist **')

    with open(root + nam + ".rvt","a") as f:
        f.write('\n')
        if os.path.isdir(obsFP):
            for k,v in wshd.gag.items():
                if len(v)==0: continue
                obsCSV =  obsFP+'\\'+str(k)+'.csv'
                ofp = "{}\\g{}.rvt".format(indir,mmio.fileNameClean(v))
                if os.path.exists(ofp): continue
                if not os.path.exists(obsCSV): obsCSV = obsFP+'\\'+v+'.csv'
                if not os.path.exists(obsCSV): continue
                f.write('# Observing outlet at subbasin {} to file: {} \n'.format(k, mmio.getFileName(obsCSV,False)))
                f.write(':RedirectToFile {}\n\n'.format(ofp))
                if not os.path.exists(ofp): writeDailyObs(obsCSV, root+ofp, k)
        else:
            ofp = "{}\\g{}.rvt".format(indir,mmio.getFileName(obsFP))
            swsID = wshd.outlets()[0]
            f.write('# Observing outlet at subbasin {} to file: {} \n'.format(swsID, mmio.getFileName(obsFP,False)))
            f.write(':RedirectToFile {}\n'.format(ofp))
            if not os.path.exists(ofp): writeDailyObs(obsFP, root+ofp, swsID)