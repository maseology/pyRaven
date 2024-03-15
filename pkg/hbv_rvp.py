

# build Classed Parameter Input file (.rvp)
def write(root, nam, desc, builder, ver, hrus):

    # collect distinct IDs
    dlu = set()
    dsg = set()
    dveg = set()
    for _,vv in hrus.items():
        for v in vv:
            dlu.add(v[0][0])
            dveg.add(v[0][1])
            dsg.add(v[1])

    with open(root + nam + ".rvp","w") as f:
        f.write('# --------------------------------------------\n')
        f.write('# Raven classed parameter file (.rvp)\n')
        # f.write('# HEC-EC semi-distributed watershed model\n')
        f.write('# ' + desc + '\n')        
        f.write('# written by ' + builder + '\n')
        f.write('# using pyRaven builder\n')
        f.write('# Raven version: ' + ver + '\n')
        f.write('# --------------------------------------------\n\n')


        f.write('\n# -----------------\n')
        f.write('# class definitions\n')
        f.write('# -----------------\n')

        f.write(':LandUseClasses\n')
        luxr = {'TallVegetation': (0.,1.), 
            'ShortVegetation': (0.,.1), 
            'DenseVegetation': (0.,1.), 
            'Forest': (0.,1.), 
            'Agriculture': (0.,1.), 
            'Waterbody': (0.,0.), 
            'Urban': (.85,0.), 
            'Swamp': (0.,.85),
            'Marsh': (0.,.25),  
            'Wetland': (0.,.25),  
            'Barren': (0.,0.),               
            'noflow': (0.,0.)}
        f.write(' :Attributes                     IMPERM  FOREST_COV\n')
        f.write(' :Units                            frac        frac\n')
        # f.write('  LU_ALL    {:12}{:12}\n'.format(0.0,0.0))
        for l in dlu: f.write('  {:25}{:12.2f}{:12.2f}\n'.format(l,luxr[l][0],luxr[l][1]))
        f.write(':EndLandUseClasses\n\n')

        f.write(':VegetationClasses\n')
        vxr = {'Coniferous': (3.,4.5,5.), 
            'Deciduous': (3.,4.5,5.), 
            'MixedVegetation': (3.,4.5,5.), 
            'Shrub': (1,2.5,5.), 
            'ShortVegetation': (.5,4.5,5.),
            'Bare': (0.,0.,.0001)}
        f.write(' :Attributes                   MAX_HT   MAX_LAI  MAX_LEAF_COND\n')
        f.write(' :Units                             m      none       mm_per_s\n')        
        # f.write('  VEG_ALL  {:10}{:10}{:14}\n'.format(3.0,4.5,5.0))
        for v in dveg: f.write('  {:25}{:10}{:10}{:15}\n'.format(v,vxr[v][0],vxr[v][1],vxr[v][2]))
        f.write(':EndVegetationClasses\n\n')

        # :TerrainClasses
        #  :Attributes , HILLSLOPE_LENGTH, DRAINAGE_DENSITY
        #  :Units , m, km/km2
        #  {terrain_class_name, HILLSLOPE_LENGTH, DRAINAGE_DENSITY}x[NTC]
        # :EndTerrainClasses

        f.write(':SoilClasses\n')
        # f.write(' :Attributes     %SAND     %CLAY     %SILT  %ORGANIC\n')
        # f.write(' :Units           none      none      none      none\n')
        # f.write('  TOP       {:10}{:10}{:10}{:10}\n'.format(.8,.2,0.0,0.0))
        # f.write('  FAST      {:10}{:10}{:10}{:10}\n'.format(.8,.2,0.0,0.0))
        # f.write('  SLOW      {:10}{:10}{:10}{:10}\n'.format(.8,.2,0.0,0.0))   
        for s in dsg: 
                f.write('  ' + s + 'TOP\n')
                f.write('  ' + s + 'FAST\n')
                f.write('  ' + s + 'SLOW\n')
        f.write(':EndSoilClasses\n\n')

        f.write('# soil profile definition\n')        
        f.write(':SoilProfiles\n')
        # f.write('  DEFAULT_P,    3,    TOP, 0.075, FAST, 0.1,  SLOW, 5.0\n')
        for s in dsg: f.write('  {0:25}{1:5}{0:>26}TOP{2:10.3f}{0:>25}FAST{3:10.3f}{0:>25}SLOW{4:10.3f}\n'.format(s,3,0.075,0.1,5.0))
        f.write('  LAKE                         0\n')
        f.write(':EndSoilProfiles\n\n')



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
        # f.write('  LU_ALL                _DEFAULT            _DEFAULT              0.6805            _DEFAULT            _DEFAULT\n')
        for l in dlu: 
            if l == 'Urban':
                f.write('  {:25}      3.5             1.3                 1.0              0.5           _DEFAULT\n'.format(l))
            else:
                f.write('  {:25} _DEFAULT        _DEFAULT            _DEFAULT         _DEFAULT           _DEFAULT\n'.format(l))
        f.write(':EndLandUseParameterList\n\n')


        f.write(':VegetationParameterList\n')
        f.write(' :Parameters            SAI_HT_RATIO  MAX_CAPACITY  MAX_SNOW_CAPACITY  RAIN_ICEPT_FACT  SNOW_ICEPT_FACT  RAIN_ICEPT_PCT  SNOW_ICEPT_PCT\n')
        f.write(' :Units                         none            mm                 mm             none             none            none            none\n')
        f.write('  [DEFAULT]                      0.0           5.0                5.0             0.05             0.05            0.05            0.05\n')
        # f.write('  VEG_ALL               0.0      16.2593            6.6763            0.05            0.05           0.05           0.05\n')
        for v in dveg: 
            if v == 'Bare':
                f.write('  {:25}      0.0           0.0                0.0              0.0              0.0             0.0             0.0\n'.format(v))
            else:
                f.write('  {:25} _DEFAULT      _DEFAULT           _DEFAULT         _DEFAULT         _DEFAULT        _DEFAULT        _DEFAULT\n'.format(v))
        f.write(':EndVegetationParameterList\n\n')

        f.write(':SeasonalCanopyLAI\n')
        # f.write('  VEG_ALL    0.0  0.0  0.0  0.0  1.0  2.0  4.0  4.0  3.0  2.0  0.0  0.0\n')
        for v in dveg:
            if v == 'Bare':
                f.write('  {:25}  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0\n'.format(v))
            elif v == 'Coniferous':
                f.write('  {:25}  4.0  4.0  4.0  4.0  4.0  4.0  4.0  4.0  4.0  4.0  4.0  4.0\n'.format(v))
            elif v == 'MixedVegetation':
                f.write('  {:25}  2.0  2.0  2.0  2.0  2.0  3.0  4.0  4.0  4.0  3.0  2.0  2.0\n'.format(v))                
            else:
                f.write('  {:25}  0.0  0.0  0.0  0.0  1.0  2.0  4.0  4.0  3.0  2.0  0.0  0.0\n'.format(v))
        f.write(':EndSeasonalCanopyLAI\n\n')        


        f.write(':SoilParameterList\n')
        sgxr = {'Low': 50., 
            'LowMedium': 150., 
            'Medium': 500.,
            'MediumHigh': 1500.,
            'High': 5000.,
            'WetlandSediments': 100.,  
            'Streambed': 1000.,               
            'Unknown': 500.}
        sgxr.update((x, y/365.24) for x, y in sgxr.items())
        # HBV parameters:
        #   BETA: HBV_BETA
        #     FC: <soillayerthickness> * POROSITY  "maximum soil moisture storage"
        #     LP: FIELD_CAPACITY (when SAT_WILT=0)
        #     K0: BASEFLOW_COEFF2
        #    LUZ: STORAGE_THRESHOLD
        #  K1/K2: BASEFLOW_COEFF
        #   xtra: BASE_THRESH_N    
        f.write(' :Parameters                POROSITY  FIELD_CAPACITY       SAT_WILT       HBV_BETA  MAX_CAP_RISE_RATE  MAX_PERC_RATE  BASEFLOW_COEFF2  STORAGE_THRESHOLD  BASEFLOW_COEFF     BASEFLOW_N\n')
        f.write(' :Units                         none            none           none           none               mm/d           mm/d              1/d                  m             1/d           none\n')
        f.write('  [DEFAULT]                  0.49732         0.11777            0.0        0.57569                0.0            0.0             0.03              0.085            0.05            1.0\n')
        # f.write('  FAST              0.43244       _DEFAULT            0.0       _DEFAULT          _DEFAULT          1.446       0.034432         1.9631\n')
        # f.write('  SLOW             _DEFAULT       _DEFAULT            0.0       _DEFAULT          _DEFAULT       _DEFAULT       0.044002            1.0\n')
        # f.write('  TOP              _DEFAULT       _DEFAULT            0.0       _DEFAULT          _DEFAULT            0.0       _DEFAULT       _DEFAULT\n')        
        for s in dsg: 
            f.write('  {:25} _DEFAULT        _DEFAULT       _DEFAULT          _DEFAULT        _DEFAULT       _DEFAULT         _DEFAULT           _DEFAULT        _DEFAULT       _DEFAULT\n'.format(s + 'TOP ')) 
            f.write('  {:25} _DEFAULT        _DEFAULT       _DEFAULT          _DEFAULT          1.1216{:15.3f}         _DEFAULT           _DEFAULT        0.034432         1.9631\n'.format(s + 'FAST',sgxr[s])) 
            f.write('  {:25} _DEFAULT        _DEFAULT       _DEFAULT          _DEFAULT        _DEFAULT       _DEFAULT         _DEFAULT           _DEFAULT        0.044002       _DEFAULT\n'.format(s + 'SLOW'))        
        f.write(':EndSoilParameterList\n\n')



        f.write('\n# -------------------\n')
        f.write('# channel profile(s):\n')
        f.write('# -------------------\n')

        f.write(':ChannelProfile default_trap\n')
        f.write(' :Bedslope 0.001\n')
        f.write(' :SurveyPoints\n')
        f.write('     0  5\n')
        f.write('    55  0\n')
        f.write('    65  0\n')
        f.write('   120  5\n')
        f.write(' :EndSurveyPoints\n')
        f.write(' :RoughnessZones\n')
        f.write('     0  0.035\n')
        f.write(' :EndRoughnessZones\n')
        f.write(':EndChannelProfile\n\n')  