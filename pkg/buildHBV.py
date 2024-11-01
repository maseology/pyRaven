
import os
import numpy as np
from datetime import datetime, timedelta
from timeit import default_timer as timer
from pymmio import files as mmio, ascii
from pyGrid.definition import GDEF
from pyGrid.indx import INDX
from pyGrid.real import REAL
from pyGrid.hdem import HDEM
from pyGrid.sws import Watershed
from pkg import hru, solris3, surfgeo_OGS, hbv_params, hbv_rvi, hbv_rvh, hbv_rvp, rvt_OWRCapi, hbv_rvc, rvbat
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
    ver = "3.8"


    # options
    params = hbv_params.Params
    ts = 86400
    obsFP = ""
    writemetfiles = not os.path.exists(root + "input")
    if 'timestep' in ins.params: ts = int(ins.params['timestep'])
    if 'obsfp' in ins.params: obsFP = ins.params['obsfp']
    if 'options' in ins.params:
        if 'overwritetemporalfiles' in ins.params['options']:
            writemetfiles = ins.params['options']['overwritetemporalfiles']      
        if 'minhrufrac' in ins.params['options']:
            params.hru_minf = float(ins.params['options']['minhrufrac'])
        if 'lakehruthresh' in ins.params['options']:
            params.hru_min_lakef = float(ins.params['options']['lakehruthresh'])            
        
    def relpath(fp):
        if os.path.exists(fp): return fp
        if not os.path.exists(root0+fp): 
            print('error: file not found: '+fp)
            quit()
        else:
            return root0+fp



    # load data
    print("\n=== Loading data..")
    # met = Met(ins.params['met'], skipdata = not writemetfiles)
    # if writemetfiles: met.dftem = np.transpose(met.dftem, (1, 0, 2)) # re-order array axes

    dem = None
    gd = GDEF(relpath(ins.params['gdef']))
    if 'hdem' in ins.params: 
        dem = HDEM(relpath(ins.params['hdem']))
        # if 'gdef' in ins.params: hdem.Crop(GDEF(relpath(ins.params['gdef'])))
        gd = dem.gd
    elif 'dem' in ins.params:
        print(' loading', ins.params['dem'])
        dem = REAL(relpath(ins.params['dem']), gd, np.float32)
    else:
        pass

    print(' loading', ins.params['sg'])
    sg = INDX(relpath(ins.params['sg']), gd).x # must be the same grid definition
    sg = surfgeo_OGS.convertOGStoRelativeK(sg) # converts OGS surficial geology index to relative permeabilities
    print(' loading', ins.params['lu'])
    lu = INDX(relpath(ins.params['lu']), gd).x # must be the same grid definition



    # build climate locations
    # if not met.lc == 0: print(" *** ERROR *** model builder only supports grid-based met files")
    # if not os.path.exists(mmio.removeExt(ins.params['met'])+'.gdef'): print(" *** ERROR *** model builder cannot locate GDEF for loaded grid-based met file")
    # metgd = GDEF(mmio.removeExt(ins.params['met'])+'.gdef')
    # mdlgd = gd
    # met.cropToExtent(metgd, mdlgd, 10000.0)
    # met.convertToLatLng()    


    # build subwatersheds
    sel = None
    if 'cid0' in ins.params: sel = int(ins.params['cid0'])
    if 'selwshd' in ins.params: sel = set(ascii.readInts(relpath(ins.params['selwshd'])))
    if 'swsids' in ins.params: sel = set(ins.params['swsids'])
    lu = {k: solris3.xr(v) for k, v in lu.items()}
    sg = {k: surfgeo_OGS.xr(v) for k, v in sg.items()}
    wshd = Watershed(relpath(ins.params['wshd']), dem, sel)
    hrus = hru.HRU(wshd,lu,sg,params.hru_minf,params.hru_min_lakef).hrus


    # make directories   
    mmio.mkDir(root)
    mmio.mkDir(root + "output")



    print("\n\n=== Writing data..")
    hbv_rvi.write(root, nam, builder, ver, ins.params['dtb'], ins.params['dte'], ts)
    hbv_rvp.write(root, nam, desc, builder, ver, hrus) # parameters
    hbv_rvh.write(root, nam, desc, builder, ver, wshd, hrus, params) # HRUs
    rvt_OWRCapi.write(root, nam, desc, builder, ver, wshd, obsFP, ts, writemetfiles=writemetfiles) # temporal
    hbv_rvc.write(root, nam, desc, builder, ver)
    rvbat.write(root, nam, ver)


    endtime = str(timedelta(seconds=round(timer() - b0,0)))
    print('\ntotal elapsed time: ' + endtime)

