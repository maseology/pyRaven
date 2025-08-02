
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from timeit import default_timer as timer
from pymmio import files as mmio, ascii
from pyGrid.definition import GDEF
from pyGrid.indx import INDX
from pyGrid.real import REAL
from pyGrid.hdem import HDEM, tec
from pyGrid.sws import Watershed
from pyRaven import buildHBV, buildHMETS, hru, ostrich_HBV, ostrich_HMETS, parameters, reservoir
from pyRaven.flags import flg

def __semidistributedCollect(ins, xrlu, xrsg):
    # paths and notes
    print("\n=== Gathering user options..")
    root0 = ins.root
    nam = ins.nam
    now = datetime.now()
    builder = 'M. Marchildon ' + now.strftime("%Y-%m-%d %H:%M:%S")
    ver = "3.8"


    #################################
    # functions
    #################################
    def isCalib():
        if 'options' in ins.params:
            if 'calibrationmode' in ins.params['options']:
                print('\n ** Calibration Mode Enabled ** ')
                print('    Raven built with calibration/MC optimizations:')
                print('      - Silent mode')
                print('      - Adds global parameter adjusters')
                print('      - Only models gauged subbasins\n')
                mmio.mkDir(root0 + nam + ins.sfx + "_CALIB\\")
                return root0 + nam + ins.sfx + "_CALIB\\model\\", True
        return root0 + nam + ins.sfx + "\\", False
    
    def relpath(fp):
        fp = fp.replace('"','')
        if os.path.exists(fp): return fp
        if not os.path.exists(root0+fp): 
            print('error: file not found: '+fp)
            quit()
        else:
            return root0+fp
        


    #################################
    # read model control file
    #  collect simulation options
    #################################
    root, flg.calibrationmode = isCalib()
    params = parameters.Params()
    ts = 86400
    epsg = 3161
    aggregateHRUs = True
    dtb = ins.params['dtb']
    dte = ins.params['dte']
    obsFP = ""
    res = None
    flg.writemetfiles = not os.path.exists(root + "input")
    if 'timestep' in ins.params: ts = int(ins.params['timestep'])
    if 'obsfp' in ins.params: obsFP = relpath(ins.params['obsfp'])
    if len(obsFP)==0 and os.path.isdir(root0+'obs'): obsFP=root0+'obs' # setting default observation directory
    if 'options' in ins.params:
        if 'overwritetemporalfiles' in ins.params['options']:
            flg.writemetfiles = ins.params['options']['overwritetemporalfiles']      
        if 'minhrufrac' in ins.params['options']:
            params.hru_minf = float(ins.params['options']['minhrufrac'])
        if 'lakehruthresh' in ins.params['options']:
            params.hru_min_lakef = float(ins.params['options']['lakehruthresh'])            
        if 'preciponly' in ins.params['options']: 
            flg.preciponly=True
        if 'skiphruaggregation' in ins.params['options']: # Lumps all small HRUs (<hru_minf) into 1 mega HRU; otherwise aggregates small HRUs into generalized HRU sub-groups (will create greater number of HRUs) 
            aggregateHRUs = False
    if 'parameters' in ins.params: # get parameters
        params.set(ins.params['parameters'])
    if 'reservoirs' in ins.params: # get reservoirs
        res = dict()
        for rnam,v in ins.params['reservoirs'].items():
            match len(v):
                case 2: # subid  fp [month,upper,lower,rulecurve] --> use to create lake-like basic outlets
                    res[int(v[0])] = reservoir.Res(int(v[0]), rnam.replace("-"," ").title(), fp=relpath(v[1]))
                case 4: # subid  minstage  maxstage  fp [month,upper,lower,rulecurve] --> use to create stage-discharge relationship (need to fix)
                    res[int(v[0])] = reservoir.Res(int(v[0]), rnam.replace("-"," ").title(), float(v[1]), float(v[2]), relpath(v[3]))
                case _:
                    print("unknown reservoir input format for "+rnam)
           


    #################################
    # load data
    #################################
    print("\n=== Loading data..")
    # met = Met(ins.params['met'], skipdata = not flg.writemetfiles)
    # if flg.writemetfiles: met.dftem = np.transpose(met.dftem, (1, 0, 2)) # re-order array axes

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
            if c in dem.gd.crc:
                i,j = dem.gd.crc[c]
                cc = dem.gd.cco[i][j]
                tem[c] = tec(cc[0],cc[1],z,g[c],a[c])
        dem = HDEM()
        gd.setActives(list(tem.keys()))
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




    #################################
    # build subwatersheds
    #################################
    print("\n=== Building sub-basins and HRUs from land use and surficial geology..")
    sel = None
    if 'cid0' in ins.params: sel = int(ins.params['cid0'])
    if 'selwshd' in ins.params: sel = set(ascii.readInts(relpath(ins.params['selwshd'])))
    if 'swsids' in ins.params: sel = set(ins.params['swsids'])       
    lu = {k: xrlu.xr(v) for k, v in lu.items()}
    sg = {k: xrsg.xr(v) for k, v in sg.items()}
    wshd = Watershed(relpath(ins.params['wshd']), dem, sel, epsg)
    if len(obsFP)>0 and not os.path.isdir(obsFP):
        df = pd.read_csv(obsFP)
        if not "Date" in df.columns and "SubId" in df.columns: 
            # special case: when observation file is not a hydrograph, rather an index of SubIds and listed .rvt files
            # created using E:\Sync\@dev\go\src\test\rdrr-to-raven-input\main.go
            gagdict = dict(zip(df.SubId,df.name))
            for k,v in gagdict.items():
                if k in wshd.gag: 
                    wshd.gag[k]=v
            obsFP=mmio.removeExt(obsFP)
    if flg.calibrationmode:
        norig = len(wshd.xr)
        sel = set()
        for k,v in wshd.gag.items():
            if len(v)==0: continue
            sel.update(wshd.climb(k))
        wshd = wshd.subset(list(sel))
        print(' for calibration mode, model reduced from {} to {} subbasins'.format(norig,len(wshd.xr)))
    # else:
    #     mmio.mkDir(root0+nam+'-rasters')
    #     gd.saveBinaryInt(root0+nam+'-rasters/'+nam+'-ilu.bil',lu)
    #     gd.saveBinaryInt(root0+nam+'-rasters/'+nam+'-isg.bil',sg)
    hrus = hru.HRU(wshd,lu,sg,params.hru_minf,params.hru_min_lakef,dem,xrlu.default(),xrsg.default(),epsg,aggregateHRUs)


    # compile subbasin land use stats
    for t in wshd.xr:
        na,nn,nu,nk=0,0,0,0
        for lusg in hrus.hrus[t]:
            if not type(lusg)==tuple: continue
            match lusg[0][0]:
                case "Agriculture": na+=1
                case "Urban": nu+=1
                case "ShortVegetation" | "Forest" | "Swamp": nn+=1
                case _: nk+=1 # Barren, Waterbody, noflow
        n=(na+nn+nu+nk)/100
        if n>0: wshd.info[t] = (na/n,nn/n,nu/n) # 'Ag{:2.0f}%; Nat{:2.0f}%; Urb{:2.0f}%'.format(na/n,nn/n,nu/n)


    # make directories   
    mmio.mkDir(root)

    # print misc files
    # if flg.calibrationmode: 
    hrus.writeHRUidBil(root,nam, gd, wshd) # outputs an HRU id cross-referencing raster

    return root0, root, nam, builder, ver, wshd, hrus, res, params, obsFP, ts, dtb, dte


# the simple HMETS model (as built by ORMGP for application in southern Ontario, Canada)
# Martel, J., Demeester, K., Brissette, F., Poulin, A., Arsenault, R., 2017. HMETS - a simple and efficient hydrology model for teaching hydrological modelling, flow forecasting and climate change impacts to civil engineering students. International Journal of Engineering Education 34, 1307–1316.
def HMETS_OWRC(ins, xrlu, xrsg):

    stmsg = "=== Raven HMETS-OWRC builder ==="
    desc = ins.desc
    print("\n" + "="*len(stmsg))
    print(stmsg)
    print("="*len(stmsg) + "\n")
    if len(desc) > 0: print(desc) #"\n{}\n".format(desc))
    b0 = timer()

    root0, root, nam, builder, ver, wshd, hrus, res, params, obsFP, ts, dtb, dte = __semidistributedCollect(ins, xrlu, xrsg)

    print("\n\n=== Writing control files..")
    if 'submodel' in ins.params['options']:
        outsb = ins.params['options']['submodel']
        buildHMETS.buildSubmodel(root, nam, desc, builder, ver, wshd, hrus, res, params, obsFP, ts, dtb, dte, outsb)
    elif 'gaugedsubmodels' in ins.params['options']:
        buildHMETS.buildGaugedSubmodels(root, nam, desc, builder, ver, wshd, hrus, res, params, obsFP, ts, dtb, dte)
    else:
        buildHMETS.build(root, nam, desc, builder, ver, wshd, hrus, res, params, obsFP, ts, dtb, dte)

    # Copy Ostrich files and templates
    if flg.calibrationmode: 
        print('\n writing Ostrich templates..')
        # shutil.copytree('E:/Sync/@dev/Raven-bin/Ostrich_HMETS', root0 + nam + ins.sfx + "_CALIB\\", dirs_exist_ok=True)
        ostrich_HMETS.writeDDS(root0 + nam + ins.sfx + "_CALIB\\", nam, wshd, hrus, res)


    endtime = str(timedelta(seconds=round(timer() - b0,0)))
    print('\ntotal elapsed time: ' + endtime)


# the HBV model (as built by ORMGP for application in southern Ontario, Canada)
def HBV_OWRC(ins, xrlu, xrsg, sfx=''):

    stmsg = "=== Raven HBV-OWRC builder ==="
    desc = ins.desc
    print("\n" + "="*len(stmsg))
    print(stmsg)
    print("="*len(stmsg) + "\n")
    if len(desc) > 0: print(desc) #"\n{}\n".format(desc))
    b0 = timer()

    root0, root, nam, builder, ver, wshd, hrus, res, params, obsFP, ts, dtb, dte = __semidistributedCollect(ins, xrlu, xrsg)

    print("\n\n=== Writing control files..")
    if 'submodel' in ins.params['options']:
        outsb = ins.params['options']['submodel']
        buildHBV.buildSubmodel(root, nam, desc, builder, ver, wshd, hrus, res, params, obsFP, ts, dtb, dte, outsb)
    elif 'gaugedsubmodels' in ins.params['options']:
        buildHBV.buildGaugedSubmodels(root0, root, nam, desc, builder, ver, wshd, hrus, res, params, obsFP, ts, dtb, dte)
    else:
        buildHBV.build(root, nam, desc, builder, ver, wshd, hrus, res, params, obsFP, ts, dtb, dte)

    # Copy Ostrich files and templates
    if flg.calibrationmode: 
        print('\n writing Ostrich templates..')
        ostrich_HBV.writeDDS(root0 + nam + ins.sfx + "_CALIB\\", nam, wshd, hrus, res)
        
    endtime = str(timedelta(seconds=round(timer() - b0,0)))
    print('\ntotal elapsed time: ' + endtime)

