

def write(root, nam, desc, builder, ver, wshd, hrus, hruid):

    with open(root + nam + "-lakes.rvh","w") as f:
        f.write('# --------------------------------------------\n')
        f.write('# Raven Lake Definition (.rvh) file\n')
        f.write('# ' + desc + '\n')
        f.write('# written by ' + builder + '\n')
        f.write('# using pyRaven builder\n')
        f.write('# Raven version: ' + ver + '\n')
        f.write('# --------------------------------------------\n\n')

        for t,lusg in hrus.items():
            if lusg=='lake':
                # f.write('####\n')
                f.write(':Reservoir   Lake-{}\n'.format(t))
                f.write('  :SubBasinID   {}\n'.format(t))
                f.write('  :HRUID   {}\n'.format(hruid[t]))
                f.write('  :Type RESROUTE_STANDARD\n')
                f.write('  :WeirCoefficient   0.6\n')
                f.write('  :CrestWidth   10.0\n')
                f.write('  :MaxDepth   20.0\n')
                f.write('  :LakeArea   {:10.1f}\n'.format(wshd.s[t].km2*1000000))
                f.write(':EndReservoir\n\n')

