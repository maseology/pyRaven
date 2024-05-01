
from pkg import solris3, surfgeo_OGS

class HRU:

    def __init__(self, wshd, lulu, sglu, minf, lakf):
        self.hrus = dict() # swsid: (lu,sg): frac
        cc = 0
        for sid,cids in wshd.xr.items():
            d = dict()
            n, nlak, nwl = 0, 0, 0
            for c in cids:
                n += 1
                
                # HARD-CODED DEFAULTS
                ll = solris3.xr(81)     # 81	Open Tallgrass Prairie ("ShortVegetation", "ShortVegetation")
                gg = surfgeo_OGS.xr(6)  #  6   "Unknown"

                if c in lulu: ll = lulu[c]
                if c in sglu: gg = sglu[c]                
                t = (ll,gg)
                if t in d: 
                    d[t] += 1 
                else: 
                    d[t] = 1

                if ll[0] in ['Swamp','Marsh','Wetland']: nwl += 1
                if ll[0] == 'Waterbody': nlak += 1

            if lakf>0 and nlak>nwl and (nlak+nwl)/n>lakf: # setting sws as lake HRU
                self.hrus[sid] = "lake" #{170,1.0}
                cc+=1
            else:
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