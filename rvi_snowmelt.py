
from pyRaven.flags import flg

# build Primary Input file (.rvi)
def write(root, nam, builder, ver, wshd, met):
    with open(root + nam + ".rvi","w") as f:
        f.write('# -------------------------------------------------------\n')
        f.write('# Raven Input (.rvi) file\n')
        f.write('# daily snowmelt model\n')
        f.write('# written by ' + builder + '\n')
        f.write('# using pyRaven builder\n')
        f.write('# Raven version: ' + ver + '\n')
        f.write('# -------------------------------------------------------\n\n')

        f.write(':RunName ' + nam + '\n')
        f.write(':OutputDirectory ' + root + "output\n")
        f.write(':StartDate ' + met.dtb.strftime("%Y-%m-%d %H:%M:%S") + '\n')
        f.write(':EndDate   ' + met.dte.strftime("%Y-%m-%d %H:%M:%S") + '\n')
        f.write(':TimeStep  1.0\n\n')


        f.write(':SoilModel            SOIL_ONE_LAYER\n')
        f.write(':Routing              ROUTE_NONE\n')
        f.write(':CatchmentRoute       DUMP\n')
        if len(wshd.xr) > 1: f.write(':InterpolationMethod  INTERP_FROM_FILE          GaugeWeightTable.txt\n')
        if flg.preciponly:
            f.write(':RainSnowFraction     RAINSNOW_HBV\n')
        else:
            f.write(':RainSnowFraction     RAINSNOW_DATA\n')


        f.write(':PotentialMeltMethod  POTMELT_DEGREE_DAY\n')


        f.write('\n# hydrologic process order for basin snowmelt emulation\n')
        f.write(':HydrologicProcesses    #  ALGORITHM            ProcessFrom      ProcessTo\n') 
        f.write(' :SnowRefreeze             FREEZE_DEGREE_DAY    SNOW_LIQ         SNOW\n')
        f.write(' :Precipitation            PRECIP_RAVEN         ATMOS_PRECIP     MULTIPLE\n')
        f.write(' :CanopyEvaporation        CANEVP_ALL           CANOPY           ATMOSPHERE\n')
        f.write(' :CanopySublimation        CANEVP_ALL           CANOPY_SNOW      ATMOSPHERE\n')
        f.write(' :SnowBalance              SNOBAL_SIMPLE_MELT   SNOW             SNOW_LIQ\n')
        f.write('  :-->Overflow             RAVEN_DEFAULT        SNOW_LIQ         PONDED_WATER\n')
        f.write(':EndHydrologicProcesses\n')


        f.write('\n# output options\n')
        # f.write(':WriteMassBalanceFile\n')
        # f.write(':WriteForcingFunctions\n')
        # f.write(':CustomOutput DAILY AVERAGE SNOW_DEPTH BY_HRU\n') # only works for SNOBAL_HBV SNOBAL_GAWSER
        # f.write(':CustomOutput DAILY AVERAGE SNOW BY_HRU\n')

        # f.write(':EvaluationMetrics KLING_GUPTA NASH_SUTCLIFFE PCT_BIAS\n')

        # f.write('\n:WriteNetCDFFormat\n')
        # f.write(':CustomOutput MONTHLY AVERAGE To:SLOW_RESERVOIR BY_HRU\n') # monthly recharge by hru

        f.write('\n:SilentMode\n') # output to the command prompt is minimized
        # f.write(':SuppressOutput\n') # Suppresses all standard output (including :CustomOutput above), including generation of Hydrograph, transport output, and watershed storage files. Does not turn of optional outputs which were requested elsewhere in the input file
