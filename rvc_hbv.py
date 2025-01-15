
from pyRaven import rvc_Res

# build Initial Conditions Input file (.rvc)
def write(root, nam, desc, builder, ver, hru, res):
    with open(root + nam + ".rvc","w") as f:
        f.write('# --------------------------------------------\n')
        f.write('# initial conditions (.rvc) file\n')
        # f.write('# HBV-like semi-distributed watershed model\n')
        f.write('# ' + desc + '\n')
        f.write('# written by ' + builder + '\n')
        f.write('# using pyRaven builder\n')
        f.write('# Raven version: ' + ver + '\n')
        f.write('# --------------------------------------------\n\n')
        f.write('# initial conditions\n')   

        f.write(':UniformInitialConditions SOIL[0] {:>10.3f}\n'.format(.1))
        f.write(':UniformInitialConditions SOIL[1] {:>10.3f}\n'.format(.1))
        f.write(':UniformInitialConditions SOIL[2] {:>10.3f}\n'.format(.1))

    rvc_Res.write(root, nam, hru, res)