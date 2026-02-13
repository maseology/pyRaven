
import shutil
import numpy as np
from pyRaven.flags import flg
from pymmio import files as mmio

def writeDDS(root, nam, nsmpl=10):
    
    rfn = 'Raven3.8.exe'
    ofn = 'Ostrich_v20171219_Windows.exe'

    shutil.copy("E:/Sync/@dev/Raven-bin/"+ofn,root+ofn)

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
        f.write('  {0}.rvp.tpl;  {0}.rvp\n'.format(nam))
        f.write('EndFilePairs\n')
        
        f.write('\nBeginParams\n')
        f.write('  #parameter                    init.     low      high   tx_in tx_ost  tx_out\n')
        f.write('  x1                           random     0.0       1.0    none   none    none\n')  # production zone soil depth [m]
        f.write('  x2                           random     0.0      25.0    none   none    none\n')  # maximum groundwater exchange rate [mm/d]
        f.write('  x3                           random     0.0    1000.0    none   none    none\n')  # baseflow reference storage [mm]
        f.write('  x4                           random     0.0     100.0    none   none    none\n')  # transfer function parameter
        f.write('EndParams\n')
        f.write('\n')
        f.write('BeginTiedParams\n')
        f.write('EndTiedParams\n')

        f.write('\nBeginResponseVars\n')
        f.write('  #name             filename                                           keyword         line    col     token\n')
        dfp = './model/output/{}_Diagnostics.csv'.format(nam)
        f.write('  KGE               {:48};  OST_NULL        1         3       \',\'\n'.format(dfp))
        f.write('EndResponseVars\n')

        f.write('\nBeginTiedRespVars\n')
        f.write('  NegKG  1  KGE  wsum  -1.000\n')
        f.write('EndTiedRespVars\n')

        f.write('\nBeginGCOP\n')
        f.write('  CostFunction NegKG\n')
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