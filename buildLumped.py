
import os
import pandas as pd
from datetime import datetime, timedelta
from timeit import default_timer as timer
from pymmio import files as mmio
from pyGrid.sws import Watershed, SWS
from pyRaven import buildHBV, buildHMETS, buildGR4J, rvt_lumped, ostrich_HBV, ostrich_HMETS, ostrich_GR4J, parameters
from pyRaven.flags import flg



# the simple HMETS model (as built by ORMGP for application in southern Ontario, Canada)
# Martel, J., Demeester, K., Brissette, F., Poulin, A., Arsenault, R., 2017. HMETS - a simple and efficient hydrology model for teaching hydrological modelling, flow forecasting and climate change impacts to civil engineering students. International Journal of Engineering Education 34, 1307–1316.
def HMETS(ins):

    stmsg = "=== Raven HMETS-lumped builder ==="
    desc = ins.desc
    print("\n" + "="*len(stmsg))
    print(stmsg)
    print("="*len(stmsg) + "\n")
    if len(desc) > 0: print(desc) #"\n{}\n".format(desc))
    b0 = timer()

    # paths and notes
    print("\n=== Gathering user options..")
    root0 = ins.root
    nam = ins.nam
    now = datetime.now()
    builder = 'M. Marchildon ' + now.strftime("%Y-%m-%d %H:%M:%S")
    ver = "3.8"

    # if 'options' in ins.params:
    #     if 'calibrationmode' in ins.params['options']:
    #         print('\n ** Calibration Mode enabled ** ')
    #         print('    Raven built with calibration/MC optimizations:')
    #         print('      - Silent mode')
    #         print('      - Adds global parameter adjusters')
    #         print('      - Only models gauged subbasins\n')
    #         mmio.mkDir(root0 + nam + ins.sfx + "-lumped_CALIB\\")
    #         flg.calibrationmode = True
    #         root = root0 + nam + ins.sfx + "-lumped_CALIB\\model\\"
    #     else:
    #         root = root0 + nam + ins.sfx + "-lumped\\"
    root = root0 + nam + ins.sfx + "-lumped\\"

    params = parameters.Params()
    ts = 86400
    dtb = ins.params['dtb']
    dte = ins.params['dte']
    flg.writemetfiles = not os.path.exists(root + "input")
    if 'timestep' in ins.params: ts = int(ins.params['timestep'])
    if 'options' in ins.params:
        if 'overwritetemporalfiles' in ins.params['options']:
            flg.writemetfiles = ins.params['options']['overwritetemporalfiles']         
        if 'preciponly' in ins.params['options']: 
            flg.preciponly=True
    if 'parameters' in ins.params: # get parameters
        params.set(ins.params['parameters'])

    wshd = Watershed()
    wshd.s[1] = SWS()
    hrus = None # hru.HRU()

    mmio.mkDir(root)

    print("\n\n=== Writing control files..")
    buildHMETS.buildLumped(root, nam, desc, builder, ver, wshd, params, ts, dtb, dte)

    # Copy Ostrich files and templates
    if flg.calibrationmode: 
        print('\n copying Ostrich templates..')
        # shutil.copytree('E:/Sync/@dev/Raven-bin/Ostrich_HMETS', root0 + nam + ins.sfx + "_CALIB\\", dirs_exist_ok=True)
        ostrich_HMETS.writeDDS(root0 + nam + ins.sfx + "-lumped_CALIB\\", nam, wshd, hrus, None)


    endtime = str(timedelta(seconds=round(timer() - b0,0)))
    print('\ntotal elapsed time: ' + endtime)


# the simple HBV model (as built by ORMGP for application in southern Ontario, Canada)
def HBV(ins):

    stmsg = "=== Raven HBV-lumped builder ==="
    desc = ins.desc
    print("\n" + "="*len(stmsg))
    print(stmsg)
    print("="*len(stmsg) + "\n")
    if len(desc) > 0: print(desc) #"\n{}\n".format(desc))
    b0 = timer()

    # paths and notes
    print("\n=== Gathering user options..")
    root0 = ins.root
    nam = ins.nam
    now = datetime.now()
    builder = 'M. Marchildon ' + now.strftime("%Y-%m-%d %H:%M:%S")
    ver = "3.8"

    root = root0 + nam + ins.sfx + "-lumped\\"

    params = parameters.Params()
    ts = 86400
    dtb = ins.params['dtb']
    dte = ins.params['dte']
    flg.writemetfiles = not os.path.exists(root + "input")
    if 'timestep' in ins.params: ts = int(ins.params['timestep'])
    if 'options' in ins.params:
        if 'overwritetemporalfiles' in ins.params['options']:
            flg.writemetfiles = ins.params['options']['overwritetemporalfiles']         
        if 'preciponly' in ins.params['options']: 
            flg.preciponly=True
    if 'parameters' in ins.params: # get parameters
        params.set(ins.params['parameters'])

    wshd = Watershed()
    wshd.s[1] = SWS()
    hrus = None # hru.HRU()

    mmio.mkDir(root)

    print("\n\n=== Writing control files..")
    buildHBV.buildLumped(root, nam, desc, builder, ver, wshd, params, ts, dtb, dte)

    # Copy Ostrich files and templates
    if flg.calibrationmode: 
        print('\n copying Ostrich templates..')
        # shutil.copytree('E:/Sync/@dev/Raven-bin/Ostrich_HBV', root0 + nam + ins.sfx + "_CALIB\\", dirs_exist_ok=True)
        ostrich_HBV.writeDDS(root0 + nam + ins.sfx + "-lumped_CALIB\\", nam, wshd, hrus, None)


    endtime = str(timedelta(seconds=round(timer() - b0,0)))
    print('\ntotal elapsed time: ' + endtime)


# the parsinonious GR4J model
# Perrin, C., Michel, C., & Andréassian, V. (2003). Improvement of a parsimonious model for streamflow simulation. Journal of hydrology, 279(1-4), 275-289.
def GR4J(ins):

    stmsg = "=== Raven GR4J builder ==="
    desc = ins.desc
    print("\n" + "="*len(stmsg))
    print(stmsg)
    print("="*len(stmsg) + "\n")
    if len(desc) > 0: print(desc) #"\n{}\n".format(desc))
    b0 = timer()

    # paths and notes
    print("\n=== Gathering user options..")
    root0 = ins.root
    nam = ins.nam
    now = datetime.now()
    builder = 'M. Marchildon ' + now.strftime("%Y-%m-%d %H:%M:%S")
    ver = "3.8"

    if 'options' in ins.params:
        if 'calibrationmode' in ins.params['options']:
            print('\n ** Calibration Mode enabled ** ')
            print('    Raven built with calibration/MC optimizations:')
            print('      - Silent mode')
            print('      - Adds global parameter adjusters')
            print('      - Only models gauged subbasins\n')
            mmio.mkDir(root0 + nam + ins.sfx + "_CALIB\\")
            flg.calibrationmode = True
            root = root0 + nam + ins.sfx + "_CALIB\\model\\" 
        else:
            root = root0 + nam + ins.sfx + "\\"

    params = parameters.Params()
    ts = 86400
    if 'data' in ins.params:
        dftem = ins.params['data']
        dtb = min(dftem.index)
        dte = max(dftem.index)
    if 'dtb' in ins.params: dtb = ins.params['dtb']
    if 'dte' in ins.params: dte = ins.params['dte']
    flg.writemetfiles = not os.path.exists(root + "input")
    # if 'timestep' in ins.params: ts = int(ins.params['timestep'])
    if 'options' in ins.params:
        if 'overwritetemporalfiles' in ins.params['options']:
            flg.writemetfiles = ins.params['options']['overwritetemporalfiles']         
        if 'preciponly' in ins.params['options']: 
            flg.precipactive=False
            flg.preciponly=True
        if 'precipactive' in ins.params['options']: 
            flg.precipactive=True
            flg.preciponly=False
    if 'parameters' in ins.params: # get parameters
        params.set(ins.params['parameters'])

    wshd = Watershed()
    sws = SWS()
    if 'carea' in ins.params: sws.km2 = ins.params['carea']
    if 'elev' in ins.params: sws.elv = ins.params['elev']
    if 'lat' in ins.params: sws.ylat = ins.params['lat']
    if 'long' in ins.params: sws.xlng = ins.params['long']    
    if 'slope' in ins.params: sws.slp = ins.params['slope']
    if 'aspect' in ins.params: sws.asp = ins.params['aspect']
    # if 'rchlen' in ins.params: sws.rchlen = ins.params['rchlen']    
    wshd.s[1] = sws
    hrus = None # hru.HRU()

    mmio.mkDir(root)

    print("\n\n=== Writing control files..")
    buildGR4J.buildLumped(root, nam, desc, builder, ver, wshd, params, ts, dtb, dte)

    print("\n\n=== Writing forcing files..")
    if 'data' in ins.params: rvt_lumped.write(root, nam, desc, builder, ver, wshd, dftem)







    # Copy Ostrich files and templates
    if flg.calibrationmode: 
        print('\n copying Ostrich templates..')
        ostrich_GR4J.writeDDS(root0 + nam + ins.sfx + "_CALIB\\", nam, 5000)


    endtime = str(timedelta(seconds=round(timer() - b0,0)))
    print('\ntotal elapsed time: ' + endtime)
