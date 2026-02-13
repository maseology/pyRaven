
import time
from pyRaven.flags import flg

# build Primary Input file (.rvi)
def write(root, nam, builder, ver, dtb, dte, res, intvl):
    with open(root + nam + ".rvi","w") as f:
        f.write('# -------------------------------------------------------\n')
        f.write('# Raven Input (.rvi) file\n')
        f.write('# GR4J lumped watershed model\n')
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
        # f.write(':PotentialMeltMethod  POTMELT_DEGREE_DAY\n')
        # if flg.preciponly or flg.precipactive:
        #     f.write(':RainSnowFraction     RAINSNOW_DINGMAN\n')
        # else:
        #     f.write(':RainSnowFraction     RAINSNOW_DATA\n')
        f.write(':RainSnowFraction     RAINSNOW_THRESHOLD\n')
        f.write(':Evaporation          PET_OUDIN\n\n') #PET_HARGREAVES_1985\n\n')

        f.write(':SoilModel            SOIL_MULTILAYER 4\n\n')

        # f.write(':AllowSoilOverfill\n\n') # soils may be filled beyond their maximum storage capacity, generally recommended for the HMETS model

        f.write(':Alias PRODUCT_STORE    SOIL[0]\n')
        f.write(':Alias ROUTING_STORE    SOIL[1]\n')
        f.write(':Alias TEMP_STORE       SOIL[2]\n')
        f.write(':Alias GW_STORE         SOIL[3]\n\n')

        f.write('\n# hydrologic process order for GR4J simulation\n')
        f.write(':HydrologicProcesses    #  ALGORITHM            ProcessFrom      ProcessTo\n') 
        f.write(' :Precipitation            RAVEN_DEFAULT        ATMOS_PRECIP     MULTIPLE\n')
        f.write(' :SnowBalance              SNOBAL_SIMPLE_MELT   SNOW             PONDED_WATER\n')
        f.write(' :OpenWaterEvaporation     OPEN_WATER_EVAP      PONDED_WATER     ATMOSPHERE                            # Pn\n')
        f.write(' :Infiltration             INF_GR4J             PONDED_WATER     MULTIPLE                              # Ps-\n')
        f.write(' :SoilEvaporation          SOILEVAP_GR4J        PRODUCT_STORE    ATMOSPHERE                            # Es\n')
        f.write(' :Percolation              PERC_GR4J            PRODUCT_STORE    TEMP_STORE                            # Perc\n')
        f.write(' :Flush                    RAVEN_DEFAULT        SURFACE_WATER    TEMP_STORE                            # Pn-Ps\n')
        f.write(' :Split                    RAVEN_DEFAULT        TEMP_STORE       CONVOLUTION[0]  CONVOLUTION[1]  0.9   # Pr\n')
        f.write(' :Convolve                 CONVOL_GR4J_1        CONVOLUTION[0]   ROUTING_STORE                         # Q9\n')
        f.write(' :Convolve                 CONVOL_GR4J_2        CONVOLUTION[1]   TEMP_STORE                            # Q1\n')
        f.write(' :Percolation              PERC_GR4JEXCH        ROUTING_STORE    GW_STORE                              # F(x1)\n')
        f.write(' :Percolation              PERC_GR4JEXCH2       TEMP_STORE       GW_STORE                              # F(x1)\n')
        f.write(' :Flush                    RAVEN_DEFAULT        TEMP_STORE       SURFACE_WATER                         # Qd\n')
        f.write(' :Baseflow                 BASE_GR4J            ROUTING_STORE    SURFACE_WATER                         # Qr\n')
        f.write(':EndHydrologicProcesses\n')


        f.write('\n# output options\n')
        f.write(':EvaluationMetrics KLING_GUPTA NASH_SUTCLIFFE PCT_BIAS\n')
        # if flg.calibrationmode:
        #     f.write(':EvaluationPeriod CALIBRATION {}-10-01 {}\n'.format(int(0.5*(dte.year-(dtb.year+1))+dtb.year+1), dte.strftime("%Y-%m-%d")))
        #     # f.write(':EvaluationPeriod CALIBRATION {} {}\n'.format(dtb.strftime("%Y-%m-%d"), dte.strftime("%Y-%m-%d")))

        cmnt = ''
        if flg.calibrationmode: cmnt='# '
        f.write('\n{}:WriteMassBalanceFile\n'.format(cmnt))
        # f.write('\n{}:WriteExhaustiveMB\n'.format(cmnt))        
        f.write('{}:WriteForcingFunctions\n'.format(cmnt))
        # f.write('\n# output waterbudgets\n')
        # # f.write('\n{}:WriteNetCDFFormat\n'.format(cmnt))
        # f.write('{}:CustomOutput MONTHLY CUMULSUM  PRECIP                                   BY_HRU\n'.format(cmnt))   # monthly precipitation by hru
        # f.write('{}:CustomOutput MONTHLY CUMULSUM  AET                                      BY_HRU\n'.format(cmnt))   # monthly evapotranspiration by hru
        # f.write('{}:CustomOutput MONTHLY AVERAGE   Between:PONDED_WATER.And.SURFACE_WATER   BY_HRU\n'.format(cmnt))   # impervious/direct runoff
        # f.write('{}:CustomOutput MONTHLY AVERAGE   Between:PONDED_WATER.And.QUICK_RUNOFF    BY_HRU\n'.format(cmnt))   # pervious runoff "surface runoff"
        # f.write('{}:CustomOutput MONTHLY AVERAGE   Between:PONDED_WATER.And.DELAYED_RUNOFF  BY_HRU\n'.format(cmnt))   # "delayed runoff"
        # f.write('{}:CustomOutput MONTHLY AVERAGE   Between:VADOSE_ZONE.And.DELAYED_RUNOFF   BY_HRU\n'.format(cmnt))   # saturation/vadose excess
        # f.write('{}:CustomOutput MONTHLY AVERAGE   Between:PHREATIC_ZONE.And.DELAYED_RUNOFF BY_HRU\n'.format(cmnt))   # groundwater/phreatic excess        
        # f.write('{}:CustomOutput MONTHLY AVERAGE   Between:VADOSE_ZONE.And.SURFACE_WATER    BY_HRU\n'.format(cmnt))   # interflow
        # f.write('{}:CustomOutput MONTHLY AVERAGE   Between:PHREATIC_ZONE.And.SURFACE_WATER  BY_HRU\n'.format(cmnt))   # baseflow

        # f.write('{}:CustomOutput MONTHLY AVERAGE   Between:PONDED_WATER.And.VADOSE_ZONE     BY_HRU\n'.format(cmnt))   # infiltration
        # f.write('{}:CustomOutput MONTHLY AVERAGE   To:PHREATIC_ZONE                         BY_HRU\n'.format(cmnt))   # recharge

        # f.write('{}:CustomOutput MONTHLY AVERAGE   VADOSE_ZONE                              BY_HRU\n'.format(cmnt))   # vadose zone storage
        # f.write('{}:CustomOutput MONTHLY AVERAGE   PHREATIC_ZONE                            BY_HRU\n'.format(cmnt))   # phreatic zone storage
        # f.write('{}:CustomOutput MONTHLY AVERAGE   QUICK_RUNOFF                             BY_HRU\n'.format(cmnt))   # CONVOLUTION[0] storage
        # f.write('{}:CustomOutput MONTHLY AVERAGE   DELAYED_RUNOFF                           BY_HRU\n'.format(cmnt))   # CONVOLUTION[1] storage

        # # f.write('{}:CustomOutput MONTHLY CUMULSUM  To:QUICK_RUNOFF   BY_HRU\n'.format(cmnt))   # pervious runoff (infiltration excess)
        # # f.write('{}:CustomOutput MONTHLY CUMULSUM  To:DELAYED_RUNOFF BY_HRU\n'.format(cmnt))   # delayed runoff
        # # f.write('{}:CustomOutput MONTHLY AVERAGE   To:SURFACE_WATER  BY_HRU\n'.format(cmnt))   # monthly runoff by hru
        # # f.write('{}:CustomOutput DAILY   AVERAGE   SNOW              BY_BASIN\n'.format(cmnt)) # daily snowpack by sub-watershed
        # # f.write('{}:CustomOutput DAILY   AVERAGE   AET               BY_BASIN\n'.format(cmnt)) # daily evapotranspiration by sub-watershed
        # # f.write('{}:CustomOutput DAILY   AVERAGE   SOIL[0]           BY_BASIN\n'.format(cmnt)) # daily soil moisture by sub-watershed
        # # f.write('{}:CustomOutput DAILY   AVERAGE   SOIL[1]           BY_BASIN\n'.format(cmnt)) # daily soil moisture by sub-watershed


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