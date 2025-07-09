
import shutil
import numpy as np
from pyRaven.flags import flg
from pymmio import files as mmio

def writeDDS(root, nam, wshd, hru, res, nsmpl=10):
    
    rfn = 'Raven3.8.exe'
    ofn = 'Ostrich_v20171219_Windows.exe'

    shutil.copy("E:/Sync/@dev/Raven-bin/"+ofn,root+ofn)

    haslakes=False
    if haslakes: 
        for ihru in hru.hrus.keys():
            if wshd.lak[ihru]:
                haslakes = True
                break

    with open(root+nam+'-Ostrich.bat','w') as f:
        f.write("""@ECHO OFF
{}
ECHO.
ECHO Optimization complete. Please press any key to close window.
PAUSE>NUL""".format(ofn))
        
    with open(root+'ost_raven.bat','w') as f:
        f.write('@echo off\n\n')
        f.write('copy {0}.rvh model\\{0}.rvh\n'.format(nam))
        f.write('copy {0}.rvp model\\{0}.rvp\n'.format(nam))
        f.write('copy {0}-channels.rvp model\\{0}-channels.rvp\n'.format(nam))
        if haslakes: f.write('copy {0}-lakes.rvh model\\{0}-lakes.rvh\n'.format(nam))
        f.write('\ncd model\n')
        f.write('\n{1} {0} -o output\\\n\ncd ..'.format(nam,rfn))

    with open(root+'ost_savebest.bat','w') as f:
        f.write('@echo off\n')
        f.write('@TITLE SAVE BEST SOLUTION\n')
        f.write('echo saving input files for the best solution found...\n\n')
        f.write('IF NOT EXIST best mkdir best\n\n')
        f.write('robocopy model\\input best\\input /E\n')
        f.write('copy model\\{0}  best\\{0}\n'.format(rfn))
        f.write('copy model\\{0}.bat  best\\{0}.bat\n'.format(nam))
        f.write('copy model\\{0}.rvi  best\\{0}.rvi\n'.format(nam))
        f.write('copy model\\{0}.rvh  best\\{0}.rvh\n'.format(nam))
        f.write('copy model\\{0}.rvt  best\\{0}.rvt\n'.format(nam))
        f.write('copy model\\{0}.rvc  best\\{0}.rvc\n'.format(nam))
        f.write('copy model\\{0}.rvp  best\\{0}.rvp\n'.format(nam))
        f.write('copy model\\{0}-channels.rvp  best\\{0}-channels.rvp\n'.format(nam))
        if haslakes: f.write('copy model\\{0}-lakes.rvh  best\\{0}-lakes.rvh\n'.format(nam))
        f.write('copy model\\output\\{0}_Diagnostics.csv best\\{0}_Diagnostics.csv\n'.format(nam))
        f.write('REM copy model\\output\\{0}_Hydrographs.csv best\\{0}_Hydrographs.csv'.format(nam))
        
    with open(root+'ostIn.txt','w') as f:
        f.write("""ProgramType         DDS
ObjectiveFunction   GCOP

ModelExecutable  ost_raven.bat
PreserveBestModel ost_savebest.bat

BeginExtraDirs
  model
  best
EndExtraDirs""")

        f.write('\nBeginFilePairs\n')
        f.write('  {0}.rvh.tpl;  {0}.rvh\n'.format(nam))
        f.write('  {0}.rvp.tpl;  {0}.rvp\n'.format(nam))
        if wshd.haschans: f.write('  {0}-channels.rvp.tpl;  {0}-channels.rvp\n'.format(nam))
        if haslakes: f.write('  {0}-lakes.rvh.tpl;  {0}-lakes.rvh\n'.format(nam))
        f.write('EndFilePairs\n')
        
        dlu, _, dsg = hru.distinctTypes()
        f.write('\nBeginParams\n')
        f.write('  #parameter                    init.     low      high   tx_in tx_ost  tx_out\n')
        f.write('  #\n')
        f.write('  # Global\n')
        f.write('  xVadose                      random     0.1       0.5    none   none    none\n')
        f.write('  xPhreatic                    random     0.1       2.0    none   none    none\n')
        f.write('  xRAINSNOW_TEMP               random    -2.0       4.0    none   none    none\n')
        if flg.preciponly: f.write('  xRAINSNOW_DELTA              random     1.0      20.0    none   none    none\n')
        f.write('  xSWI_REDUCT_COEFF            random     0.0      0.05    none   none    none\n')
        f.write('  xSNOW_SWI                    random    0.01      0.12    none   none    none\n')
        f.write('  xLogMAX_PERC_RATE_MULT       random      -2         2    none   none    none  # global multiplier (tied)\n')
        f.write('  #\n')
        f.write('  # Landuse\n')
        f.write('  xMIN_MELT_FACTOR             random     0.0       6.0    none   none    none\n')
        f.write('  xMAX_MELT_FACTOR             random     0.0      18.0    none   none    none\n')
        f.write('  xDD_MELT_TEMP                random    -2.0       2.0    none   none    none\n')
        f.write('  xDD_AGGRADATION              random     0.0      0.15    none   none    none\n')
        f.write('  xREFREEZE_FACTOR             random     0.0      10.0    none   none    none\n')
        f.write('  xREFREEZE_EXP                random     0.1       1.0    none   none    none\n')
        f.write('  xDD_REFREEZE_TEMP            random    -4.0       4.0    none   none    none\n')
        f.write('  xLAKE_PET_CORR               random     0.5       1.2    none   none    none\n')
        f.write('  xPET_CORRECTION              random     0.5       1.2    none   none    none\n')
        # runoff coefficients:
        f.write('  xHMETS_RUNOFF_COEFF          random     0.0       1.0    none   none    none\n')
        noAg, noNat, noWet = True, True, True
        for l in dlu: 
            if l=='Agriculture' and noAg:
                f.write('  xAgRC                        random     0.0       1.0    none   none    none\n')
                noAg = False
            elif l in ['Forest','Meadow','ShortVegetation','TallVegetation','SparseVegetation','DenseVegetation'] and noNat:
                f.write('  xNatRC                       random     0.0       1.0    none   none    none\n')
                noNat = False
            elif l in ['Wetland','Swamp','Marsh','Channel','Waterbody','Lake'] and noWet:
                f.write('  xWetRC                       random     0.0       1.0    none   none    none\n')
                noWet = False

        f.write('  #\n')
        f.write('  # Routing\n')
        f.write('  xGAMMA_SHAPE1                random     0.0        10    none   none    none\n')
        f.write('  xLogGAMMA_SCALE1                0.0      -4       2.2    none   none    none  # (tied)\n')
        f.write('  xGAMMA_SHAPE2                random     0.0        10    none   none    none\n')
        f.write('  xLogGAMMA_SCALE2                0.0      -4         2    none   none    none  # (tied)\n')
        f.write('  #\n')
        f.write('  # Interception\n')
        f.write('  xRAIN_ICEPT_FACT             random     0.0       1.0    none   none    none\n')
        f.write('  xSNOW_ICEPT_FACT             random     0.0       1.0    none   none    none\n')
        f.write('  xMAX_CAPACITY                random     0.0       5.0    none   none    none\n')
        f.write('  xMAX_SNOW_CAPACITY           random     0.0       5.0    none   none    none\n')
        f.write('  #\n')

        f.write('  # Baseflow\n')
        if flg.gwzonemode:
            for zone in sorted(set(wshd.gwz.values())):
                f.write('  xBASEFLOW_COEFF{}             random     0.0       1.0    none   none    none\n'.format(zone))
            for st in set([v[0] for v in dsg]):
                if st=='L': continue # LAKE
                stpl = st
                if stpl[:3]=="Low" and len(stpl)>3: stpl=stpl.replace("Low","L")
                if stpl[:6]=="Medium" and len(stpl)>6: stpl=stpl.replace("Medium","M")            
                f.write('  xiflw{:<22}    random     0.0       1.0    none   none    none\n'.format(stpl))
        else:
            f.write('  xinterflow                 random     0.0       1.0    none   none    none\n')
            for st in set([v for v in dsg]):
                if st=='LAKE': continue
                stpl = st
                if stpl[:3]=="Low" and len(stpl)>3: stpl=stpl.replace("Low","L")
                if stpl[:6]=="Medium" and len(stpl)>6: stpl=stpl.replace("Medium","M")            
                f.write('  xbf{:<20}    random     0.0       1.0    none   none    none\n'.format(stpl))

        if wshd.haschans:
            f.write('  #\n')
            f.write('  # channels roughness\n')
            # f.write('  #pNagriculture                0.035    0.01       0.5    none   none    none  # Manning\'s N, mostly agriculture (>60%)\n')
            f.write('  xNurban                       0.035    0.01       0.2    none   none    none  # Manning\'s N, some urban (>25%)\n')
            f.write('  xNnatural                     0.035    0.01       0.8    none   none    none\n')
            f.write('  xNflood                         0.1    0.01       0.5    none   none    none\n')

        if haslakes:
            f.write('  #\n')
            f.write('  # reservoir crest width\n')
            if res is not None:
                for _,r in res.items():
                    if r.hruid in hru.hrus: f.write('  xCW{:<20}        10.0     0.1      50.0    none   none    none\n'.format(r.name.lower().replace(' ','')))
            else: # len(wshd.lak)>0:
                for t,lusg in hru.hrus.items():
                    if lusg=='lake':
                        f.write('  xCW{:<20}        10.0     0.1      50.0    none   none    none\n'.format(t))


        f.write('EndParams\n')
        f.write('\n')
        f.write('BeginTiedParams\n')
        f.write('  # logarithm, base 10 (pl = 10^p)\n')
        f.write('  xMAX_PERC_RATE_MULT  1   xLogMAX_PERC_RATE_MULT  exp  10.0  1.0  1.0  0.0  free\n')
        f.write('  xGAMMA_SCALE1        1   xLogGAMMA_SCALE1        exp  10.0  1.0  1.0  0.0  free\n')
        f.write('  xGAMMA_SCALE2        1   xLogGAMMA_SCALE2        exp  10.0  1.0  1.0  0.0  free\n')
        f.write('EndTiedParams\n')
        

        f.write('\nBeginResponseVars\n')
        f.write('  #name             filename                                           keyword         line    col     token\n')
        dfp = './model/output/{}_Diagnostics.csv'.format(nam)
        glist = list()
        for t in hru.hrus:
            if len(wshd.gag[t])==0: continue
            g = mmio.fileNameClean(wshd.gag[t])[:7]
            cc=0
            while g in glist:
                g = g[:6]+str(cc)
                cc+=1
            glist.append(g)

        for i, g in enumerate(glist):
            f.write('  KG{:<14}  {:48};  OST_NULL      {:>3}       3       \',\'\n'.format(g,dfp,i+1))
        f.write('EndResponseVars\n')

        f.write('\nBeginTiedRespVars\n')
        if len(glist)<10:
            f.write('  NegKG  {}  KG{}  wsum  {}\n'.format(len(glist)," KG".join(glist)," ".join(["{:.3f}".format(-1/len(glist))]*len(glist))))
            # f.write('  NegKG  {}  KG{}  wsum  {}\n'.format(len(glist)," KG".join(glist)," ".join(["-1.0"]*len(glist))))
        else:
            nln = int(np.floor(len(glist)/10))
            for i in range(nln-1):
                f.write('  NegKG_{:<2}  {}  KG{}  wsum  {}\n'.format(i+1,10," KG".join(glist[i*10:(i+1)*10])," ".join(["-0.1"]*10)))
            rem = len(glist)-(nln-1)*10
            f.write('  NegKG_{:<2}  {}  KG{}  wsum  {}\n'.format(nln,10," KG".join(glist[-rem:])," ".join(["{:.3f}".format(-1/rem)]*rem)))
            f.write('  NegKG_all {}  NegKG_{}  wsum  {}\n'.format(nln," NegKG_".join([str(i+1) for i in np.arange(nln)])," ".join(["{:.3f}".format(-1/nln)]*nln)))
        f.write('EndTiedRespVars\n')


        f.write('\nBeginGCOP\n')
        if len(glist)<10:
            f.write('  #CostFunction NegNS\n')
            f.write('  CostFunction NegKG\n')
        else:
            f.write('  CostFunction NegKG_all\n')
        f.write('  PenaltyFunction APM\n')
        f.write('EndGCOP\n')

        f.write("""\nBeginConstraints
  # not needed when no constraints, but PenaltyFunction statement above is required
  # name     type     penalty    lwr   upr   resp.var
EndConstraints

# Randomsed control added
#RandomSeed 12345

#Algorithm should be last in this file:
BeginDDSAlg
  PerturbationValue 0.20
  MaxIterations {}
  UseRandomParamValues
  #UseInitialParamValues   # intializes DDS to parameter values IN the initial model input files
EndDDSAlg""".format(nsmpl))