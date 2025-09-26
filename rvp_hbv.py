
from pymmio import files as mmio
from pyRaven.rvp_defaults import luxr, vxr, sgxr, seasonalLAI
from pyRaven.flags import flg

# build Classed Parameter Input file (.rvp) using HBV conceptualization
def write(root, nam, desc, builder, ver, wshd, hru, par):

    dlu, dveg, dsg = hru.distinctTypes()

    def write_rvp(fp, astpl):
        with open(fp,"w") as f:
            f.write('# --------------------------------------------\n')
            f.write('# Raven classed parameter file (.rvp)\n')
            # f.write('# HEC-like semi-distributed watershed model\n')
            f.write('# ' + desc + '\n')        
            f.write('# written by ' + builder + '\n')
            f.write('# using pyRaven builder\n')
            f.write('# Raven version: ' + ver + '\n')
            f.write('# --------------------------------------------\n\n')


            f.write('\n# -----------------\n')
            f.write('# class definitions\n')
            f.write('# -----------------\n')

            f.write(':LandUseClasses\n')
            # luxr = {'TallVegetation': (0.,1.), 
            #     'ShortVegetation': (0.,.1), 
            #     'DenseVegetation': (0.,1.), 
            #     'Forest': (0.,1.), 
            #     'Agriculture': (0.,1.), 
            #     'Waterbody': (0.,0.), 
            #     'Urban': (.85,0.), 
            #     'Swamp': (0.,.85),
            #     'Marsh': (0.,.25),  
            #     'Wetland': (0.,.25),  
            #     'Barren': (0.,0.),               
            #     'noflow': (0.,0.),
            #     'LAKE': (0.,0.)}
            f.write(' :Attributes                     IMPERV     VEG_COV\n')
            f.write(' :Units                            frac        frac\n')
            if astpl:
                for l in dlu:
                    if l=='Agriculture':
                        f.write('  {:25}    xAgImprv{:12.2f}\n'.format(l,luxr[l][1]))
                    else:                        
                        f.write('  {:25}{:12.2f}{:12.2f}\n'.format(l,luxr[l][0],luxr[l][1]))
            else:
                # f.write('  LU_ALL    {:12}{:12}\n'.format(0.0,0.0))
                for l in dlu: f.write('  {:25}{:12.2f}{:12.2f}\n'.format(l,luxr[l][0],luxr[l][1]))
            f.write(':EndLandUseClasses\n\n')

            f.write(':VegetationClasses\n')
            # vxr = {'Coniferous': (3.,4.5,5.), 
            #     'Deciduous': (3.,4.5,5.), 
            #     'MixedVegetation': (3.,4.5,5.), 
            #     'Shrub': (1,2.5,5.), 
            #     'ShortVegetation': (.5,4.5,5.),
            #     'Bare': (0.,0.,.0001),
            #     'LAKE': (0.,0.,0.)}
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
            f.write('  ' + 'TOP\n')
            for s in dsg: 
                if s=='LAKE':continue
                if flg.gwzonemode:
                    # f.write('  ' + s[0]+str(s[1]) + 'TOP\n')
                    f.write('  ' + s[0]+str(s[1]) + '\n') #'FAST\n')
                    # f.write('  ' + s[0]+str(s[1]) + 'SLOW\n')
                else:
                    # f.write('  ' + s + 'TOP\n')
                    f.write('  ' + s + '\n') #'FAST\n')
                    # f.write('  ' + s + 'SLOW\n')
            if len(wshd.zon)>0:
                grps = [int(i) for i in list(set(wshd.zon.values()))]
                grps.sort()
                for g in grps: f.write('  ' + 'SLOW{0:03d}\n'.format(g))
            else:
                f.write('  ' + 'SLOW\n')
            f.write(':EndSoilClasses\n\n')

            f.write('# soil profile definition (horizon depths in metres)\n')
            f.write('#  Note: in HBV only the top layer requires a capacity, both the fast and slow reservoirs have a semi-infinite domain)\n')        
            f.write(':SoilProfiles\n')
            # f.write('  DEFAULT_P,    3,    TOP, 0.075, FAST, 0.1,  SLOW, 5.0\n')
            if len(wshd.zon)>0:
                grps = [int(i) for i in list(set(wshd.zon.values()))]
                grps.sort()
                for g in grps:
                    for s in dsg:
                        if s=='LAKE':continue
                        ss = s
                        if flg.gwzonemode: ss=s[0]+str(s[1])
                        if astpl:
                            # f.write('  {0:25}{1:5}{0:>26}TOP{2:>10}{0:>25}FAST{3:>10}{0:>25}SLOW{4:>10}\n'.format(ss,3,'xTop','xFast','xSlow'))
                            f.write('  {0:25}{1:5}   TOP{2:>10}{5:>25}{3:>10}        SLOW{6:03d}{4:>10}\n'.format(ss+'{:03d}'.format(g),3,'xTop',1.,1.,ss,g))
                        else:
                            # f.write('  {0:25}{1:5}{0:>26}TOP{2:>10}{0:>25}FAST{3:>10}{0:>25}SLOW{4:>10}\n'.format(ss,3,0.075,0.1,5.))
                            f.write('  {0:25}{1:5}   TOP{2:>10}{5:>25}{3:>10}        SLOW{6:03d}{4:>10}\n'.format(ss+'{:03d}'.format(g),3,0.075,1.,1.,ss,g))                    
            else:
                for s in dsg: 
                    if s=='LAKE':continue
                    ss = s
                    if flg.gwzonemode: ss=s[0]+str(s[1])
                    if astpl:
                        # f.write('  {0:25}{1:5}{0:>26}TOP{2:>10}{0:>25}FAST{3:>10}{0:>25}SLOW{4:>10}\n'.format(ss,3,'xTop','xFast','xSlow'))
                        f.write('  {0:25}{1:5}   TOP{2:>10}{0:>25}FAST{3:>10}{0:>25}SLOW{4:>10}\n'.format(ss,3,'xTop',1.,1.))
                    else:
                        # f.write('  {0:25}{1:5}{0:>26}TOP{2:>10}{0:>25}FAST{3:>10}{0:>25}SLOW{4:>10}\n'.format(ss,3,0.075,0.1,5.0))
                        f.write('  {0:25}{1:5}   TOP{2:>10}{0:>25}FAST{3:>10}{0:>25}SLOW{4:>10}\n'.format(ss,3,0.075,1.,1.))
            f.write('  LAKE                         0\n')
            f.write(':EndSoilProfiles\n\n')


            f.write('\n# -----------------------\n')
            f.write('# parameter specification\n')
            f.write('# -----------------------\n')


            f.write('# global parameters:\n')
            f.write('# -----------------------\n')
            if astpl:
                f.write(':GlobalParameter RAINSNOW_TEMP     {}\n'.format('xRAINSNOW_TEMP'))
                if flg.preciponly: f.write(':GlobalParameter RAINSNOW_DELTA    {}\n'.format('xRAINSNOW_DELTA'))
                f.write(':GlobalParameter SNOW_SWI          {}\n'.format('xSNOW_SWI'))
                f.write(':GlobalParameter AVG_ANNUAL_RUNOFF {} # mm\n'.format(par.AVG_ANNUAL_RUNOFF))
            else:
                f.write(':GlobalParameter RAINSNOW_TEMP     {}\n'.format(par.RAINSNOW_TEMP))
                if flg.preciponly: f.write(':GlobalParameter RAINSNOW_DELTA    {}\n'.format(par.RAINSNOW_DELTA))
                f.write(':GlobalParameter SNOW_SWI          {}\n'.format(par.SNOW_SWI))
                f.write(':GlobalParameter AVG_ANNUAL_RUNOFF {}\n'.format(par.AVG_ANNUAL_RUNOFF))
                # :GlobalParameter AIRSNOW_COEFF   0.75 #(1-x6)
                # :GlobalParameter AVG_ANNUAL_SNOW 123.3 #x5 mm
                # :GlobalParameter PRECIP_LAPSE    0.4
                # :GlobalParameter ADIABATIC_LAPSE 6.5


            f.write('\n\n# class parameters:\n')
            f.write('# -----------------------\n\n')

            f.write('# snowmelt and lake PET parameters:\n')
            f.write(':LandUseParameterList\n')
            f.write(' :Parameters           LAKE_PET_CORR  MELT_FACTOR  REFREEZE_FACTOR\n')
            f.write(' :Units                         none       mm/d/K           mm/d/K\n') 
            if astpl:
                f.write('  [DEFAULT] {:>24} {:>12} {:>16}\n'.format('xLAKE_PET_CORR', 'xMELT_FACTOR', 'xREFREEZE_FACTOR'))
                # for l in dlu: f.write('  {:25} _DEFAULT     _DEFAULT         _DEFAULT\n'.format(l))
            else:
                f.write('  [DEFAULT] {:24} {:12} {:16}\n'.format(par.LAKE_PET_CORR, par.MELT_FACTOR, par.REFREEZE_FACTOR))
                # for l in dlu: f.write('  {:25} _DEFAULT     _DEFAULT         _DEFAULT\n'.format(l))
                # # for l in dlu: 
                # #     if l == 'Urban':
                # #         f.write('  {:25} _DEFAULT          3.5              0.5\n'.format(l))
                # #     else:
                # #         f.write('  {:25} _DEFAULT     _DEFAULT         _DEFAULT\n'.format(l))
                # # # f.write(' :Parameters             MELT_FACTOR  MIN_MELT_FACTOR  HBV_MELT_FOR_CORR  REFREEZE_FACTOR  HBV_MELT_ASP_CORR\n')
                # # # f.write(' :Units                       mm/d/K          mm/d/K                none           mm/d/K               none\n') 
                # # # f.write('  [DEFAULT]                   3.1339          1.3036                 1.0              1.0            0.65836\n')
                # # # # f.write('  LU_ALL                _DEFAULT            _DEFAULT              0.6805            _DEFAULT            _DEFAULT\n')
                # # # for l in dlu: 
                # # #     if l == 'Urban':
                # # #         f.write('  {:25}      3.5             1.3                 1.0              0.5           _DEFAULT\n'.format(l))
                # # #     else:
                # # #         f.write('  {:25} _DEFAULT        _DEFAULT            _DEFAULT         _DEFAULT           _DEFAULT\n'.format(l))
 
            f.write(':EndLandUseParameterList\n\n')


            f.write('# interception parameters:\n')
            f.write(':VegetationParameterList\n')
            # f.write(' :Parameters            RAIN_ICEPT_PCT  SNOW_ICEPT_PCT\n') # if using PRECIP_ICEPT_USER
            # f.write(' :Units                           none            none\n')
            # f.write('  [DEFAULT]                        0.0             0.0\n')
            f.write(' :Parameters          RAIN_ICEPT_FACT  SNOW_ICEPT_FACT  MAX_CAPACITY  MAX_SNOW_CAPACITY\n') # if using PRECIP_ICEPT_LAI
            f.write(' :Units                          none             none          none               none\n')
            if astpl:
                f.write('  [DEFAULT] {:>25}{:>17}{:>14}{:>19}\n'.format('xRAIN_ICEPT_FACT', 'xSNOW_ICEPT_FACT','xMAX_CAPACITY', 'xMAX_SNOW_CAPACITY'))   
            else:
                f.write('  [DEFAULT] {:25}{:17}{:14}{:19}\n'.format(par.RAIN_ICEPT_FACT, par.SNOW_ICEPT_FACT,par.MAX_CAPACITY, par.MAX_SNOW_CAPACITY))   
            # for v in dveg: 
            #     if v == 'Bare':
            #         f.write('  {:25}       0.0              0.0\n'.format(v))
            #     else:
            #         f.write('  {:25}  _DEFAULT         _DEFAULT\n'.format(v))
            f.write(':EndVegetationParameterList\n\n')

            f.write(':SeasonalCanopyLAI\n')
            for v in dveg: f.write(seasonalLAI(v))            
            f.write(':EndSeasonalCanopyLAI\n\n')               
            # f.write(':VegetationParameterList\n')
            # f.write(' :Parameters            SAI_HT_RATIO  MAX_CAPACITY  MAX_SNOW_CAPACITY  RAIN_ICEPT_FACT  SNOW_ICEPT_FACT  RAIN_ICEPT_PCT  SNOW_ICEPT_PCT\n')
            # f.write(' :Units                         none            mm                 mm             none             none            none            none\n')
            # f.write('  [DEFAULT]                      0.0           5.0                5.0             0.05             0.05            0.05            0.05\n')
            # # f.write('  VEG_ALL               0.0      16.2593            6.6763            0.05            0.05           0.05           0.05\n')
            # for v in dveg: 
            #     if v == 'Bare':
            #         f.write('  {:25}      0.0           0.0                0.0              0.0              0.0             0.0             0.0\n'.format(v))
            #     else:
            #         f.write('  {:25} _DEFAULT      _DEFAULT           _DEFAULT         _DEFAULT         _DEFAULT        _DEFAULT        _DEFAULT\n'.format(v))
            # f.write(':EndVegetationParameterList\n\n')

            # f.write(':SeasonalCanopyLAI\n')
            # # f.write('  VEG_ALL    0.0  0.0  0.0  0.0  1.0  2.0  4.0  4.0  3.0  2.0  0.0  0.0\n')
            # for v in dveg: f.write(seasonalLAI(v))
            # f.write(':EndSeasonalCanopyLAI\n\n')        


            f.write('# soilzone parameters:\n') # (Note: MAX_PERC_RATE is further affected by a global multiplier in the .rvh file)\n')
            # sgxr = {'Low': 50., 
            #     'LowMedium': 150., 
            #     'Medium': 500.,
            #     'MediumHigh': 1500.,
            #     'High': 5000.,
            #     'WetlandSediments': 100.,  
            #     'Streambed': 1000.,               
            #     'Unknown': 500.}            
            sxgrDay = {x: y/365.24 for x, y in sgxr.items()} # convert from mm/yr to mm/d
            f.write(':SoilParameterList\n')
            # HBV parameters:
            #   BETA: HBV_BETA
            #     FC: <soillayerthickness> * POROSITY  "maximum soil moisture storage"
            #     LP: FIELD_CAPACITY (when SAT_WILT=0)
            #     K0: BASEFLOW_COEFF2
            #    LUZ: STORAGE_THRESHOLD
            #  K1/K2: BASEFLOW_COEFF
            #   xtra: BASE_THRESH_N   MAX_BASEFLOW_RATE   BASEFLOW_THRESH   
            f.write(' :Parameters                PET_CORRECTION  POROSITY  HBV_BETA  FIELD_CAPACITY  SAT_WILT  MAX_CAP_RISE_RATE  MAX_PERC_RATE  STORAGE_THRESHOLD     BASEFLOW_COEFF2      BASEFLOW_COEFF  BASEFLOW_N\n')
            f.write(' :Units                               none      none      none            none      none               mm/d           mm/d                 mm                 1/d                 1/d        none\n')
            if flg.gwzonemode:
                print(" \n\n\n ******  WARNING TODO: rvp_hbv.py (flg.gwzonemode)  ****** \n\n\n")
                pass
            else:
                if astpl:
                    f.write('  [DEFAULT]               {:>16}       1.0{:>10}{:>16}       0.0{:>19}            0.0{:>19}{:20.3f}{:20.3f}{:>12}\n'.format('xPET_CORRECTION','xHBV_BETA','xFIELD_CAPACITY','xMAX_CAP_RISE_RATE','xSTORAGE_THRESHOLD',par.INTERFLOW_COEFF,par.INTERFLOW_COEFF,'xBASEFLOW_N'))
                    f.write('  TOP                             _DEFAULT  _DEFAULT  _DEFAULT        _DEFAULT  _DEFAULT           _DEFAULT       _DEFAULT           _DEFAULT            _DEFAULT            _DEFAULT    _DEFAULT\n') 
                    for s in dsg: 
                        if s=='LAKE':continue
                        stpl = s
                        if stpl[:3]=="Low" and len(stpl)>3: stpl=stpl.replace("Low","L")
                        if stpl[:6]=="Medium" and len(stpl)>6: stpl=stpl.replace("Medium","M")
                        f.write('  {0:25}       _DEFAULT  _DEFAULT  _DEFAULT        _DEFAULT  _DEFAULT           _DEFAULT{1:15.3f}           _DEFAULT{2:>20}{2:>20}    _DEFAULT\n'.format(s,sxgrDay[s],'xk'+stpl))                    
                    if len(wshd.zon)>0:
                        grps = [int(i) for i in list(set(wshd.zon.values()))]
                        grps.sort()
                        for g in grps:
                            f.write('  {:25}       _DEFAULT  _DEFAULT  _DEFAULT        _DEFAULT  _DEFAULT           _DEFAULT       _DEFAULT           _DEFAULT            _DEFAULT{:>20}    _DEFAULT\n'.format('SLOW'+'{:03d}'.format(g),'xbf'+'{:03d}'.format(g)))
                    else:
                        for s in dsg: 
                            if s=='LAKE':continue
                            # stpl = s
                            # if stpl[:3]=="Low" and len(stpl)>3: stpl=stpl.replace("Low","L")
                            # if stpl[:6]=="Medium" and len(stpl)>6: stpl=stpl.replace("Medium","M")
                            # f.write('  {:25}       _DEFAULT  _DEFAULT  _DEFAULT        _DEFAULT  _DEFAULT           _DEFAULT       _DEFAULT            _DEFAULT    _DEFAULT\n'.format(s + 'TOP '))
                            f.write('  {:25}       _DEFAULT  _DEFAULT  _DEFAULT        _DEFAULT  _DEFAULT           _DEFAULT{:15.3f}            _DEFAULT    _DEFAULT    _DEFAULT    _DEFAULT\n'.format(s,sxgrDay[s]))
                            # f.write('  {:25}       _DEFAULT  _DEFAULT  _DEFAULT        _DEFAULT  _DEFAULT           _DEFAULT       _DEFAULT{:>20}    _DEFAULT\n'.format(s + 'SLOW','xbf'+stpl))
                        f.write('  {:25}       _DEFAULT  _DEFAULT  _DEFAULT        _DEFAULT  _DEFAULT           _DEFAULT       _DEFAULT{:>20}    _DEFAULT    _DEFAULT    _DEFAULT\n'.format('SLOW','xbflw'))
                else:
                    f.write('  [DEFAULT]               {:>16}{:>10}{:>10}{:>16}{:>10}{:>19}{:>15}{:>19}{:20.3f}{:20.3f}{:12.3f}\n'.format(par.PET_CORRECTION,1.0,par.HBV_BETA,par.FIELD_CAPACITY,0.0,par.MAX_CAP_RISE_RATE,0.0,par.STORAGE_THRESHOLD,par.INTERFLOW_COEFF,par.INTERFLOW_COEFF,par.BASEFLOW_N))

                    # f.write('  FAST             _DEFAULT      0.43244       _DEFAULT            0.0       _DEFAULT          _DEFAULT          1.446       0.034432         1.9631\n')
                    # f.write('  SLOW             _DEFAULT     _DEFAULT       _DEFAULT            0.0       _DEFAULT          _DEFAULT       _DEFAULT       0.044002            1.0\n')
                    # f.write('  TOP              _DEFAULT     _DEFAULT       _DEFAULT            0.0       _DEFAULT          _DEFAULT            0.0       _DEFAULT       _DEFAULT\n')
                    f.write('  TOP                             _DEFAULT  _DEFAULT  _DEFAULT        _DEFAULT  _DEFAULT           _DEFAULT       _DEFAULT           _DEFAULT            _DEFAULT            _DEFAULT    _DEFAULT\n') 
                    for s in dsg: 
                        if s=='LAKE':continue
                        # f.write('  {:25}       _DEFAULT  _DEFAULT  _DEFAULT        _DEFAULT  _DEFAULT           _DEFAULT       _DEFAULT            _DEFAULT    _DEFAULT\n'.format(s + 'TOP ')) 
                        f.write('  {:25}       _DEFAULT  _DEFAULT  _DEFAULT        _DEFAULT  _DEFAULT           _DEFAULT{:15.3f}           _DEFAULT            _DEFAULT            _DEFAULT    _DEFAULT\n'.format(s,sxgrDay[s])) 
                        # f.write('  {:25}       _DEFAULT  _DEFAULT  _DEFAULT        _DEFAULT  _DEFAULT           _DEFAULT       _DEFAULT{:20.3f}    _DEFAULT\n'.format(s + 'SLOW',par.BASEFLOW_COEFF))        
                    if len(wshd.zon)>0:
                        grps = [int(i) for i in list(set(wshd.zon.values()))]
                        grps.sort()
                        for g in grps: 
                            f.write('  {:25}       _DEFAULT  _DEFAULT  _DEFAULT        _DEFAULT  _DEFAULT           _DEFAULT       _DEFAULT           _DEFAULT            _DEFAULT{:20.3f}    _DEFAULT\n'.format('SLOW'+'{:03d}'.format(g),par.BASEFLOW_COEFF))
                    else:
                        f.write('  {:25}       _DEFAULT  _DEFAULT  _DEFAULT        _DEFAULT  _DEFAULT           _DEFAULT       _DEFAULT           _DEFAULT            _DEFAULT{:20.3f}    _DEFAULT\n'.format('SLOW',par.BASEFLOW_COEFF))
                f.write(':EndSoilParameterList\n\n')

    write_rvp(root + nam + ".rvp", False)
    if flg.calibrationmode: write_rvp(mmio.getFileDir(root) +"/"+ nam + ".rvp.tpl", True)



def writeLumped(root, nam, desc, builder, ver, par):

    def write_rvp(fp, astpl):
        with open(fp,"w") as f:
            f.write('# --------------------------------------------\n')
            f.write('# Raven classed parameter file (.rvp)\n')
            # f.write('# HEC-like semi-distributed watershed model\n')
            f.write('# ' + desc + '\n')        
            f.write('# written by ' + builder + '\n')
            f.write('# using pyRaven builder\n')
            f.write('# Raven version: ' + ver + '\n')
            f.write('# --------------------------------------------\n\n')


            f.write('\n# -----------------\n')
            f.write('# class definitions\n')
            f.write('# -----------------\n')

            f.write(':LandUseClasses\n')
            f.write(' :Attributes                     IMPERM  FOREST_COV\n')
            f.write(' :Units                            frac        frac\n')
            f.write('  {:25}{:12.2f}{:12.2f}\n'.format('luclass',0.15,0.15))
            f.write(':EndLandUseClasses\n\n')

            f.write(':VegetationClasses\n')
            f.write(' :Attributes                   MAX_HT   MAX_LAI  MAX_LEAF_COND\n')
            f.write(' :Units                             m      none       mm_per_s\n')        
            f.write('  {:25}{:10}{:10}{:15}\n'.format('vegclass',10.,4.,.1))
            f.write(':EndVegetationClasses\n\n')

            f.write(':SoilClasses\n')
            f.write('  TOP\n')
            f.write('  FAST\n')
            f.write('  SLOW\n')
            f.write(':EndSoilClasses\n\n')

            f.write('# soil profile definition (horizon depths in metres)\n')        
            f.write(':SoilProfiles\n')
            if astpl:
                f.write('  {0:15}{1:5}  TOP{2:>10}  FAST{3:>10}  SLOW{4:>10}\n'.format('soilclass',3,'xTop',1.,1.))
            else:
                f.write('  {0:15}{1:5}  TOP{2:>10}  FAST{3:>10}  SLOW{4:>10}\n'.format('soilclass',3,0.075,1.,1.))
            f.write(':EndSoilProfiles\n\n')


            f.write('\n# -----------------------\n')
            f.write('# parameter specification\n')
            f.write('# -----------------------\n')


            f.write('# global parameters:\n')
            f.write('# -----------------------\n')
            if astpl:
                f.write(':GlobalParameter RAINSNOW_TEMP     {}\n'.format('xRAINSNOW_TEMP'))
                if flg.preciponly: f.write(':GlobalParameter RAINSNOW_DELTA    {}\n'.format('xRAINSNOW_DELTA'))
                f.write(':GlobalParameter SNOW_SWI          {}\n'.format('xSNOW_SWI'))
                f.write(':GlobalParameter AVG_ANNUAL_RUNOFF {} # mm\n'.format(par.AVG_ANNUAL_RUNOFF))
            else:
                f.write(':GlobalParameter RAINSNOW_TEMP     {}\n'.format(par.RAINSNOW_TEMP))
                if flg.preciponly: f.write(':GlobalParameter RAINSNOW_DELTA    {}\n'.format(par.RAINSNOW_DELTA))
                f.write(':GlobalParameter SNOW_SWI          {}\n'.format(par.SNOW_SWI))
                f.write(':GlobalParameter AVG_ANNUAL_RUNOFF {}\n'.format(par.AVG_ANNUAL_RUNOFF))
                # :GlobalParameter AIRSNOW_COEFF   0.75 #(1-x6)
                # :GlobalParameter AVG_ANNUAL_SNOW 123.3 #x5 mm
                # :GlobalParameter PRECIP_LAPSE    0.4
                # :GlobalParameter ADIABATIC_LAPSE 6.5


            f.write('\n# land use parameters:\n')
            f.write(':LandUseParameterList\n')
            f.write(' :Parameters           LAKE_PET_CORR  MELT_FACTOR  REFREEZE_FACTOR\n')
            f.write(' :Units                         none       mm/d/K           mm/d/K\n') 
            if astpl:
                f.write('  [DEFAULT] {:>24} {:>12} {:>16}\n'.format('xLAKE_PET_CORR', 'xMELT_FACTOR', 'xREFREEZE_FACTOR'))
            else:
                f.write('  [DEFAULT] {:24} {:12} {:16}\n'.format(par.LAKE_PET_CORR, par.MELT_FACTOR, par.REFREEZE_FACTOR))
            f.write(':EndLandUseParameterList\n\n')


            f.write('# interception parameters:\n')
            f.write(':VegetationParameterList\n')
            # f.write(' :Parameters            RAIN_ICEPT_PCT  SNOW_ICEPT_PCT\n') # if using PRECIP_ICEPT_USER
            # f.write(' :Units                           none            none\n')
            # f.write('  [DEFAULT]                        0.0             0.0\n')
            f.write(' :Parameters          RAIN_ICEPT_FACT  SNOW_ICEPT_FACT  MAX_CAPACITY  MAX_SNOW_CAPACITY\n') # if using PRECIP_ICEPT_LAI
            f.write(' :Units                          none             none          none               none\n')
            if astpl:
                f.write('  [DEFAULT] {:>25}{:>17}{:>14}{:>19}\n'.format('xRAIN_ICEPT_FACT', 'xSNOW_ICEPT_FACT','xMAX_CAPACITY', 'xMAX_SNOW_CAPACITY'))   
            else:
                f.write('  [DEFAULT] {:25}{:17}{:14}{:19}\n'.format(par.RAIN_ICEPT_FACT, par.SNOW_ICEPT_FACT,par.MAX_CAPACITY, par.MAX_SNOW_CAPACITY))   
            # for v in dveg: 
            #     if v == 'Bare':
            #         f.write('  {:25}       0.0              0.0\n'.format(v))
            #     else:
            #         f.write('  {:25}  _DEFAULT         _DEFAULT\n'.format(v))
            f.write(':EndVegetationParameterList\n\n')

            f.write(':SeasonalCanopyLAI\n')
            f.write('  {:25}  0.0  0.0  0.0  0.0  1.0  2.0  4.5  4.5  3.0  2.0  0.0  0.0\n'.format('vegclass'))          
            f.write(':EndSeasonalCanopyLAI\n\n')        


            f.write('# soilzone parameters:\n')
            f.write(':SoilParameterList\n')
            # HBV parameters:
            #   BETA: HBV_BETA
            #     FC: <soillayerthickness> * POROSITY  "maximum soil moisture storage"
            #     LP: FIELD_CAPACITY (when SAT_WILT=0)
            #     K0: BASEFLOW_COEFF2
            #    LUZ: STORAGE_THRESHOLD
            #  K1/K2: BASEFLOW_COEFF
            #   xtra: BASE_THRESH_N
            f.write(' :Parameters                PET_CORRECTION  POROSITY  HBV_BETA  FIELD_CAPACITY  SAT_WILT  MAX_CAP_RISE_RATE  MAX_PERC_RATE      BASEFLOW_COEFF  BASEFLOW_N\n') #  BASEFLOW_COEFF2  STORAGE_THRESHOLD\n') # for BASE_THRESH_STOR
            f.write(' :Units                               none      none      none            none      none               mm/d           mm/d                 1/d        none\n') #              1/d                  m\n')
            if astpl:
                f.write('  [DEFAULT]               {:>16}       1.0{:>10}{:>16}       0.0{:>19}            0.0{:>20}{:>12}\n'.format('xPET_CORRECTION','xHBV_BETA','xFIELD_CAPACITY','xMAX_CAP_RISE_RATE','xinterflow','xBASEFLOW_N'))
                f.write('  {:25}       _DEFAULT  _DEFAULT  _DEFAULT        _DEFAULT  _DEFAULT           _DEFAULT       _DEFAULT            _DEFAULT    _DEFAULT\n'.format('TOP ')) 
                f.write('  {:25}       _DEFAULT  _DEFAULT  _DEFAULT        _DEFAULT  _DEFAULT           _DEFAULT{:15.3f}            _DEFAULT    _DEFAULT\n'.format('FAST', 'xinterflow')) 
                f.write('  {:25}       _DEFAULT  _DEFAULT  _DEFAULT        _DEFAULT  _DEFAULT           _DEFAULT       _DEFAULT{:>20}    _DEFAULT\n'.format('SLOW','xbf'))
            else:
                f.write('  [DEFAULT]               {:>16}{:>10}{:>10}{:>16}{:>10}{:>19}{:>15}{:20.3f}{:>12}\n'.format(par.PET_CORRECTION,1.0,par.HBV_BETA,par.FIELD_CAPACITY,0.0,par.MAX_CAP_RISE_RATE,0.0,par.INTERFLOW_COEFF,par.BASEFLOW_N))
                f.write('  {:25}       _DEFAULT  _DEFAULT  _DEFAULT        _DEFAULT  _DEFAULT           _DEFAULT       _DEFAULT            _DEFAULT    _DEFAULT\n'.format('TOP ')) 
                f.write('  {:25}       _DEFAULT  _DEFAULT  _DEFAULT        _DEFAULT  _DEFAULT           _DEFAULT{:15.3f}            _DEFAULT    _DEFAULT\n'.format('FAST',par.INTERFLOW_COEFF)) 
                f.write('  {:25}       _DEFAULT  _DEFAULT  _DEFAULT        _DEFAULT  _DEFAULT           _DEFAULT       _DEFAULT{:20.3f}    _DEFAULT\n'.format('SLOW',par.BASEFLOW_COEFF))        
            f.write(':EndSoilParameterList\n\n')

    write_rvp(root + nam + ".rvp", False)
    if flg.calibrationmode: write_rvp(mmio.getFileDir(root) +"/"+ nam + ".rvp.tpl", True)
