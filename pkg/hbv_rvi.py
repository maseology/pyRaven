
import time

# build Primary Input file (.rvi)
def write(root, nam, builder, ver, met):
    with open(root + nam + ".rvi","w") as f:
        f.write('# -------------------------------------------------------\n')
        f.write('# Raven Input (.rvi) file\n')
        f.write('# HBV-EC semi-distributed watershed model\n')
        f.write('# written by ' + builder + '\n')
        f.write('# using pyRaven builder\n')
        f.write('# Raven version: ' + ver + '\n')
        f.write('# -------------------------------------------------------\n\n')

        f.write(':RunName ' + nam + '\n')
        f.write(':OutputDirectory ' + root + "output\n")
        f.write(':StartDate ' + met.dtb.strftime("%Y-%m-%d %H:%M:%S") + '\n')
        f.write(':EndDate   ' + met.dte.strftime("%Y-%m-%d %H:%M:%S") + '\n')
        if met.intvl < 86400:
            f.write(':TimeStep  ' + time.strftime('%H:%M:%S', time.gmtime(met.intvl)) + '\n\n')
        else:
            f.write(':TimeStep  {}'.format(met.intvl/86400) + '\n\n')


        f.write(':SoilModel            SOIL_MULTILAYER 3\n')
        # SOIL_ONE_LAYER - Single soil layer
        # SOIL_TWO_LAYER - Two soil layers
        # SOIL_MULTILAYER [number of layers] - Any number of soil layers

        f.write(':CatchmentRoute       ROUTE_TRI_CONVOLUTION\n')
        f.write(':Routing              ROUTE_HYDROLOGIC\n')
        # :Method
        f.write(':InterpolationMethod  INTERP_NEAREST_NEIGHBOR\n') # INTERP_NEAREST_NEIGHBOR is default
        f.write(':RainSnowFraction     RAINSNOW_DATA\n')
        f.write(':PotentialMeltMethod  POTMELT_HBV\n')
        f.write(':Evaporation          PET_HARGREAVES_1985\n')
        f.write(':OW_Evaporation       PET_HARGREAVES_1985\n')
        # :DirectEvaporation
        # :OroPrecipCorrect
        # :OroTempCorrect
        # :OroPETCorrect
        # :SWRadiationMethod
        # :SWCanopyCorrect
        # :SWCloudCorrect
        # :LWRadiationMethod
        # :CloudCoverMethod 
        # :WindspeedMethod
        # :RelativeHumidityMethod
        # :AirPressureMethod 
        f.write(':PrecipIceptFract     PRECIP_ICEPT_USER\n')
        # :PotentialMelt
        # :MonthlyInterpolationMethod
        # :SubDailyMethod
        # :LakeStorage


        f.write('\n# HBV-EC reservoir aliases\n')
        f.write(':Alias                FAST_RESERVOIR SOIL[1]\n')
        f.write(':Alias                SLOW_RESERVOIR SOIL[2]\n')
        f.write(':LakeStorage          SLOW_RESERVOIR\n')


        f.write('\n# hydrologic process order for HBV-EC emulation\n')
        f.write(':HydrologicProcesses    #  ALGORITHM            ProcessFrom      ProcessTo\n') 
        #  The state variables SURFACE_WATER, PONDED_WATER, ATMOS_PRECIP and ATMOSPHERE are automatically included in all models
        #  MULTIPLE tag is a placeholder, indicating that there are more than one compartments either receiving water/energy/mass, or more than one losing.
        #         :ProcessName              ALGORITHM          {ProcessFrom}    {ProcessTo}
        # f.write('\n#                          ALGORITHM          ProcessFrom      ProcessTo\n')
        f.write(' :SnowRefreeze             FREEZE_DEGREE_DAY    SNOW_LIQ         SNOW\n') 
        f.write(' :Precipitation            PRECIP_RAVEN         ATMOS_PRECIP     MULTIPLE\n')
        f.write(' :CanopyEvaporation        CANEVP_ALL           CANOPY           ATMOSPHERE\n')
        f.write(' :CanopySnowEvap           CANEVP_ALL           CANOPY_SNOW      ATMOSPHERE\n')
        
        f.write(' :SnowBalance              SNOBAL_SIMPLE_MELT   SNOW             SNOW_LIQ\n')
        f.write('  :-->Overflow             RAVEN_DEFAULT        SNOW_LIQ         PONDED_WATER\n')

        f.write(' :Infiltration             INF_HBV              PONDED_WATER     MULTIPLE\n')                                                         
        f.write(' :Flush                    RAVEN_DEFAULT        SURFACE_WATER    FAST_RESERVOIR\n')

        f.write(' :SoilEvaporation          SOILEVAP_HBV         SOIL[0]          ATMOSPHERE\n')
        f.write(' :CapillaryRise            CRISE_HBV            FAST_RESERVOIR   SOIL[0]\n')
        f.write(' :SoilEvaporation          SOILEVAP_HBV         FAST_RESERVOIR   ATMOSPHERE\n')
        f.write(' :Percolation              PERC_CONSTANT        FAST_RESERVOIR   SLOW_RESERVOIR\n')
        f.write(' :Baseflow                 BASE_THRESH_STOR     FAST_RESERVOIR   SURFACE_WATER\n')
        f.write(' :Baseflow                 BASE_POWER_LAW       FAST_RESERVOIR   SURFACE_WATER\n')
        f.write(' :Baseflow                 BASE_LINEAR          SLOW_RESERVOIR   SURFACE_WATER\n')

        f.write(':EndHydrologicProcesses\n')


        f.write('\n# output options\n')
        f.write(':WriteMassBalanceFile\n')
        f.write(':WriteForcingFunctions\n')
        # f.write(':CustomOutput DAILY AVERAGE SNOW BY_HRU\n')
        f.write(':AggregatedVariable FAST_RESERVOIR AllHRUs\n')
        f.write(':AggregatedVariable SLOW_RESERVOIR AllHRUs\n')
        f.write(':EvaluationMetrics KLING_GUPTA NASH_SUTCLIFFE PCT_BIAS\n')

        # f.write('\n:WriteNetCDFFormat\n')
        f.write(':CustomOutput MONTHLY AVERAGE To:SLOW_RESERVOIR BY_HRU\n') # monthly recharge by hru

        # :SilentMode
        # :SuppressOutput
