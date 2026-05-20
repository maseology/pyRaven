
from pymmio import files as mmio
from pyRaven.flags import flg

def write(root, nam, desc, builder, ver, par):

    def write_rvp(fp, astpl):
        with open(fp,"w") as f:
            f.write('# --------------------------------------------\n')
            f.write('# Raven classed parameter file (.rvp)\n')
            f.write('# ' + desc + '\n')        
            f.write('# written by ' + builder + '\n')
            f.write('# using pyRaven builder\n')
            f.write('# Raven version: ' + ver + '\n')
            f.write('# --------------------------------------------\n\n')


            f.write('# class definitions:\n')
            f.write('# -----------------------\n')

            f.write(':SoilClasses\n')
            f.write('  TOPSOIL\n')
            f.write('  SUBSOIL\n')
            f.write('  PHREATIC\n')
            f.write(':EndSoilClasses\n\n')

            f.write('# soil profile definition (horizon depths in metres)\n')        
            f.write(':SoilProfiles\n')
            if astpl:
                f.write('  {0:15}{1:5}  TOPSOIL{2:>10}  SUBSOIL{3:>10}  PHREATIC{4:>11}\n'.format('soilclass',3,'xZtopsoil','xZsubsoil','xZphreatic'))
            else:
                f.write('  {0:15}{1:5}  TOPSOIL{2:>10}  SUBSOIL{3:>10}  PHREATIC{4:>11}\n'.format('soilclass',3,.1,.3,1.))
            f.write(':EndSoilProfiles\n\n')

            f.write(':VegetationClasses\n')
            f.write(' :Attributes                   MAX_HT   MAX_LAI  MAX_LEAF_COND\n') #  RAIN_ICEPT_PCT  SNOW_ICEPT_PCT\n')
            f.write(' :Units                             m      none       mm_per_s\n') #            none            none\n')        
            f.write('  {:25}{:10}{:10}{:15}\n'.format('vegclass',0.,0.,0.)) #,0.,0.)) {:16}{:16}
            f.write(':EndVegetationClasses\n\n')

            f.write(':LandUseClasses\n')
            f.write(' :Attributes                     IMPERM  FOREST_COV\n')
            f.write(' :Units                            frac        frac\n')
            f.write('  {:25}{:12.2f}{:12.2f}\n'.format('luclass',0.,0.))
            f.write(':EndLandUseClasses\n\n')

            f.write(':TerrainClasses\n')
            f.write(' :Attributes                 HILLSLOPE_LENGTH  DRAINAGE_DENSITY  TOPMODEL_LAMBDA\n')
            f.write(' :Units                                     m            km/km2             none\n')
            if astpl:
                f.write('  {:25}{:18}{:18}{:>17}\n'.format('terclass',1.,1.,'xTOPMODEL_LAMBDA'))                
            else:
                f.write('  {:25}{:18}{:18}{:17}\n'.format('terclass',1.,1.,1.))
            f.write(':EndTerrainClasses\n\n')


            f.write('\n# global parameters:\n')
            f.write('# -----------------------\n')
            if flg.precipactive: f.write(':GlobalParameter RAINSNOW_TEMP     -100\n')


            f.write('\n# soil zone parameters:\n')
            f.write(':SoilParameterList\n')
            f.write(' :Parameters           POROSITY  FIELD_CAPACITY   SAT_WILT  BASEFLOW_COEFF  BASEFLOW_N  HBV_BETA  MAX_BASEFLOW_RATE  PERC_COEFF  VIC_B_EXP\n')
            f.write(' :Units                    none            none       none             1/d        none      none               mm/d         1/d       none\n')
            if astpl:
                f.write('  [DEFAULT]                 1.0{:>16}{:>11}{:>16}{:>12}{:>10}{:>19}{:>12}{:>11}\n'.format('xFC','xWilt','xBASEFLOW_COEFF','xBASEFLOW_N','xHBV_BETA','xMAX_BASEFLOW_RATE','xPERC_COEFF','xVIC_B_EXP'))
            else:
                f.write('  [DEFAULT]                 1.0{:16}{:11}{:16}{:12}{:10}{:19}{:12}{:11}\n'.format(.3,.05,.1,1.,.1,.6,.1,.01))
            f.write(':EndSoilParameterList\n\n')


            f.write('\n# land use parameters:\n')
            f.write(':LandUseParameterList\n')
            f.write(' :Parameters    GAMMA_SCALE  GAMMA_SCALE2   GAMMA_SHAPE  GAMMA_SHAPE2  HMETS_RUNOFF_COEFF  MELT_FACTOR\n')
            f.write(' :Units                 1/d           1/d          none          none                none       mm/d/K\n') 
            if astpl:
                f.write('  [DEFAULT] {:>15}{:>14}{:>14}{:>14}{:>20}{:>13}\n'.format('xGAMMA_SCALE','xGAMMA_SCAL2','xGAMMA_SHAPE','xGAMMA_SHAP2','xHMETS_RUNOFF_COEFF', par.MELT_FACTOR))
            else:
                f.write('  [DEFAULT] {:15}{:14}{:14}{:14}{:20}{:13}\n'.format(.1,.1,.5,.5,.3, par.MELT_FACTOR))
            f.write(':EndLandUseParameterList\n\n')


    write_rvp(root + nam + ".rvp", False)
    if flg.calibrationmode: write_rvp(mmio.getFileDir(root) +"/"+ nam + ".rvp.tpl", True)
