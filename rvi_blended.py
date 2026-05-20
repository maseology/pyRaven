
import time
from datetime import timedelta
from pymmio import files as mmio
from pyRaven.flags import flg

# build Primary Input file (.rvi)
def write(root, nam, builder, ver, dtb, dte, res, intvl):

    def write_rvi(fp, astpl):
        with open(fp,"w") as f:
            f.write('# -------------------------------------------------------\n')
            f.write('# Raven Input (.rvi) file\n')
            f.write('# Blended lumped watershed model\n')
            f.write('# written by ' + builder + '\n')
            f.write('# using pyRaven builder\n')
            f.write('# Raven version: ' + ver + '\n')
            f.write('# -------------------------------------------------------\n\n')

            f.write(':RunName ' + nam + '\n')
            # f.write(':OutputDirectory ' + "output\n")
            f.write(':StartDate ' + dtb.strftime("%Y-%m-%d %H:%M:%S") + '\n')
            f.write(':EndDate   ' + dte.strftime("%Y-%m-%d %H:%M:%S") + '\n')
            if intvl < 86400:
                f.write(':TimeStep  ' + time.strftime('%H:%M:%S', time.gmtime(intvl)) + '\n\n')
            else:
                f.write(':TimeStep  {}'.format(intvl/86400) + '\n\n')

            # :Method
            f.write(':InterpolationMethod  INTERP_NEAREST_NEIGHBOR\n') # INTERP_NEAREST_NEIGHBOR is default
            f.write(':Routing              ROUTE_NONE\n')
            f.write(':CatchmentRoute       ROUTE_DUMP\n')
            # f.write(':PotentialMeltMethod POTMELT_HMETS\n') # snow melt pre-computed by OWRC API
            f.write(':RainSnowFraction     RAINSNOW_THRESHOLD\n')
            f.write(':Evaporation          PET_BLENDED\n')
            f.write(':SoilModel            SOIL_MULTILAYER 3\n\n')

            if astpl:
                f.write(':BlendedPETWeights    PET_OUDIN xBlndPET1 PET_HAMON xBlndPET2 PET_HARGREAVES_1985\n\n')
            else:
                f.write(':BlendedPETWeights    PET_OUDIN 0.55556 PET_HAMON 0.5 PET_HARGREAVES_1985\n\n')

            f.write(':Alias DELAYED_RUNOFF CONVOLUTION[1]\n')

            f.write('\n# hydrologic process order for Blended (Mai etal., 2020) simulation\n')
            f.write(':HydrologicProcesses    #  ALGORITHM            ProcessFrom      ProcessTo\n') 
            f.write(' :Precipitation            RAVEN_DEFAULT        ATMOS_PRECIP     MULTIPLE\n')
            f.write(' :SnowBalance              SNOBAL_SIMPLE_MELT   SNOW             PONDED_WATER\n')

            f.write(' :ProcessGroup          # infiltration group\n')
            f.write('  :Infiltration            INF_HMETS            PONDED_WATER     MULTIPLE\n')
            f.write('  :Infiltration            INF_VIC_ARNO         PONDED_WATER     MULTIPLE\n')
            f.write('  :Infiltration            INF_HBV              PONDED_WATER     MULTIPLE\n')
            if astpl:
                f.write(' :EndProcessGroup CALCULATE_WTS xBlndInf1 xBlndInf2\n')
            else:
                f.write(' :EndProcessGroup CALCULATE_WTS 0.55556 0.5\n')

            f.write(' :Overflow OVERFLOW_RAVEN SOIL[0] DELAYED_RUNOFF\n')

            f.write(' :ProcessGroup          # quickflow group\n')
            f.write('  :Baseflow                BASE_LINEAR_ANALYTIC SOIL[0]          SURFACE_WATER\n')
            f.write('  :Baseflow                BASE_VIC             SOIL[0]          SURFACE_WATER\n')
            f.write('  :Baseflow                BASE_TOPMODEL        SOIL[0]          SURFACE_WATER\n')
            if astpl:
                f.write(' :EndProcessGroup CALCULATE_WTS xBlndQF1 xBlndQF2\n')
            else:
                f.write(' :EndProcessGroup CALCULATE_WTS 0.55556 0.5\n')

            f.write(' :Percolation              PERC_LINEAR          SOIL[0]          SOIL[1]\n')
            f.write(' :Overflow                 OVERFLOW_RAVEN       SOIL[1]          DELAYED_RUNOFF\n')
            f.write(' :Percolation              PERC_LINEAR          SOIL[1]          SOIL[2]\n')

            f.write(' :ProcessGroup          # evaporation group\n')
            f.write('  :SoilEvaporation         SOILEVAP_ALL         SOIL[0]          ATMOSPHERE\n')
            f.write('  :SoilEvaporation         SOILEVAP_HBV         SOIL[0]          ATMOSPHERE\n')
            if astpl:
                f.write(' :EndProcessGroup CALCULATE_WTS xBlndSoilEvap\n')
            else:
                f.write(' :EndProcessGroup CALCULATE_WTS 0.5\n')
            # f.write(' :OpenWaterEvaporation     OPEN_WATER_EVAP      PONDED_WATER     ATMOSPHERE\n') # not in original Mai blended

            f.write(' :Convolve                 CONVOL_GAMMA         CONVOLUTION[0]   SURFACE_WATER\n')
            f.write(' :Convolve                 CONVOL_GAMMA_2       DELAYED_RUNOFF   SURFACE_WATER\n')

            f.write(' :ProcessGroup          # baseflow group\n')
            f.write('  :Baseflow                BASE_LINEAR_ANALYTIC SOIL[1]          SURFACE_WATER\n')
            f.write('  :Baseflow                BASE_POWER_LAW       SOIL[1]          SURFACE_WATER\n')
            if astpl:
                f.write(' :EndProcessGroup CALCULATE_WTS xBlndBF\n')
            else:
                f.write(' :EndProcessGroup CALCULATE_WTS 0.5\n')

            f.write(':EndHydrologicProcesses\n')        


            f.write('\n# output options\n')
            f.write(':EvaluationMetrics KLING_GUPTA NASH_SUTCLIFFE PCT_BIAS\n')
            if flg.calibrationmode:
                # f.write(':EvaluationPeriod CALIBRATION {}-10-01 {}\n'.format(int(0.5*(dte.year-(dtb.year+1))+dtb.year+1), dte.strftime("%Y-%m-%d")))
                # f.write(':EvaluationPeriod CALIBRATION {} {}\n'.format(dtb.strftime("%Y-%m-%d"), dte.strftime("%Y-%m-%d")))
                f.write(':EvaluationPeriod CALIBRATION {} {}\n'.format((dtb + timedelta(days=365)).strftime("%Y-%m-%d"), dte.strftime("%Y-%m-%d")))

            cmnt = ''
            if flg.calibrationmode: cmnt='# '
            f.write('\n{}:WriteMassBalanceFile\n'.format(cmnt))        
            f.write('{}:WriteForcingFunctions\n'.format(cmnt))

            if not flg.calibrationmode and res is not None:
                f.write('\n# output reservoir mass balance\n')
                f.write(':WriteReservoirMBFile\n')

            if flg.calibrationmode:
                f.write('\n:SilentMode\n')
                f.write(':SuppressOutput\n')
                f.write(':DontWriteWatershedStorage\n')
            else:
                # :NoisyMode
                f.write('\n#:SilentMode\n')
                f.write('#:SuppressOutput\n')
                f.write('#:DontWriteWatershedStorage\n')
    
    write_rvi(root + nam + ".rvi", False)
    if flg.calibrationmode: write_rvi(mmio.getFileDir(root) +"/"+ nam + ".rvi.tpl", True)
