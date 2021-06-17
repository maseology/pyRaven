

# build Classed Parameter Input file (.rvp)
def write(root, nam, desc, builder, ver):

    with open(root + nam + ".rvp","w") as f:
        f.write('# --------------------------------------------\n')
        f.write('# Raven classed parameter file (.rvp)\n')
        f.write('# ' + desc + '\n')        
        f.write('# written by ' + builder + '\n')
        f.write('# using pyRaven builder\n')
        f.write('# Raven version: ' + ver + '\n')
        f.write('# --------------------------------------------\n\n')


        f.write('\n# -----------------------\n')
        f.write('# parameter specification\n')
        f.write('# -----------------------\n')


        f.write('# global parameters:\n')
        f.write(':GlobalParameter RAINSNOW_TEMP     0.0\n')
        f.write(':GlobalParameter RAINSNOW_DELTA    1.1559\n')
        f.write(':GlobalParameter SNOW_SWI          0.05\n')
        f.write(':GlobalParameter AVG_ANNUAL_RUNOFF 350 # mm\n')
        # :GlobalParameter AIRSNOW_COEFF   0.75 #(1-x6)
        # :GlobalParameter AVG_ANNUAL_SNOW 123.3 #x5 mm
        # :GlobalParameter PRECIP_LAPSE    0.4
        # :GlobalParameter ADIABATIC_LAPSE 6.5


        f.write('\n# class parameters:\n')


        f.write(':LandUseParameterList\n')
        f.write(' :Parameters             MELT_FACTOR  MIN_MELT_FACTOR  HBV_MELT_FOR_CORR  REFREEZE_FACTOR  HBV_MELT_ASP_CORR\n')
        f.write(' :Units                       mm/d/K          mm/d/K                none           mm/d/K               none\n') 
        f.write('  [DEFAULT]                   3.1339          1.3036                 1.0              1.0            0.65836\n')
        f.write(':EndLandUseParameterList\n\n')


        f.write(':VegetationParameterList\n')
        f.write(' :Parameters            SAI_HT_RATIO  MAX_CAPACITY  MAX_SNOW_CAPACITY  RAIN_ICEPT_FACT  SNOW_ICEPT_FACT  RAIN_ICEPT_PCT  SNOW_ICEPT_PCT\n')
        f.write(' :Units                         none            mm                 mm             none             none            none            none\n')
        f.write('  [DEFAULT]                      0.0           5.0                5.0             0.05             0.05            0.05            0.05\n')
        f.write(':EndVegetationParameterList\n\n')
