
import time
from pyRaven.flags import flg

# build Primary Input file (.rvi)
def write(root, nam, builder, ver, dtb, dte, res, intvl):
    with open(root + nam + ".rvi","w") as f:
        f.write('# -------------------------------------------------------\n')
        f.write('# Raven Input (.rvi) file\n')
        f.write('# HMETS semi-distributed watershed model\n')
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
        f.write(':PotentialMeltMethod  POTMELT_HMETS\n')
        if flg.preciponly:
            f.write(':RainSnowFraction     RAINSNOW_HBV\n')
        else:
            f.write(':RainSnowFraction     RAINSNOW_DATA\n')
        f.write(':Evaporation          PET_HARGREAVES_1985\n') # PET_OUDIN used in HMETS
        f.write(':PrecipIceptFract     PRECIP_ICEPT_LAI\n')
        # f.write(':InterpolationMethod  INTERP_FROM_FILE  {}\n'.format(nam + "-GaugeWeightTable.txt"))
        f.write(':CatchmentRoute       ROUTE_GAMMA_CONVOLUTION\n')
        f.write(':Routing              ROUTE_DIFFUSIVE_WAVE\n\n')

        f.write(':SoilModel            SOIL_TWO_LAYER\n\n') # Two soil layers

        f.write(':Alias VADOSE_ZONE    SOIL[0]\n')
        f.write(':Alias PHREATIC_ZONE  SOIL[1]\n')
        f.write(':Alias QUICK_RUNOFF   CONVOLUTION[0]\n')
        f.write(':Alias DELAYED_RUNOFF CONVOLUTION[1]\n')
        f.write(':DefineHRUGroups LakeHRUs LandHRUs\n\n')


        f.write('\n# hydrologic process order for HMETS emulation\n')
        f.write(':HydrologicProcesses    #  ALGORITHM            ProcessFrom      ProcessTo\n') 
        f.write(' :SnowBalance              SNOBAL_HMETS         MULTIPLE         MULTIPLE\n')
        f.write(' :Precipitation            RAVEN_DEFAULT        ATMOS_PRECIP     MULTIPLE\n')
        f.write(' :CanopyEvaporation        CANEVP_ALL           CANOPY           ATMOSPHERE\n')
        f.write(' :CanopySublimation        CANEVP_ALL           CANOPY_SNOW      ATMOSPHERE\n')  
        f.write(' :Infiltration             INF_HMETS            PONDED_WATER     MULTIPLE\n')         
        f.write('  :Overflow                OVERFLOW_RAVEN       VADOSE_ZONE      DELAYED_RUNOFF\n')
        f.write(' :Baseflow                 BASE_LINEAR          VADOSE_ZONE      SURFACE_WATER     # Interflow  "hypodermic flow" in Martel etal. (2017)\n')
        f.write(' :Percolation              PERC_CONSTANT        VADOSE_ZONE      PHREATIC_ZONE     # Groundwater recharge\n')
        f.write('  :Overflow                OVERFLOW_RAVEN       PHREATIC_ZONE    DELAYED_RUNOFF\n')
        f.write(' :SoilEvaporation          SOILEVAP_ALL         VADOSE_ZONE      ATMOSPHERE        # AET\n')
        f.write(' :Convolve                 CONVOL_GAMMA         QUICK_RUNOFF     SURFACE_WATER     # Surface runoff\n')
        f.write(' :Convolve                 CONVOL_GAMMA_2       DELAYED_RUNOFF   SURFACE_WATER     # Delayed runoff\n')
        f.write(' :Baseflow                 BASE_LINEAR          PHREATIC_ZONE    SURFACE_WATER     # Baseflow  "groundwater flow" in Martel etal. (2017)\n')
        f.write(' :LateralEquilibrate       RAVEN_DEFAULT        LandHRUs         VADOSE_ZONE       1.0\n')
        f.write(' :LateralEquilibrate       RAVEN_DEFAULT        LandHRUs         PHREATIC_ZONE     1.0\n')
        f.write(':EndHydrologicProcesses\n')


        f.write('\n# output options\n')
        f.write(':EvaluationMetrics KLING_GUPTA NASH_SUTCLIFFE PCT_BIAS\n')
        if flg.calibrationmode:
            f.write(':EvaluationPeriod CALIBRATION {}-10-01 {}\n'.format(int(0.5*(dte.year-(dtb.year+1))+dtb.year+1), dte.strftime("%Y-%m-%d")))

        cmnt = ''
        if flg.calibrationmode: cmnt='# '
        f.write('\n{}:WriteMassBalanceFile\n'.format(cmnt))
        # f.write('\n{}:WriteExhaustiveMB\n'.format(cmnt))        
        f.write('{}:WriteForcingFunctions\n'.format(cmnt))
        f.write('\n# output waterbudgets\n')
        # f.write('\n{}:WriteNetCDFFormat\n'.format(cmnt))
        f.write('{}:CustomOutput MONTHLY CUMULSUM  PRECIP                                   BY_HRU\n'.format(cmnt))   # monthly precipitation by hru
        f.write('{}:CustomOutput MONTHLY CUMULSUM  AET                                      BY_HRU\n'.format(cmnt))   # monthly evapotranspiration by hru
        f.write('{}:CustomOutput MONTHLY AVERAGE   Between:PONDED_WATER.And.SURFACE_WATER   BY_HRU\n'.format(cmnt))   # impervious/direct runoff
        f.write('{}:CustomOutput MONTHLY AVERAGE   Between:PONDED_WATER.And.QUICK_RUNOFF    BY_HRU\n'.format(cmnt))   # pervious runoff "surface runoff"
        f.write('{}:CustomOutput MONTHLY AVERAGE   Between:PONDED_WATER.And.DELAYED_RUNOFF  BY_HRU\n'.format(cmnt))   # "delayed runoff"
        f.write('{}:CustomOutput MONTHLY AVERAGE   Between:VADOSE_ZONE.And.DELAYED_RUNOFF   BY_HRU\n'.format(cmnt))   # saturation/vadose excess
        f.write('{}:CustomOutput MONTHLY AVERAGE   Between:PHREATIC_ZONE.And.DELAYED_RUNOFF BY_HRU\n'.format(cmnt))   # groundwater/phreatic excess        
        f.write('{}:CustomOutput MONTHLY AVERAGE   Between:VADOSE_ZONE.And.SURFACE_WATER    BY_HRU\n'.format(cmnt))   # interflow
        f.write('{}:CustomOutput MONTHLY AVERAGE   Between:PHREATIC_ZONE.And.SURFACE_WATER  BY_HRU\n'.format(cmnt))   # baseflow

        f.write('{}:CustomOutput MONTHLY AVERAGE   Between:PONDED_WATER.And.VADOSE_ZONE     BY_HRU\n'.format(cmnt))   # infiltration
        f.write('{}:CustomOutput MONTHLY AVERAGE   To:PHREATIC_ZONE                         BY_HRU\n'.format(cmnt))   # recharge

        f.write('{}:CustomOutput MONTHLY AVERAGE   VADOSE_ZONE                              BY_HRU\n'.format(cmnt))   # vadose zone storage
        f.write('{}:CustomOutput MONTHLY AVERAGE   PHREATIC_ZONE                            BY_HRU\n'.format(cmnt))   # phreatic zone storage
        f.write('{}:CustomOutput MONTHLY AVERAGE   QUICK_RUNOFF                             BY_HRU\n'.format(cmnt))   # CONVOLUTION[0] storage
        f.write('{}:CustomOutput MONTHLY AVERAGE   DELAYED_RUNOFF                           BY_HRU\n'.format(cmnt))   # CONVOLUTION[1] storage

        # f.write('{}:CustomOutput MONTHLY CUMULSUM  To:QUICK_RUNOFF   BY_HRU\n'.format(cmnt))   # pervious runoff (infiltration excess)
        # f.write('{}:CustomOutput MONTHLY CUMULSUM  To:DELAYED_RUNOFF BY_HRU\n'.format(cmnt))   # delayed runoff
        # f.write('{}:CustomOutput MONTHLY AVERAGE   To:SURFACE_WATER  BY_HRU\n'.format(cmnt))   # monthly runoff by hru
        # f.write('{}:CustomOutput DAILY   AVERAGE   SNOW              BY_BASIN\n'.format(cmnt)) # daily snowpack by sub-watershed
        # f.write('{}:CustomOutput DAILY   AVERAGE   AET               BY_BASIN\n'.format(cmnt)) # daily evapotranspiration by sub-watershed
        # f.write('{}:CustomOutput DAILY   AVERAGE   SOIL[0]           BY_BASIN\n'.format(cmnt)) # daily soil moisture by sub-watershed
        # f.write('{}:CustomOutput DAILY   AVERAGE   SOIL[1]           BY_BASIN\n'.format(cmnt)) # daily soil moisture by sub-watershed


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