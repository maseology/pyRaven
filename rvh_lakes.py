
import math
from pymmio import files as mmio
from pyRaven.flags import flg

def write(root, nam, desc, builder, ver, wshd, hru, hruid, res):
    def rvh_write(fp,astpl):
        with open(fp,"w") as f:
            f.write('# --------------------------------------------\n')
            f.write('# Raven Lake Definition (.rvh) file\n')
            f.write('# ' + desc + '\n')
            f.write('# written by ' + builder + '\n')
            f.write('# using pyRaven builder\n')
            f.write('# Raven version: ' + ver + '\n')
            f.write('# --------------------------------------------\n\n')

            def writeWeir(t):
                # " the preferred option for natural reservoirs." p.201
                f.write(':Reservoir   Lake-{}  # {}\n'.format(t, wshd.nam[t]))
                f.write('  :SubBasinID          {}\n'.format(t))
                f.write('  :HRUID               {}\n'.format(hruid[t]))
                f.write('  :Type  RESROUTE_STANDARD\n')
                f.write('  :WeirCoefficient      0.6\n')
                if astpl:
                    f.write('  :CrestWidth          xCW{}\n'.format(wshd.nam[t].lower().replace('reservoir','').replace('-','')))
                else:
                    f.write('  :CrestWidth          10.0\n')
                f.write('  :MaxDepth            20.0\n')
                f.write('  :LakeArea            {:.1f}\n'.format(wshd.s[t].km2*1000000))
                # f.write('  :AbsoluteCrestHeight {:.1f}\n'.format(hru.zga[t]))  # Absolute crest height is only really needed when comparing to actual stage measurements (defaults to 0)
                f.write(':EndReservoir\n\n')
            
            if res is not None:
                for t,r in res.items():
                    if not t in hruid: continue # needed when sub-setting model domain
                    if r.rvh is not None:
                        pass
                    elif r.minstage is None:
                        writeWeir(t)
                    else:
                        print('  ** WARNING: auto creation of stage-discharge needs work, consider using simple wier')
                        f.write(':Reservoir   {}\n'.format(r.name))
                        f.write('  :SubBasinID   {}\n'.format(t))
                        f.write('  :HRUID   {}\n'.format(hruid[t])) # needed for evaporation
                        f.write('  :StageRelations\n')
                        mn, a = math.floor(r.minstage)-2, wshd.s[t].km2*1000000
                        n = int(math.ceil(r.maxstage+2)-mn)
                        f.write('    {} # number of points\n'.format(n))
                        f.write('    #stage [m]   Q [m3/s]         V [m3]         A [m2]\n')
                        for i in range(n):
                            v=0
                            if i>0: v=i*a*(i+mn)
                            f.write('{:10.1f}{:15.3f}{:15.1f}{:15.1f}\n'.format(i+mn,0,v,a))
                        f.write('  :EndStageRelations\n')
                        f.write(':EndReservoir\n\n')

            for t,lusg in hru.hrus.items():
                if lusg=='lake':
                    if res is None or not t in res:
                        writeWeir(t)

    rvh_write(root + nam + "-lakes.rvh",False)
    if flg.calibrationmode: rvh_write(mmio.getFileDir(root) +"/" + nam + "-lakes.rvh.tpl",True)