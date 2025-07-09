
from pyRaven import rvc_Res

# build Initial Conditions Input file (.rvc)
def write(root, nam, desc, builder, ver, hru, res):
    with open(root + nam + ".rvc","w") as f:
        f.write('# --------------------------------------------\n')
        f.write('# initial conditions (.rvc) file\n')
        f.write('# ' + desc + '\n')
        f.write('# written by ' + builder + '\n')
        f.write('# using pyRaven builder\n')
        f.write('# Raven version: ' + ver + '\n')
        f.write('# --------------------------------------------\n\n')
        f.write('# initial conditions\n')   

        if hru is None:
            f.write(':UniformInitialConditions SOIL[0] {:>10.3f}\n'.format(5.))
            f.write(':UniformInitialConditions SOIL[1] {:>10.3f}\n'.format(70.))
        else:
            f.write(':HRUStateVariableTable\n')
            f.write('  :Attributes SOIL[0] SOIL[1]\n')
            f.write('  :Units mm mm\n')
            f.write('   LandHRUs {:10.3}{:10.3}\n'.format(5.,70.))
            f.write('   LakeHRUs        0.0       0.0\n')
            f.write(':EndHRUStateVariableTable\n')

    if hru is not None: rvc_Res.write(root, nam, hru, res)