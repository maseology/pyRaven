
from pymmio import files as mmio
from pyRaven.rvp_defaults import luxr, vxr, sgxr, seasonalLAI
from pyRaven.flags import flg

# build Classed Parameter Input file (.rvp) using HMETS conceptualization
# ref: Martel, J., Demeester, K., Brissette, F., Poulin, A., Arsenault, R., 2017. HMETS - a simple and efficient hydrology model for teaching hydrological modelling, flow forecasting and climate change impacts to civil engineering students. International Journal of Engineering Education 34, 1307–1316.
def write(root, nam, desc, builder, ver, hru, par):

    dlu, dveg, dsg = hru.distinctTypes()

    def write_rvp(fp, astpl):
        with open(fp,"w") as f:
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

            """ infiltration.cpp
            else if(type==INF_HMETS)
            {
                double infil,delayed,direct;

                double stor       =state_vars[iTopSoil];
                double max_stor   =pHRU->GetSoilCapacity(0);
                double coef_runoff=pHRU->GetSurfaceProps()->HMETS_runoff_coeff; //[-]

                double sat = min(max(stor/max_stor,0.0),1.0);

                direct=Fimp*rainthru;

                runoff=coef_runoff*(sat)*(1.0-Fimp)*rainthru; //[mm/d] 'horizontal transfer'

                infil=(1.0-Fimp)*rainthru-runoff;

                delayed=coef_runoff*pow(sat,2.0)*infil; //[mm/d]
                infil-=delayed;

                rates[0]=infil;     //PONDED->SOIL[0]
                rates[1]=direct;    //PONDED->SW
                rates[2]=runoff;    //PONDED->CONVOL[0]
                rates[3]=delayed;   //PONDED->CONVOL[1]
            }
            """


            f.write(':LandUseClasses\n')
            f.write(' :Attributes                     IMPERV     VEG_COV\n')
            f.write(' :Units                            frac        frac\n')
            for l in dlu: f.write('  {:25}{:12.2f}{:12.2f}\n'.format(l,luxr[l][0],luxr[l][1]))
            f.write(':EndLandUseClasses\n\n')

            f.write(':VegetationClasses\n')
            f.write(' :Attributes                   MAX_HT   MAX_LAI  MAX_LEAF_COND\n')
            f.write(' :Units                             m      none       mm_per_s\n')        
            for v in dveg: f.write('  {:25}{:10}{:10}{:15}\n'.format(v,vxr[v][0],vxr[v][1],vxr[v][2]))
            f.write(':EndVegetationClasses\n\n')

            f.write(':SoilClasses\n')
            # f.write('  VADOSE\n')
            # f.write('  PHREATIC\n')
            for s in dsg: 
                if s=='LAKE':continue
                if flg.gwzonemode:
                    f.write('  ' + s[0]+str(s[1]) + 'VADOSE\n')
                    f.write('  ' + s[0]+str(s[1]) + 'PHREATIC\n')
                else:
                    f.write('  ' + s + 'VADOSE\n')
                    f.write('  ' + s + 'PHREATIC\n')
            f.write(':EndSoilClasses\n\n')

            f.write('# soil profile definition\n')        
            f.write(':SoilProfiles\n')
            for s in dsg: 
                if s=='LAKE':continue
                ss = s
                if flg.gwzonemode: ss=s[0]+str(s[1])
                if astpl:
                    f.write('  {0:25}{1:5}{0:>26}VADOSE{2:>10}{0:>25}PHREATIC{3:>10}\n'.format(ss,2,'xVadose','xPhreatic'))
                else:
                    f.write('  {0:25}{1:5}{0:>26}VADOSE{2:10.3f}{0:>25}PHREATIC{3:10.3f}\n'.format(ss,2,0.3,0.7))
            f.write('  LAKE                         0\n')
            f.write(':EndSoilProfiles\n\n')


            f.write('\n# -----------------------\n')
            f.write('# parameter specification\n')
            f.write('# -----------------------\n\n')


            f.write('# global parameters:\n')
            f.write('# -----------------------\n')
            if astpl:
                f.write(':GlobalParameter RAINSNOW_TEMP     {}\n'.format('xRAINSNOW_TEMP'))
                if flg.preciponly: f.write(':GlobalParameter RAINSNOW_DELTA    {}\n'.format('xRAINSNOW_DELTA'))
                f.write(':GlobalParameter SNOW_SWI_MIN      {}\n'.format(par.SNOW_SWI_MIN))
                f.write(':GlobalParameter SNOW_SWI_MAX      {}\n'.format(par.SNOW_SWI_MAX))
                f.write(':GlobalParameter SWI_REDUCT_COEFF  {}\n'.format('xSWI_REDUCT_COEFF'))
                f.write(':GlobalParameter SNOW_SWI          {}\n'.format('xSNOW_SWI'))
                f.write(':GlobalParameter AVG_ANNUAL_RUNOFF {} # mm\n'.format(par.AVG_ANNUAL_RUNOFF))
            else:
                f.write(':GlobalParameter RAINSNOW_TEMP     {}\n'.format(par.RAINSNOW_TEMP))
                if flg.preciponly: f.write(':GlobalParameter RAINSNOW_DELTA    {}\n'.format(par.RAINSNOW_DELTA))
                f.write(':GlobalParameter SNOW_SWI_MIN      {}\n'.format(par.SNOW_SWI_MIN))
                f.write(':GlobalParameter SNOW_SWI_MAX      {}\n'.format(par.SNOW_SWI_MAX))
                f.write(':GlobalParameter SWI_REDUCT_COEFF  {}\n'.format(par.SWI_REDUCT_COEFF))
                f.write(':GlobalParameter SNOW_SWI          {}\n'.format(par.SNOW_SWI))
                f.write(':GlobalParameter AVG_ANNUAL_RUNOFF {} # mm\n'.format(par.AVG_ANNUAL_RUNOFF))


            f.write('\n\n# class parameters:\n')
            f.write('# -----------------------\n\n')

            f.write('# snow balance and infiltration parameters (HMETS):\n')
            f.write(':LandUseParameterList\n')
            f.write(' :Parameters         MIN_MELT_FACTOR  MAX_MELT_FACTOR  DD_MELT_TEMP  DD_AGGRADATION  REFREEZE_FACTOR  DD_REFREEZE_TEMP  REFREEZE_EXP  HMETS_RUNOFF_COEFF\n')
            f.write(' :Units                       mm/d/K           mm/d/K             C            1/mm           mm/d/K                 C          none                none\n') 
            # if astpl:
            #     f.write('  [DEFAULT] {:>24}{:>17}{:>14}{:>16}{:>17}{:>18}{:>14}{:>20}\n'.format('xMIN_MELT_FACTOR', 'xMAX_MELT_FACTOR', 'xDD_MELT_TEMP', 'xDD_AGGRADATION', 'xREFREEZE_FACTOR', 'xDD_REFREEZE_TEMP', 'xREFREEZE_EXP', 'xHMETS_RUNOFF_COEFF'))
            # else:
            #     f.write('  [DEFAULT] {:24}{:17}{:14}{:16}{:17}{:18}{:14}{:20}\n'.format(par.MIN_MELT_FACTOR, par.MAX_MELT_FACTOR, par.DD_MELT_TEMP, par.DD_AGGRADATION, par.REFREEZE_FACTOR, par.DD_REFREEZE_TEMP, par.REFREEZE_EXP, par.HMETS_RUNOFF_COEFF))
            if astpl:
                f.write('  [DEFAULT] {:>24}{:>17}{:>14}{:>16}{:>17}{:>18}{:>14}{:>20}\n'.format('xMIN_MELT_FACTOR', 'xMAX_MELT_FACTOR', 'xDD_MELT_TEMP', 'xDD_AGGRADATION', 'xREFREEZE_FACTOR', 'xDD_REFREEZE_TEMP', 'xREFREEZE_EXP', 'xHMETS_RUNOFF_COEFF'))
                for l in dlu: 
                    if l=='Agriculture':
                        f.write('  {:25} _DEFAULT         _DEFAULT      _DEFAULT        _DEFAULT         _DEFAULT          _DEFAULT      _DEFAULT{:>20}\n'.format(l,'xAgRC'))
                    elif l in ['Forest','Meadow','ShortVegetation','TallVegetation','SparseVegetation','DenseVegetation']:
                        f.write('  {:25} _DEFAULT         _DEFAULT      _DEFAULT        _DEFAULT         _DEFAULT          _DEFAULT      _DEFAULT{:>20}\n'.format(l,'xNatRC'))                        
                    elif l in ['Wetland','Swamp','Marsh','Channel','Waterbody','Lake']:
                        f.write('  {:25} _DEFAULT         _DEFAULT      _DEFAULT        _DEFAULT         _DEFAULT          _DEFAULT      _DEFAULT{:>20}\n'.format(l,'xWetRC'))
                    elif l=='noflow':
                        f.write('  {:25} _DEFAULT         _DEFAULT      _DEFAULT        _DEFAULT         _DEFAULT          _DEFAULT      _DEFAULT{:>20}\n'.format(l,0.0))
                    else: # elif l in ['Urban','Barren']:
                        f.write('  {:25} _DEFAULT         _DEFAULT      _DEFAULT        _DEFAULT         _DEFAULT          _DEFAULT      _DEFAULT            _DEFAULT\n'.format(l))
            else:
                f.write('  [DEFAULT] {:24}{:17}{:14}{:16}{:17}{:18}{:14}{:20}\n'.format(par.MIN_MELT_FACTOR, par.MAX_MELT_FACTOR, par.DD_MELT_TEMP, par.DD_AGGRADATION, par.REFREEZE_FACTOR, par.DD_REFREEZE_TEMP, par.REFREEZE_EXP, par.HMETS_RUNOFF_COEFF))
                for l in dlu: f.write('  {:25} _DEFAULT         _DEFAULT      _DEFAULT        _DEFAULT         _DEFAULT          _DEFAULT      _DEFAULT            _DEFAULT\n'.format(l))
            f.write(':EndLandUseParameterList\n\n')

            if astpl:
                f.write('# routing parameters:  xLogGAMMA_SCALE1 xLogGAMMA_SCALE2\n')
            else:
                f.write('# routing parameters:\n')
            f.write(':LandUseParameterList\n')
            f.write(' :Parameters           LAKE_PET_CORR   GAMMA_SHAPE   GAMMA_SCALE  GAMMA_SHAPE2  GAMMA_SCALE2\n')
            f.write(' :Units                         none          none          none          none          none\n')
            if astpl:
                f.write('  [DEFAULT] {:>24}{:>14}{:>14}{:>14}{:>14}\n'.format('xLAKE_PET_CORR' , 'xGAMMA_SHAPE1', 'xGAMMA_SCALE1', 'xGAMMA_SHAPE2', 'xGAMMA_SCALE2')) 
            else:
                f.write('  [DEFAULT] {:24}{:14}{:14}{:14}{:14}\n'.format(par.LAKE_PET_CORR , par.GAMMA_SHAPE, par.GAMMA_SCALE, par.GAMMA_SHAPE2, par.GAMMA_SCALE2)) 
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


            f.write('# groundwater parameters:\n')
            sxgrDay = {x: y/365.24 for x, y in sgxr.items()} # convert from mm/yr to mm/d
            f.write(':SoilParameterList\n')
            f.write(' :Parameters                 POROSITY  PET_CORRECTION   MAX_PERC_RATE  BASEFLOW_COEFF\n')
            f.write(' :Units                          none            mm/d            mm/d             1/d\n')
            if flg.gwzonemode:
                if astpl:
                    f.write('  [DEFAULT]                       1.0{:>16}             1.0 {:>16}\n'.format('xPET_CORRECTION', 'xiflwUnknown'))      
                else:
                    f.write('  [DEFAULT]                       1.0{:16}             1.0 {:16}\n'.format(par.PET_CORRECTION, par.INTERFLOW_COEFF))      
                for s in dsg:
                    if s=='LAKE':continue
                    ss = s[0]+str(s[1])
                    if astpl:
                        stpl = s[0]
                        if stpl[:3]=="Low" and len(stpl)>3: stpl=stpl.replace("Low","L")
                        if stpl[:6]=="Medium" and len(stpl)>6: stpl=stpl.replace("Medium","M")
                        f.write('  {:25}  _DEFAULT        _DEFAULT{:16.3f}     xiflw{}\n'.format(ss + 'VADOSE ',sxgrDay[s[0]],stpl)) 
                        f.write('  {:25}  _DEFAULT             0.0             0.0 {:16}\n'.format(ss + 'PHREATIC', 'xBASEFLOW_COEFF'+str(s[1])))
                    else:
                        f.write('  {:25}  _DEFAULT        _DEFAULT{:16.3f}         _DEFAULT\n'.format(ss + 'VADOSE ',sxgrDay[s[0]])) 
                        f.write('  {:25}  _DEFAULT             0.0             0.0 {:16.3f}\n'.format(ss + 'PHREATIC', par.BASEFLOW_COEFF))
            else:
                if astpl:
                    f.write('  [DEFAULT]                       1.0{:>16}             1.0           0.001\n'.format('xPET_CORRECTION'))
                else:
                    f.write('  [DEFAULT]                       1.0{:16}             1.0{:16}\n'.format(par.PET_CORRECTION, par.BASEFLOW_COEFF))      
                for s in dsg: 
                    if s=='LAKE':continue
                    if astpl:
                        stpl = s
                        if stpl[:3]=="Low" and len(stpl)>3: stpl=stpl.replace("Low","L")
                        if stpl[:6]=="Medium" and len(stpl)>6: stpl=stpl.replace("Medium","M")                
                        f.write('  {:25}  _DEFAULT        _DEFAULT{:16.3f}{:>16}\n'.format(s + 'VADOSE ',sxgrDay[s], 'xinterflow')) 
                        f.write('  {:25}  _DEFAULT             0.0             0.0 {:>15}\n'.format(s + 'PHREATIC', 'xbf'+stpl))
                    else:
                        f.write('  {:25}  _DEFAULT        _DEFAULT{:16.3f}{:16.3f}\n'.format(s + 'VADOSE ',sxgrDay[s], par.INTERFLOW_COEFF)) 
                        f.write('  {:25}  _DEFAULT             0.0             0.0        _DEFAULT\n'.format(s + 'PHREATIC'))
            f.write(':EndSoilParameterList\n\n')

    write_rvp(root + nam + ".rvp", False)
    if flg.calibrationmode: write_rvp(mmio.getFileDir(root) +"/"+ nam + ".rvp.tpl", True)


def writeLumped(root, nam, desc, builder, ver, par):

    def write_rvp(fp, astpl):
        with open(fp,"w") as f:
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
            f.write('  {:25}{:12.2f}{:12.2f}\n'.format('luclass',0.15,0.15))
            f.write(':EndLandUseClasses\n\n')

            f.write(':VegetationClasses\n')
            f.write(' :Attributes                   MAX_HT   MAX_LAI  MAX_LEAF_COND\n')
            f.write(' :Units                             m      none       mm_per_s\n')        
            f.write('  {:25}{:10}{:10}{:15}\n'.format('vegclass',10.,4.,.1))
            f.write(':EndVegetationClasses\n\n')

            f.write(':SoilClasses\n')
            f.write('  VADOSE\n')
            f.write('  PHREATIC\n')
            f.write(':EndSoilClasses\n\n')

            f.write('# soil profile definition\n')        
            f.write(':SoilProfiles\n')
            if astpl:
                f.write('  {0:25}{1:5} VADOSE{2:>10} PHREATIC{3:>10}\n'.format('soilclass',2,'xVadose','xPhreatic'))
            else:
                f.write('  {0:25}{1:5} VADOSE{2:10.3f} PHREATIC{3:10.3f}\n'.format('soilclass',2,0.3,0.7))
            f.write(':EndSoilProfiles\n\n')


            f.write('\n# -----------------------\n')
            f.write('# parameter specification\n')
            f.write('# -----------------------\n\n')


            f.write('# global parameters:\n')
            f.write('# -----------------------\n')
            if astpl:
                f.write(':GlobalParameter RAINSNOW_TEMP     {}\n'.format('xRAINSNOW_TEMP'))
                f.write(':GlobalParameter RAINSNOW_DELTA    {}\n'.format('xRAINSNOW_DELTA'))
                f.write(':GlobalParameter SNOW_SWI_MIN      {}\n'.format(par.SNOW_SWI_MIN))
                f.write(':GlobalParameter SNOW_SWI_MAX      {}\n'.format(par.SNOW_SWI_MAX))
                f.write(':GlobalParameter SWI_REDUCT_COEFF  {}\n'.format('xSWI_REDUCT_COEFF'))
                f.write(':GlobalParameter SNOW_SWI          {}\n'.format('xSNOW_SWI'))
                f.write(':GlobalParameter AVG_ANNUAL_RUNOFF {} # mm\n'.format(par.AVG_ANNUAL_RUNOFF))
            else:
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
            f.write(' :Parameters         MIN_MELT_FACTOR  MAX_MELT_FACTOR  DD_MELT_TEMP  DD_AGGRADATION  REFREEZE_FACTOR  DD_REFREEZE_TEMP  REFREEZE_EXP  HMETS_RUNOFF_COEFF\n')
            f.write(' :Units                       mm/d/K           mm/d/K             C            1/mm           mm/d/K                 C          none                none\n') 
            if astpl:
                f.write('  [DEFAULT] {:>24}{:>17}{:>14}{:>16}{:>17}{:>18}{:>14}{:>20}\n'.format('xMIN_MELT_FACTOR', 'xMAX_MELT_FACTOR', 'xDD_MELT_TEMP', 'xDD_AGGRADATION', 'xREFREEZE_FACTOR', 'xDD_REFREEZE_TEMP', 'xREFREEZE_EXP', 'xHMETS_RUNOFF_COEFF'))
            else:
                f.write('  [DEFAULT] {:24}{:17}{:14}{:16}{:17}{:18}{:14}{:20}\n'.format(par.MIN_MELT_FACTOR, par.MAX_MELT_FACTOR, par.DD_MELT_TEMP, par.DD_AGGRADATION, par.REFREEZE_FACTOR, par.DD_REFREEZE_TEMP, par.REFREEZE_EXP, par.HMETS_RUNOFF_COEFF))
            f.write(':EndLandUseParameterList\n\n')

            if astpl:
                f.write('# routing parameters:  xLogGAMMA_SCALE1 xLogGAMMA_SCALE2\n')
            else:
                f.write('# routing parameters:\n')
            f.write(':LandUseParameterList\n')
            f.write(' :Parameters           LAKE_PET_CORR   GAMMA_SHAPE   GAMMA_SCALE  GAMMA_SHAPE2  GAMMA_SCALE2\n')
            f.write(' :Units                         none          none          none          none          none\n')
            if astpl:
                f.write('  [DEFAULT] {:>24}{:>14}{:>14}{:>14}{:>14}\n'.format('xLAKE_PET_CORR' , 'xGAMMA_SHAPE1', 'xGAMMA_SCALE1', 'xGAMMA_SHAPE2', 'xGAMMA_SCALE2')) 
            else:
                f.write('  [DEFAULT] {:24}{:14}{:14}{:14}{:14}\n'.format(par.LAKE_PET_CORR , par.GAMMA_SHAPE, par.GAMMA_SCALE, par.GAMMA_SHAPE2, par.GAMMA_SCALE2)) 
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


            f.write('# groundwater parameters:\n')
            f.write(':SoilParameterList\n')
            f.write(' :Parameters                 POROSITY  PET_CORRECTION   MAX_PERC_RATE  BASEFLOW_COEFF\n')
            f.write(' :Units                          none            mm/d            mm/d             1/d\n')
            if astpl:
                f.write('  [DEFAULT]                       1.0{:>16}             1.0           0.001\n'.format('xPET_CORRECTION'))
                f.write('  {:25}  _DEFAULT        _DEFAULT{:16.3f}{:>16}\n'.format('VADOSE ','_DEFAULT', 'xinterflow')) 
                f.write('  {:25}  _DEFAULT             0.0             0.0 {:>15}\n'.format('PHREATIC', 'xbf'))                
            else:
                f.write('  [DEFAULT]                       1.0{:16}             1.0{:16}\n'.format(par.PET_CORRECTION, par.BASEFLOW_COEFF)) 
                f.write('  {:25}  _DEFAULT        _DEFAULT        _DEFAULT{:16.3f}\n'.format('VADOSE ', par.INTERFLOW_COEFF)) 
                f.write('  {:25}  _DEFAULT             0.0             0.0        _DEFAULT\n'.format('PHREATIC'))
            f.write(':EndSoilParameterList\n\n')

    write_rvp(root + nam + ".rvp", False)
    if flg.calibrationmode: write_rvp(mmio.getFileDir(root) +"/"+ nam + ".rvp.tpl", True)