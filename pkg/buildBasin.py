
import os
from datetime import datetime, timedelta
from timeit import default_timer as timer
from pymmio import files as mmio
from pyMet.met import Met
from pyGrid.hdem import HDEM
from pyGrid.sws import Watershed
from pkg import rvi_snowmelt, rvh_hru, rvp_OneBareLayer, rvt_OWRCapi, rvc_allZero, rvbat



def BasinMelt(ins):    

    stmsg = "=== Raven Basin Snowmelt builder ==="
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

    # read options
    # params = bsm_params.Params
    writemetfiles = not os.path.exists(root + "input")
    if 'options' in ins.params:
        if 'overwritetemporalfiles' in ins.params['options']:
            writemetfiles = ins.params['options']['overwritetemporalfiles'] 

    # load data
    print("\n\n=== Loading data..")
    hdem = HDEM(ins.params['hdem'], True)
    wshd = Watershed(ins.params['wshd'], hdem)
    
    # met = Met(ins.params['met'], skipdata = not writemetfiles)
    # if writemetfiles: met.dftem = np.transpose(met.dftem, (1, 0, 2)) # re-order array axes               
    met = Met()
    met.dtb = datetime.strptime(ins.params['dtb'],"%Y-%m-%d")
    met.dte = datetime.strptime(ins.params['dte'],"%Y-%m-%d")

    # make directories   
    mmio.mkDir(root)
    mmio.mkDir(root + "output")


    print("\n=== Writing model files..")
    
    rvi_snowmelt.write(root, nam, builder, ver, wshd, met)
    rvp_OneBareLayer.write(root, nam, desc, builder, ver) # parameters
    rvh_hru.write(root, nam, desc, builder, ver, wshd) # HRUs    
    rvt_OWRCapi.write(root, nam, desc, builder, ver, wshd, writemetfiles=writemetfiles) # temporal
    rvc_allZero.write(root, nam, desc, builder, ver)
    rvbat.write(root, nam, ver)


    endtime = str(timedelta(seconds=round(timer() - b0,0)))
    print('\ntotal elapsed time: ' + endtime)