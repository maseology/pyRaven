
import os
from datetime import datetime, timedelta
from timeit import default_timer as timer
from pymmio import files as mmio, ascii
from pyGrid.indx import INDX
from pyGrid.hdem import HDEM
from pyGrid.sws import Watershed
from pkg import hru, solris3, surfgeo, hbv_params, hbv_rvi, hbv_rvh, hbv_rvp, rvt_dailyAPI, hbv_rvc, rvbat
# import rvi, rvh, rvp, rvt, rvc, rvbat



def HBV(ins):

    stmsg = "=== Raven HBV-EC builder ==="
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


    # options
    params = hbv_params.Params
    writemetfiles = not os.path.exists(root + "input")
    if 'options' in ins.params:
        if 'overwritetemporalfiles' in ins.params['options']:
            writemetfiles = ins.params['options']['overwritetemporalfiles']      
        if 'minhrufrac' in ins.params['options']:
            params.hru_minf = float(ins.params['options']['minhrufrac'])


    # load data
    print("\n=== Loading data..")
    # met = Met(ins.params['met'], skipdata = not writemetfiles)
    # if writemetfiles: met.dftem = np.transpose(met.dftem, (1, 0, 2)) # re-order array axes
    hdem = HDEM(ins.params['hdem'], True)
    print(' loading', ins.params['sg'])
    sg = INDX(ins.params['sg'], hdem.gd).x
    print(' loading', ins.params['lu'])
    lu = INDX(ins.params['lu'], hdem.gd).x # must be the same grid definition



    # build climate locations
    # if not met.lc == 0: print(" *** ERROR *** model builder only supports grid-based met files")
    # if not os.path.exists(mmio.removeExt(ins.params['met'])+'.gdef'): print(" *** ERROR *** model builder cannot locate GDEF for loaded grid-based met file")
    # metgd = GDEF(mmio.removeExt(ins.params['met'])+'.gdef')
    # mdlgd = hdem.gd
    # met.cropToExtent(metgd, mdlgd, 10000.0)
    # met.convertToLatLng()    


    # build subwatersheds
    sel = None
    if 'selwshd' in ins.params: sel = set(ascii.readInts(ins.params['selwshd']))
    lu = {k: solris3.xr(v) for k, v in lu.items()}
    sg = {k: surfgeo.xr(v) for k, v in sg.items()}
    wshd = Watershed(ins.params['wshd'], hdem, sel)
    hrus = hru.HRU(wshd,lu,sg,params.hru_minf).hrus


    # make directories   
    mmio.mkDir(root)
    mmio.mkDir(root + "output")



    print("\n\n=== Writing data..")
    hbv_rvi.write(root, nam, builder, ver, ins.params['dtb'], ins.params['dte'], 86400)
    hbv_rvp.write(root, nam, desc, builder, ver, hrus) # parameters
    hbv_rvh.write(root, nam, desc, builder, ver, wshd, hrus, params) # HRUs
    rvt_dailyAPI.write(root, nam, desc, builder, ver, wshd, writemetfiles=writemetfiles) # temporal
    hbv_rvc.write(root, nam, desc, builder, ver)
    rvbat.write(root, nam, ver)


    endtime = str(timedelta(seconds=round(timer() - b0,0)))
    print('\ntotal elapsed time: ' + endtime)

