
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
            f.write('  SOIL_PROD\n')
            f.write('  SOIL_ROUT\n')
            f.write('  SOIL_TEMP\n')
            f.write('  SOIL_GW\n')
            f.write(':EndSoilClasses\n\n')

            f.write('# soil profile definition (horizon depths in metres)\n')        
            f.write(':SoilProfiles\n')
            if astpl:
                f.write('  {0:15}{1:5}  SOIL_PROD{2:>10}  SOIL_ROUT{3:>10}  SOIL_TEMP{4:>10}  SOIL_GW{5:>10}\n'.format('soilclass',4,'x1',.3,1.,1.))
            else:
                f.write('  {0:15}{1:5}  SOIL_PROD{2:>10}  SOIL_ROUT{3:>10}  SOIL_TEMP{4:>10}  SOIL_GW{5:>10}\n'.format('soilclass',4,.5,.3,1.,1.))
            f.write(':EndSoilProfiles\n\n')


            f.write(':VegetationClasses\n')
            f.write(' :Attributes                   MAX_HT   MAX_LAI  MAX_LEAF_COND\n')
            f.write(' :Units                             m      none       mm_per_s\n')        
            f.write('  {:25}{:10}{:10}{:15}\n'.format('vegclass',0.,0.,0.))
            f.write(':EndVegetationClasses\n\n')


            f.write(':LandUseClasses\n')
            f.write(' :Attributes                     IMPERM  FOREST_COV\n')
            f.write(' :Units                            frac        frac\n')
            f.write('  {:25}{:12.2f}{:12.2f}\n'.format('luclass',0.,0.))
            f.write(':EndLandUseClasses\n\n')



            f.write('\n# global parameters:\n')
            f.write('# -----------------------\n')
            # if astpl:
            #     f.write(':GlobalParameter RAINSNOW_TEMP     {}\n'.format('xRAINSNOW_TEMP'))
            #     if flg.preciponly: f.write(':GlobalParameter RAINSNOW_DELTA    {}\n'.format('xRAINSNOW_DELTA'))
            #     f.write(':GlobalParameter SNOW_SWI          {}\n'.format('xSNOW_SWI'))
            #     f.write(':GlobalParameter AVG_ANNUAL_RUNOFF {} # mm\n'.format(par.AVG_ANNUAL_RUNOFF))
            # else:
            #     f.write(':GlobalParameter RAINSNOW_TEMP     {}\n'.format(par.RAINSNOW_TEMP))
            #     if flg.preciponly: f.write(':GlobalParameter RAINSNOW_DELTA    {}\n'.format(par.RAINSNOW_DELTA))
            #     f.write(':GlobalParameter SNOW_SWI          {}\n'.format(par.SNOW_SWI))
            #     f.write(':GlobalParameter AVG_ANNUAL_RUNOFF {}\n'.format(par.AVG_ANNUAL_RUNOFF))
            #     # :GlobalParameter AIRSNOW_COEFF   0.75 #(1-x6)
            #     # :GlobalParameter AVG_ANNUAL_SNOW 123.3 #x5 mm
            #     # :GlobalParameter PRECIP_LAPSE    0.4
            #     # :GlobalParameter ADIABATIC_LAPSE 6.5
            if flg.precipactive: f.write(':GlobalParameter RAINSNOW_TEMP     -100\n')

            f.write('\n# soil zone parameters:\n')
            f.write(':SoilParameterList\n')
            f.write(' :Parameters           POROSITY      GR4J_X2      GR4J_X3\n')
            f.write(' :Units                    none         mm/d           mm\n') 
            if astpl:
                f.write('  [DEFAULT]                 1.0 {:>12} {:>12}\n'.format('x2','x3'))
            else:
                f.write('  [DEFAULT]                 1.0 {:12} {:12}\n'.format(-3.3,300.))
            f.write(':EndSoilParameterList\n\n')


            f.write('\n# land use parameters:\n')
            f.write(':LandUseParameterList\n')
            f.write(' :Parameters           GR4J_X4  MELT_FACTOR\n')
            f.write(' :Units                      d       mm/d/K\n') 
            if astpl:
                f.write('  [DEFAULT] {:>18} {:12}\n'.format('x4', par.MELT_FACTOR))
            else:
                f.write('  [DEFAULT] {:18} {:12}\n'.format(1., par.MELT_FACTOR))
            f.write(':EndLandUseParameterList\n\n')


    write_rvp(root + nam + ".rvp", False)
    if flg.calibrationmode: write_rvp(mmio.getFileDir(root) +"/"+ nam + ".rvp.tpl", True)
