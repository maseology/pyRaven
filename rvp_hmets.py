
from pyRaven.rvp_defaults import luxr, vxr, sgxr, seasonalLAI

# build Classed Parameter Input file (.rvp)
def write(root, nam, desc, builder, ver, hru, par):

    # collect distinct IDs
    dlu = set()
    dsg = set()
    dveg = set()
    for _,vv in hru.hrus.items():
        if vv=='lake':
            dlu.add('LAKE')
            dveg.add('LAKE')
            dsg.add('LAKE')
        else:
            for v in vv:
                dlu.add(v[0][0])
                dveg.add(v[0][1])
                dsg.add(v[1])

    with open(root + nam + ".rvp","w") as f:
        f.write('# --------------------------------------------\n')
        f.write('# Raven classed parameter file (.rvp)\n')
        f.write('# ' + desc + '\n')        
        f.write('# written by ' + builder + '\n')
        f.write('# using pyRaven builder\n')
        f.write('# Raven version: ' + ver + '\n')
        f.write('# --------------------------------------------\n\n')


        f.write('\n# -----------------\n')
        f.write('# class definitions\n')
        f.write('# -----------------\n\n')

        f.write(':LandUseClasses\n')
        f.write(' :Attributes                     IMPERM  FOREST_COV\n')
        f.write(' :Units                            frac        frac\n')
        for l in dlu: f.write('  {:25}{:12.2f}{:12.2f}\n'.format(l,luxr[l][0],luxr[l][1]))
        f.write(':EndLandUseClasses\n\n')

        f.write(':VegetationClasses\n')
        f.write(' :Attributes                   MAX_HT   MAX_LAI  MAX_LEAF_COND\n')
        f.write(' :Units                             m      none       mm_per_s\n')        
        for v in dveg: f.write('  {:25}{:10}{:10}{:15}\n'.format(v,vxr[v][0],vxr[v][1],vxr[v][2]))
        f.write(':EndVegetationClasses\n\n')

        f.write(':SoilClasses\n')
        # f.write('  TOPSOIL\n')
        # f.write('  PHREATIC\n')
        for s in dsg: 
            if s=='LAKE':continue
            f.write('  ' + s + 'TOPSOIL\n')
            f.write('  ' + s + 'PHREATIC\n')
        f.write(':EndSoilClasses\n\n')


        f.write('# soil profile definition\n')        
        f.write(':SoilProfiles\n')
        for s in dsg: 
            if s=='LAKE':continue
            f.write('  {0:25}{1:5}{0:>26}TOPSOIL{2:10.3f}{0:>25}PHREATIC{3:10.3f}\n'.format(s,2,0.3,0.7))
        f.write('  LAKE                         0\n')
        f.write(':EndSoilProfiles\n\n')



        f.write('\n# -----------------------\n')
        f.write('# parameter specification\n')
        f.write('# -----------------------\n\n')


        f.write('# global parameters:\n')
        f.write('# -----------------------\n')
        f.write(':GlobalParameter RAINSNOW_TEMP     {}\n'.format(par.RAINSNOW_TEMP))
        f.write(':GlobalParameter RAINSNOW_DELTA    {}\n'.format(par.RAINSNOW_DELTA))
        f.write(':GlobalParameter SNOW_SWI_MIN      {}\n'.format(par.SNOW_SWI_MIN))
        f.write(':GlobalParameter SNOW_SWI_MAX      {}\n'.format(par.SNOW_SWI_MAX))
        f.write(':GlobalParameter SWI_REDUCT_COEFF  {}\n'.format(par.SWI_REDUCT_COEFF))
        f.write(':GlobalParameter SNOW_SWI          {}\n'.format(par.SNOW_SWI))
        f.write(':GlobalParameter AVG_ANNUAL_RUNOFF {} # mm\n'.format(par.AVG_ANNUAL_RUNOFF))


        f.write('\n\n# class parameters:\n')
        f.write('# -----------------------\n\n')

        f.write('# snow balance and infiltration parameters (HMETS):\n')
        f.write(':LandUseParameterList\n')
        f.write(' :Parameters         MIN_MELT_FACTOR  MAX_MELT_FACTOR  DD_MELT_TEMP  DD_AGGRADATION  REFREEZE_FACTOR  REFREEZE_EXP  DD_REFREEZE_TEMP  HMETS_RUNOFF_COEFF\n')
        f.write(' :Units                       mm/d/K           mm/d/K             C            1/mm           mm/d/K          none                 C                none\n') 
        f.write('  [DEFAULT] {:24}{:17}{:14}{:16}{:17}{:14}{:18}{:20}\n'.format(par.MIN_MELT_FACTOR, par.MAX_MELT_FACTOR, par.DD_MELT_TEMP, par.DD_AGGRADATION, par.REFREEZE_FACTOR, par.REFREEZE_EXP, par.DD_REFREEZE_TEMP, par.HMETS_RUNOFF_COEFF))
        f.write(':EndLandUseParameterList\n\n')


        f.write('# routing parameters:\n')
        f.write(':LandUseParameterList\n')
        f.write(' :Parameters           LAKE_PET_CORR  GAMMA_SHAPE  GAMMA_SCALE  GAMMA_SHAPE2  GAMMA_SCALE2\n')
        f.write(' :Units                         none         none         none          none          none\n') 
        f.write('  [DEFAULT] {:24}{:13}{:13}{:14}{:14}\n'.format(par.LAKE_PET_CORR , par.GAMMA_SHAPE, par.GAMMA_SCALE, par.GAMMA_SHAPE2, par.GAMMA_SCALE2)) 
        f.write(':EndLandUseParameterList\n\n')


        f.write('# interception parameters:\n')
        f.write(':VegetationParameterList\n')
        # f.write(' :Parameters            RAIN_ICEPT_PCT  SNOW_ICEPT_PCT\n') # if using PRECIP_ICEPT_USER
        # f.write(' :Units                           none            none\n')
        # f.write('  [DEFAULT]                        0.0             0.0\n')
        f.write(' :Parameters          RAIN_ICEPT_FACT  SNOW_ICEPT_FACT\n') # if using PRECIP_ICEPT_LAI
        f.write(' :Units                          none             none\n')
        f.write('  [DEFAULT] {:25}{:17}\n'.format(par.RAIN_ICEPT_FACT, par.SNOW_ICEPT_FACT))   
        # for v in dveg: 
        #     if v == 'Bare':
        #         f.write('  {:25}       0.0              0.0\n'.format(v))
        #     else:
        #         f.write('  {:25}  _DEFAULT         _DEFAULT\n'.format(v))
        f.write(':EndVegetationParameterList\n\n')

        f.write(':SeasonalCanopyLAI\n')
        for v in dveg: f.write(seasonalLAI(v))            
        f.write(':EndSeasonalCanopyLAI\n\n')     


        f.write('# groundwater parameters:\n')
        sgxr.update((x, y/365.24) for x, y in sgxr.items()) # convert from mm/yr to mm/d
        f.write(':SoilParameterList\n')
        f.write(' :Parameters                 POROSITY  PET_CORRECTION   MAX_PERC_RATE  BASEFLOW_COEFF\n')
        f.write(' :Units                          none            mm/d            mm/d             1/d\n')
        f.write('  [DEFAULT]                       1.0             1.0             1.0{:16.3f}\n'.format(par.BASEFLOW_COEFF))      
        for s in dsg: 
            if s=='LAKE':continue
            f.write('  {:25}  _DEFAULT        _DEFAULT{:16.3f}{:16.3f}\n'.format(s + 'TOPSOIL ',sgxr[s], par.interflow_COEFF)) 
            f.write('  {:25}  _DEFAULT             0.0             0.0        _DEFAULT\n'.format(s + 'PHREATIC'))
        f.write(':EndSoilParameterList\n\n')