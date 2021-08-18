

# build Classed Parameter Input file (.rvp)
def write(root, nam, desc, builder, ver):

    with open(root + nam + ".rvp","w") as f:
        f.write('# --------------------------------------------\n')
        f.write('# Raven classed parameter file (.rvp)\n')
        f.write('# Single-layered bare soil\n')
        f.write('# ' + desc + '\n')        
        f.write('# written by ' + builder + '\n')
        f.write('# using pyRaven builder\n')
        f.write('# Raven version: ' + ver + '\n')
        f.write('# --------------------------------------------\n\n')

        f.write('\n# -----------------\n')
        f.write('# class definitions\n')
        f.write('# -----------------\n')

        f.write(':SoilClasses\n')
        # f.write(' :Attributes     %SAND     %CLAY     %SILT  %ORGANIC\n')
        # f.write(' :Units           none      none      none      none\n')
        # f.write('  TOP       {:10}{:10}{:10}{:10}\n'.format(.8,.2,0.0,0.0))
        # f.write('  FAST      {:10}{:10}{:10}{:10}\n'.format(.8,.2,0.0,0.0))
        # f.write('  SLOW      {:10}{:10}{:10}{:10}\n'.format(.8,.2,0.0,0.0)) 
        f.write('  SOIL_ALL\n')
        f.write(':EndSoilClasses\n\n')

        f.write('# soil profile definition\n')        
        f.write(':SoilProfiles\n')
        # f.write(' :Attributes              N_HORIZONS  SOIL_CLASS_NAME     THICK\n')
        # f.write(' :Units                         none             none         m\n')
        f.write(' #Attributes              N_HORIZONS  SOIL_CLASS_NAME     THICK\n') 
        f.write('  DEFAULT_P                        1         SOIL_ALL       0.3\n')
        f.write(':EndSoilProfiles\n\n')

        f.write(':LandUseClasses\n')
        f.write(' :Attributes                  IMPERM       FOREST_COV\n')
        f.write(' :Units                         frac             frac\n') 
        f.write('  LU_ALL                         0.0              0.0\n')
        f.write(':EndLandUseClasses\n\n')   
   
        f.write(':VegetationClasses\n')   
        f.write(' :Attributes                  MAX_HT          MAX_LAI  MAX_LEAF_COND\n')
        f.write(' :Units                            m             none       mm_per_s\n')
        f.write('  VEG_ALL                        0.0              0.0            0.0\n')
        # f.write(' :Parameters            SAI_HT_RATIO  MAX_CAPACITY  MAX_SNOW_CAPACITY  RAIN_ICEPT_FACT  SNOW_ICEPT_FACT  RAIN_ICEPT_PCT  SNOW_ICEPT_PCT\n')
        # f.write(' :Units                         none            mm                 mm             none             none            none            none\n')
        # f.write('  [DEFAULT]                      0.0           5.0                5.0             0.05             0.05            0.05            0.05\n')
        f.write(':EndVegetationClasses\n\n')



        f.write('\n# -----------------------\n')
        f.write('# parameter specification\n')
        f.write('# -----------------------\n')

        f.write('# global parameters:\n')
        f.write(':GlobalParameter SNOW_SWI                0.05\n')
        f.write(':GlobalParameter AVG_ANNUAL_RUNOFF      350.0\n')

        f.write('\n# class parameters:\n')
        f.write(':SoilParameterList\n')
        f.write(' :Parameters                POROSITY\n')
        f.write(' :Units                         none\n')
        f.write('  SOIL_ALL                      0.35\n')        
        # f.write(' :Parameters                POROSITY  FIELD_CAPACITY       SAT_WILT       HBV_BETA  MAX_CAP_RISE_RATE  MAX_PERC_RATE  BASEFLOW_COEFF2  STORAGE_THRESHOLD  BASEFLOW_COEFF     BASEFLOW_N\n')
        # f.write(' :Units                         none            none           none           none               mm/d           mm/d              1/d                  m             1/d           none\n')
        # f.write('  [DEFAULT]                  0.49732         0.11777            0.0        0.57569                0.0            0.0             0.03              0.085            0.05            1.0\n')
        f.write(':EndSoilParameterList\n\n')

        f.write(':LandUseParameterList\n')
        f.write(' :Parameters             MELT_FACTOR  REFREEZE_FACTOR\n')
        f.write(' :Units                       mm/d/K           mm/d/K\n') 
        f.write('  LU_ALL                      3.1339              1.0\n')
        f.write(':EndLandUseParameterList\n\n')