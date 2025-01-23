
import os
from pymmio import files as mmio
from pyRaven import batchfile, rvc_hbv, rvh_hbv, rvi_hbv, rvp_hbv, rvp_channels, rvt_OWRCapi, rvt_Obs, rvt_Res


def build(root, nam, desc, builder, ver, wshd, hrus, res, params, obsFP, ts, dtb, dte, writemetfiles, preonly, calibrationmode):
    # full model domain
    mmio.mkDir(root + "input")
    mmio.mkDir(root + "output")
    rvi_hbv.write(root, nam, builder, ver, dtb, dte, res, ts, preonly) # model structure
    rvh_hbv.write(root, nam, desc, builder, ver, wshd, hrus, res, params) # HRUs
    rvp_hbv.write(root, nam, desc, builder, ver, hrus, params) # parameters
    rvp_channels.default_trap(root, nam)
    rvc_hbv.write(root, nam, desc, builder, ver, hrus, res) # initial conditions
    rvt_OWRCapi.write(root, nam, desc, builder, ver, wshd, hrus, ts, preciponly=preonly, writemetfiles=writemetfiles) # temporal forcing files
    rvt_Obs.write(root, nam, wshd, obsFP) # temporal observation files        
    rvt_Res.write(root, nam, hrus, res)
    batchfile.write(root, nam, ver)


def buildSubmodel(root, nam, desc, builder, ver, wshd, hrus, res, params, obsFP, ts, dtb, dte, writemetfiles, preonly, calibrationmode, outsb):
    mmio.mkDir(root + "input")
    mmio.mkDir(root + "output")
    if type(outsb)==int:
        wshd2 = wshd.subset(outsb)
        def subsetHRUs():                
            hrus2, zga2 = dict(), dict()
            for k in wshd2.xr.keys(): 
                hrus2[k] = hrus.hrus[k]
                zga2[k] = hrus.zga[k]
            return hrus2, zga2
        hrus.hrus, hrus.zga = subsetHRUs()
        rvi_hbv.write(root, nam, builder, ver, dtb, dte, res, ts, preonly)
        rvh_hbv.write(root, nam, desc, builder, ver, wshd2, hrus, res, params)
        rvp_hbv.write(root, nam, desc, builder, ver, hrus, params) # parameters
        rvp_channels.default_trap(root, nam)
        rvt_OWRCapi.write(root, nam, desc, builder, ver, wshd2, hrus, ts, preciponly=preonly, writemetfiles=writemetfiles) # temporal forcing files
        rvt_Obs.write(root, nam, wshd2, obsFP) # temporal observation files  
        rvc_hbv.write(root, nam, desc, builder, ver, hrus, res) # initial conditions
        rvt_Res.write(root, nam, hrus, res)            
        batchfile.write(root, nam, ver)             
    elif type(outsb)==list:
        print('TODO: multiple submodel input.  Quitting build')
        exit()

def buildGaugedSubmodels(root0, root, nam, desc, builder, ver, wshd, hrus, res, params, obsFP, ts, dtb, dte, writemetfiles, preonly, calibrationmode):
    mmio.mkDir(root + "input")
    gag = {(k,v) for k,v in wshd.gag.items() if len(v)>0}
    print(' creating sub-models draining to {} gauge(s):'.format(len(gag)))
    for k,v in gag:
        print('  > '+v)
        subroot = root + v + '\\'
        subnam = nam+'-'+v
        mmio.mkDir(subroot)
        mmio.mkDir(subroot + "output")
        wshd2 = wshd.subset(k)
        hrus2, zga2 = dict(), dict()
        for k in wshd2.xr.keys(): 
            hrus2[k] = hrus.hrus[k]
            zga2[k] = hrus.zga[k]
        hrus.hrus = hrus2
        hrus.zga = zga2
        rvi_hbv.write(subroot, subnam, builder, ver, dtb, dte, res, ts, preonly)
        rvh_hbv.write(subroot, subnam, desc, builder, ver, wshd2, hrus, res, params)
        rvp_hbv.write(subroot, subnam, desc, builder, ver, hrus, params) # parameters
        rvp_channels.default_trap(subroot, subnam)
        rvt_OWRCapi.write(subroot, subnam, desc, builder, ver, wshd2, hrus, ts, preciponly=preonly, writemetfiles=writemetfiles, submdl=True) # temporal forcing files)
        obsFP = root0+'obs\\'+v+'.csv'
        if os.path.exists(obsFP): rvt_Obs.write(subroot, subnam, wshd2, obsFP, submdl=True)
        rvc_hbv.write(subroot, subnam, desc, builder, ver, hrus, res)   
        rvt_Res.write(subroot, subnam, hrus, res)
        batchfile.write(subroot, subnam, ver)    

    mmio.deletefile(root + nam + ".rvt")
    mmio.deletefile(root + 'GaugeWeightTable.txt')
