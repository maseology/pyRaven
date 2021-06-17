
from pkg import solris3, surfgeo

class HRU:

    def __init__(self, wshd, lulu, sglu, minf):
        self.hrus = dict() # swsid: (lu,sg): frac
        cc = 0
        for sid,cids in wshd.xr.items():
            d = dict()
            n = 0
            for c in cids:
                n += 1
                ll = solris3.xr(81) # 81	Open Tallgrass Prairie ("ShortVegetation", "ShortVegetation")  # HARD-CODED DEFAULTS
                gg = surfgeo.xr(6)  #  6   "Unknown"
                if c in lulu: ll = lulu[c]
                if c in sglu: gg = sglu[c]                
                t = (ll,gg)
                if t in d: 
                    d[t] += 1 
                else: 
                    d[t] = 1
            
            dd = dict()
            dn = 0.0
            for t,v in d.items():
                if v/n > minf: 
                    dd[t] = v/n
                    dn += v/n
            
            # normalize
            for t,v in dd.items(): dd[t]/=dn
            self.hrus[sid] = dd
            cc += len(dd)

        print(' {} distinct HRUs'.format(cc))