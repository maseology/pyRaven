

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
        f.write(':GlobalParameter SNOW_SWI          0.05\n')


        f.write('\n# class parameters:\n')


        f.write(':LandUseParameterList\n')
        f.write(' :Parameters             MELT_FACTOR  REFREEZE_FACTOR\n')
        f.write(' :Units                       mm/d/K           mm/d/K\n') 
        f.write('  [DEFAULT]                   3.1339              1.0\n')
        f.write(':EndLandUseParameterList\n\n')
