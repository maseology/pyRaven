
import os
import numpy as np
from datetime import datetime, timedelta
from timeit import default_timer as timer
from pymmio import files as mmio, ascii
from pyGrid.definition import GDEF
from pyGrid.indx import INDX
from pyGrid.real import REAL
from pyGrid.hdem import HDEM, tec
from pyGrid.sws import Watershed
from pyRaven import batchfile, hru, rvi_hmets, rvh_hmets, rvp_hmets, rvp_channels, rvc_hmets, rvt_OWRCapi, rvt_Obs, rvt_Res, parameters, reservoir


# the simple HMETS model
# Martel, J., Demeester, K., Brissette, F., Poulin, A., Arsenault, R., 2017. HMETS - a simple and efficient hydrology model for teaching hydrological modelling, flow forecasting and climate change impacts to civil engineering students. International Journal of Engineering Education 34, 1307–1316.
def HMETS_OWRC(ins, xrlu, xrsg):

    stmsg = "=== Raven HMETS-OWRC builder ==="
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


    # functions
    def relpath(fp):
        if os.path.exists(fp): return fp
        if not os.path.exists(root0+fp): 
            print('error: file not found: '+fp)
            quit()
        else:
            return root0+fp
        

    # options
    params = parameters.Params()
    ts = 86400
    obsFP = ""
    res = None
    preonly=False
    writemetfiles = not os.path.exists(root + "input")
    if 'timestep' in ins.params: ts = int(ins.params['timestep'])
    if 'obsfp' in ins.params: obsFP = ins.params['obsfp']
    if len(obsFP)==0 and os.path.isdir(root0+'obs'): obsFP=root0+'obs' # setting default observation directory
    if 'options' in ins.params:
        if 'overwritetemporalfiles' in ins.params['options']:
            writemetfiles = ins.params['options']['overwritetemporalfiles']      
        if 'minhrufrac' in ins.params['options']:
            params.hru_minf = float(ins.params['options']['minhrufrac'])
        if 'lakehruthresh' in ins.params['options']:
            params.hru_min_lakef = float(ins.params['options']['lakehruthresh'])            
        if 'preciponly' in ins.params['options']: 
            preonly=True
    if 'parameters' in ins.params: # get parameters
        params.set(ins.params['parameters'])
    if 'reservoirs' in ins.params: # get reservoirs
        res = dict()
        for rnam,v in ins.params['reservoirs'].items():            
            res[int(v[0])] = reservoir.Res(int(v[0]), rnam.replace("-"," ").title(), float(v[1]), float(v[2]), relpath(v[3]))
           


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
        g,a = dem.slopeAspectTarboton()
        tem = dict()
        for c, z in dem.x.items():
            i,j = dem.gd.crc[c]
            cc = dem.gd.cco[i][j]
            tem[c] = tec(cc[0],cc[1],z,g[c],a[c])
        dem = HDEM()
        dem.gd = gd
        dem.tem = tem
    else:
        pass

    print(' loading', ins.params['sg'])
    sg = INDX(relpath(ins.params['sg']), gd).x # must be the same grid definition
    sg = xrsg.convertOGStoRelativeK(sg) # converts OGS surficial geology index to relative permeabilities
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
    print("\n=== Building subbasins, HRUs, from land use and surficial geology..")
    sel = None
    if 'cid0' in ins.params: sel = int(ins.params['cid0'])
    if 'selwshd' in ins.params: sel = set(ascii.readInts(relpath(ins.params['selwshd'])))
    if 'swsids' in ins.params: sel = set(ins.params['swsids'])
    lu = {k: xrlu.xr(v) for k, v in lu.items()}
    sg = {k: xrsg.xr(v) for k, v in sg.items()}
    wshd = Watershed(relpath(ins.params['wshd']), dem, sel)
    hrus = hru.HRU(wshd,lu,sg,params.hru_minf,params.hru_min_lakef,dem,xrlu.default(),xrsg.default())



    # make directories   
    mmio.mkDir(root)

    print("\n\n=== Writing control files..")
    if 'submodel' in ins.params['options']:
        mmio.mkDir(root + "input")
        mmio.mkDir(root + "output")
        outsb = ins.params['options']['submodel']
        if type(outsb)==int:
            wshd2 = wshd.subset(outsb)
            def subsetHRUs():                
                hrus2, zga2 = dict(), dict()
                for k in wshd2.xr.keys(): 
                    hrus2[k] = hrus.hrus[k]
                    zga2[k] = hrus.zga[k]
                return hrus2, zga2
            hrus.hrus, hrus.zga = subsetHRUs()
            rvi_hmets.write(root, nam, builder, ver, ins.params['dtb'], ins.params['dte'], res, ts, preonly)            
            rvh_hmets.write(root, nam, desc, builder, ver, wshd2, hrus, res, params) # structure
            rvp_hmets.write(root, nam, desc, builder, ver, hrus, params) # parameters
            rvp_channels.default_trap(root, nam)
            rvc_hmets.write(root, nam, desc, builder, ver, hrus, res) # initial conditions
            rvt_OWRCapi.write(root, nam, desc, builder, ver, wshd2, ts, preciponly=preonly, writemetfiles=writemetfiles) # temporal forcing files
            rvt_Obs.write(root, nam, wshd2, obsFP) # temporal observation files  
            rvt_Res.write(root, nam, hrus, res)
            batchfile.write(root, nam, ver)             
        elif type(outsb)==list:
            print('TODO: multiple submodel input.  Quitting build')
            exit()
    elif 'gaugedsubmodels' in ins.params['options']:
        pass # TODO
        # mmio.mkDir(root + "input")
        # gag = {(k,v) for k,v in wshd.gag.items() if len(v)>0}
        # print(' creating sub-models draining to {} gauge(s):'.format(len(gag)))
        # for k,v in gag:
        #     print('  > '+v)
        #     subroot = root + v + '\\'
        #     subnam = nam+'-'+v
        #     mmio.mkDir(subroot)
        #     mmio.mkDir(subroot + "output")
        #     wshd2 = wshd.subset(k)
        #     hrus2, zga2 = dict(), dict()
        #     for k in wshd2.xr.keys(): 
        #         hrus2[k] = hrus.hrus[k]
        #         zga2[k] = hrus.zga[k]
        #     hrus.hrus = hrus2
        #     hrus.zga = zga2
        #     rvi_hbv.write(subroot, subnam, builder, ver, ins.params['dtb'], ins.params['dte'], res, ts, preonly)
        #     rvp_hbv.write(subroot, subnam, desc, builder, ver, hrus, params) # parameters
        #rvp_channels.default_trap(root, nam)
        #     rvh_hbv.write(subroot, subnam, desc, builder, ver, wshd2, hrus, res, params)
        #     rvt_OWRCapi.write(subroot, subnam, desc, builder, ver, wshd2, ts, preciponly=preonly, writemetfiles=writemetfiles, submdl=True) # temporal forcing files)
        #     obsFP = root0+'obs\\'+v+'.csv'
        #     if os.path.exists(obsFP): rvt_Obs.write(subroot, subnam, wshd2, obsFP, submdl=True)
        #     rvc_hbv.write(subroot, subnam, desc, builder, ver, hrus, res)   
        #     rvt_Res.write(subroot, subnam, hrus, res)
        #     batchfile.write(subroot, subnam, ver)            
    else: # full model domain
        pass # TODO
        # mmio.mkDir(root + "input")
        # mmio.mkDir(root + "output")
        # rvi_hbv.write(root, nam, builder, ver, ins.params['dtb'], ins.params['dte'], res, ts, preonly) # model structure
        # rvp_hbv.write(root, nam, desc, builder, ver, hrus, params) # parameters
        #rvp_channels.default_trap(root, nam)
        # rvh_hbv.write(root, nam, desc, builder, ver, wshd, hrus, res, params) # HRUs
        # rvc_hbv.write(root, nam, desc, builder, ver, hrus, res) # initial conditions
        # rvt_OWRCapi.write(root, nam, desc, builder, ver, wshd, ts, preciponly=preonly, writemetfiles=writemetfiles) # temporal forcing files
        # rvt_Obs.write(root, nam, wshd, obsFP) # temporal observation files        
        # rvt_Res.write(root, nam, hrus, res)
        # batchfile.write(root, nam, ver)
    
    # if 'gaugedsubmodels' in ins.params['options']: # clean up files
    #     mmio.deletefile(root + nam + ".rvt")
    #     mmio.deletefile(root + 'GaugeWeightTable.txt')


    endtime = str(timedelta(seconds=round(timer() - b0,0)))
    print('\ntotal elapsed time: ' + endtime)

