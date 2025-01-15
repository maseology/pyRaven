
import os


# append to Time Series Input file (.rvt)
def write(root, nam, hru, res, submdl=False):
    if res is None: return

    indir = 'input'
    if submdl: indir = '..\\'+indir
    if not os.path.exists(root + nam + ".rvt"): print('  **WARNING: appending to .rvt file that does not exist **')

    with open(root + nam + ".rvt","a") as f:
        for k,v in res.items():
            if not k in hru.hrus: continue # needed when sub-setting model domain
            if v.rvh is None:
                f.write('\n# Reservoir {} stage constraints\n'.format(v.name))
                f.write(":ReservoirMaxStage {}\n".format(k))
                f.write("  :AnnualCycle   {}\n".format(' '.join('{:.2f}'.format(x) for x in v.maxbound)))
                f.write(":EndReservoirMaxStage\n")
                f.write(":ReservoirMinStage {}\n".format(k))
                f.write("  :AnnualCycle   {}\n".format(' '.join('{:.2f}'.format(x) for x in v.minbound)))
                f.write(":EndReservoirMinStage\n")
                if v.rule is not None:
                    f.write(":ReservoirTargetStage {}\n".format(k))
                    f.write("  :AnnualCycle   {}\n".format(' '.join('{:.2f}'.format(x) for x in v.rule)))
                    f.write(":EndReservoirTargetStage\n")