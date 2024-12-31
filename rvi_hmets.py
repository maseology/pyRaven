
import time

# build Primary Input file (.rvi)
def write(root, nam, builder, ver, dtb, dte, res, intvl, preciponly, silentmode=False):
    with open(root + nam + ".rvi","w") as f:
        f.write('# -------------------------------------------------------\n')
        f.write('# Raven Input (.rvi) file\n')
        f.write('# HMETS semi-distributed watershed model\n')
        f.write('# written by ' + builder + '\n')
        f.write('# using pyRaven builder\n')
        f.write('# Raven version: ' + ver + '\n')
        f.write('# -------------------------------------------------------\n\n')

        f.write(':RunName ' + nam + '\n')
        f.write(':OutputDirectory ' + root + "output\n")
        f.write(':StartDate ' + dtb.strftime("%Y-%m-%d %H:%M:%S") + '\n')
        f.write(':EndDate   ' + dte.strftime("%Y-%m-%d %H:%M:%S") + '\n')
        if intvl < 86400:
            f.write(':TimeStep  ' + time.strftime('%H:%M:%S', time.gmtime(intvl)) + '\n\n')
        else:
            f.write(':TimeStep  {}'.format(intvl/86400) + '\n\n')

        # :Method
        f.write(':PotentialMeltMethod  POTMELT_HMETS\n')
        if preciponly:
            f.write(':RainSnowFraction     RAINSNOW_HBV\n')
        else:
            f.write(':RainSnowFraction     RAINSNOW_DATA\n')
        f.write(':Evaporation          PET_HARGREAVES_1985\n')
        f.write(':CatchmentRoute       ROUTE_GAMMA_CONVOLUTION\n')
        f.write(':Routing              ROUTE_DIFFUSIVE_WAVE\n\n')

        f.write(':SoilModel            SOIL_TWO_LAYER\n\n') # Two soil layers

        f.write(':Alias DELAYED_RUNOFF CONVOLUTION[1]\n\n')

        f.write('\n# hydrologic process order for HMETS emulation\n')
        f.write(':HydrologicProcesses    #  ALGORITHM            ProcessFrom      ProcessTo\n') 
        f.write(' :SnowBalance              SNOBAL_HMETS         MULTIPLE         MULTIPLE\n')
        f.write(' :Precipitation            RAVEN_DEFAULT        ATMOS_PRECIP     MULTIPLE\n')
        f.write(' :Infiltration             INF_HMETS            PONDED_WATER     MULTIPLE\n')         
        f.write('  :Overflow                OVERFLOW_RAVEN       SOIL[0]          DELAYED_RUNOFF\n')
        f.write(' :Baseflow                 BASE_LINEAR          SOIL[0]          SURFACE_WATER     # Interflow\n')
        f.write(' :Percolation              PERC_LINEAR          SOIL[0]          SOIL[1]           # Recharge\n')
        f.write('  :Overflow                OVERFLOW_RAVEN       SOIL[1]          DELAYED_RUNOFF\n')
        f.write(' :SoilEvaporation          SOILEVAP_ALL         SOIL[0]          ATMOSPHERE        # AET\n')
        f.write(' :Convolve                 CONVOL_GAMMA         CONVOLUTION[0]   SURFACE_WATER     # Surface runoff\n')
        f.write(' :Convolve                 CONVOL_GAMMA_2       DELAYED_RUNOFF   SURFACE_WATER     # Delayed runoff\n')
        f.write(' :Baseflow                 BASE_LINEAR          SOIL[1]          SURFACE_WATER     # Baseflow\n')
        f.write(':EndHydrologicProcesses\n')


        f.write('\n# output options\n')
        f.write(':WriteMassBalanceFile\n')
        f.write(':WriteForcingFunctions\n')

        f.write(':DefineHRUGroups LandHRUs LakeHRUs\n')
        f.write(':EvaluationMetrics KLING_GUPTA NASH_SUTCLIFFE PCT_BIAS\n')

        f.write('\n# output recharge\n')
        # f.write('\n:WriteNetCDFFormat\n')
        f.write(':CustomOutput MONTHLY AVERAGE  To:SOIL[1]  BY_HRU\n')   # monthly recharge by hru
        f.write(':CustomOutput DAILY   AVERAGE  To:SOIL[1]  BY_BASIN\n') # daily recharge by sub-watershed
        f.write(':CustomOutput DAILY   AVERAGE  SNOW        BY_BASIN\n') # daily snowpack by sub-watershed
        f.write(':CustomOutput DAILY   AVERAGE  AET         BY_BASIN\n') # daily evapotranspiration by sub-watershed
        f.write(':CustomOutput DAILY   AVERAGE  SOIL[0]     BY_BASIN\n') # daily soil moisture by sub-watershed
        f.write(':CustomOutput DAILY   AVERAGE  SOIL[1]     BY_BASIN\n') # daily soil moisture by sub-watershed
 
        if res is not None:
            f.write('\n# output reservoir mass balance\n')
            f.write(':WriteReservoirMBFile\n')

        if silentmode:
            f.write('\n:SilentMode\n')
            f.write(':SuppressOutput\n')
