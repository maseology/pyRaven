
from pymmio import files as mmio
from pyRaven import batchfile, rvi_hmets, rvh_hmets, rvp_hmets, rvp_channels, rvc_hmets, rvt_OWRCapi, rvt_Obs, rvt_Res


# the simple HMETS model
# Martel, J., Demeester, K., Brissette, F., Poulin, A., Arsenault, R., 2017. HMETS - a simple and efficient hydrology model for teaching hydrological modelling, flow forecasting and climate change impacts to civil engineering students. International Journal of Engineering Education 34, 1307–1316.
def build(root, nam, desc, builder, ver, wshd, hrus, res, params, obsFP, ts, dtb, dte):
    # full model domain
    mmio.mkDir(root + "input")
    mmio.mkDir(root + "output")
    rvi_hmets.write(root, nam, builder, ver, dtb, dte, res, ts)            
    rvh_hmets.write(root, nam, desc, builder, ver, wshd, hrus, res, params) # structure
    rvp_hmets.write(root, nam, desc, builder, ver, hrus, params) # parameters
    rvp_channels.write(root, nam, wshd)
    rvc_hmets.write(root, nam, desc, builder, ver, hrus, res) # initial conditions
    rvt_OWRCapi.write(root, nam, desc, builder, ver, wshd, hrus, ts) # temporal forcing files
    rvt_Obs.write(root, nam, wshd, obsFP) # temporal observation files  
    rvt_Res.write(root, nam, hrus, res)
    batchfile.write(root, nam, ver) 


def buildSubmodel(root, nam, desc, builder, ver, wshd, hrus, res, params, obsFP, ts, dtb, dte, outsb):
    mmio.mkDir(root + "input")
    mmio.mkDir(root + "output")
    if type(outsb)==int:
        wshd2 = wshd.subset(outsb)
        def subsetHRUs():                
            hrus2, xyzga2 = dict(), dict()
            for k in wshd2.xr.keys(): 
                hrus2[k] = hrus.hrus[k]
                xyzga2[k] = hrus.xyzga[k]
            return hrus2, xyzga2
        hrus.hrus, hrus.xyzga = subsetHRUs()
        print(' submodel mode: model reduced from {} to {} subbasins'.format(len(wshd.xr),len(hrus.hrus)))
        rvi_hmets.write(root, nam, builder, ver, dtb, dte, res, ts)            
        rvh_hmets.write(root, nam, desc, builder, ver, wshd2, hrus, res, params) # structure
        rvp_hmets.write(root, nam, desc, builder, ver, hrus, params) # parameters
        rvp_channels.write(root, nam, wshd2)
        rvc_hmets.write(root, nam, desc, builder, ver, hrus, res) # initial conditions
        rvt_OWRCapi.write(root, nam, desc, builder, ver, wshd2, hrus, ts) # temporal forcing files
        rvt_Obs.write(root, nam, wshd2, obsFP) # temporal observation files  
        rvt_Res.write(root, nam, hrus, res)
        batchfile.write(root, nam, ver)   
    elif type(outsb)==list:
        print('TODO: multiple submodel input.  Quitting build')
        exit()

def buildGaugedSubmodels(root, nam, desc, builder, ver, wshd, hrus, res, params, obsFP, ts, dtb, dte):
    print('TODO: multiple submodel input.  Quitting build')
    exit()
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
    #     rvi_hbv.write(subroot, subnam, builder, ver, dtb, dte, res, ts)
    #     rvp_hbv.write(subroot, subnam, desc, builder, ver, hrus, params) # parameters
    #     rvp_channels.default_trap(root, nam)
    #     rvh_hbv.write(subroot, subnam, desc, builder, ver, wshd2, hrus, res, params)
    #     rvt_OWRCapi.write(subroot, subnam, desc, builder, ver, wshd2, ts, submdl=True) # temporal forcing files)
    #     obsFP = root0+'obs\\'+v+'.csv'
    #     if os.path.exists(obsFP): rvt_Obs.write(subroot, subnam, wshd2, obsFP, submdl=True)
    #     rvc_hbv.write(subroot, subnam, desc, builder, ver, hrus, res)   
    #     rvt_Res.write(subroot, subnam, hrus, res)
    #     batchfile.write(subroot, subnam, ver)     

    #     mmio.deletefile(root + nam + ".rvt")
    #     mmio.deletefile(root + 'GaugeWeightTable.txt')


def buildLumped(root, nam, desc, builder, ver, wshd, params, ts, dtb, dte):
    # full model domain
    mmio.mkDir(root + "input")
    mmio.mkDir(root + "output")
    rvi_hmets.write(root, nam, builder, ver, dtb, dte, None, ts)            
    rvh_hmets.writeLumped(root, nam, desc, builder, ver, wshd) # structure
    rvp_hmets.writeLumped(root, nam, desc, builder, ver, params) # parameters
    rvp_channels.default_trap(root, nam)
    rvc_hmets.write(root, nam, desc, builder, ver, None, None) # initial conditions
    rvt_OWRCapi.write(root, nam, desc, builder, ver, wshd, None, ts) # temporal forcing files
    batchfile.write(root, nam, ver) 
