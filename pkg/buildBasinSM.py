
import os
from datetime import datetime, timedelta
import numpy as np
from timeit import default_timer as timer
from pymmio import files as mmio
from pyMet.met import Met
from pyGrid.hdem import HDEM
from pyGrid.sws import Watershed
from pyInstruct import instruct
from pkg import bsm_rvi, bsm_rvh, bsm_rvp, bsm_rvt, bsm_rvc, rvbat



def BasinMelt(fp):
    ins = instruct.build(fp)

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

    # make directories   
    mmio.mkDir(root)
    mmio.mkDir(root + "output")


    print("\n\n=== Writing data..")
    bsm_rvt.write(root, nam, desc, builder, ver, met, wshd, writemetfiles=writemetfiles) # temporal
    bsm_rvi.write(root, nam, builder, ver, met)
    bsm_rvp.write(root, nam, desc, builder, ver) # parameters
    bsm_rvh.write(root, nam, desc, builder, ver, wshd) # HRUs    
    bsm_rvc.write(root, nam, desc, builder, ver)
    rvbat.write(root, nam, ver)


    endtime = str(timedelta(seconds=round(timer() - b0,0)))
    print('\ntotal elapsed time: ' + endtime)