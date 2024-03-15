
import pandas as pd

def writeDailyObs(infp, outfp, swsID):
    hyd = pd.read_csv(infp, parse_dates=["Date"])[['Date','Flow']].set_index('Date')
    dtb = hyd.index.min()
    dte = hyd.index.max()
    hyd = hyd.reindex(pd.date_range(dtb,dte), fill_value=-1.2345)
    with open(outfp,"w") as f:
        f.write(":ObservationData HYDROGRAPH {} m3/s\n".format(swsID))
        f.write(' {} 1.0 {}\n'.format(dtb.strftime("%Y-%m-%d %H:%M:%S"), len(hyd)))
        for v in hyd.Flow:
            f.write('  {:.4f}\n'.format(v))
        f.write(':EndObservationData')
