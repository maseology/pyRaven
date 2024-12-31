
import numpy as np
import math

class HRU:

    def __init__(self, wshd, lulu, sglu, minf, lakf, hdem, defaultLU, defaultSG):
        self.hrus = dict() # swsid: (lu,sg): frac
        self.zga = dict() # swsid: (lu,sg): (elev,slopeangle,aspect)

        zc, gc, ac = dict(), dict(), dict()
        for c, tec in hdem.tem.items():
            zc[c] = tec.z
            gc[c] = tec.g
            ac[c] = tec.a

        cc = 0
        for sid,cids in wshd.xr.items():
            d, z, g, ax, ay, gn = dict(), dict(), dict(), dict(), dict(), dict()
            n, nlak, nwl = 0, 0, 0
            for c in cids:
                n += 1
                
                # HARD-CODED DEFAULTS
                ll = defaultLU
                gg = defaultSG

                if c in lulu: ll = lulu[c]
                if c in sglu: gg = sglu[c]                
                t = (ll,gg)

                if zc[c]>-999:
                    if t in d: 
                        d[t] += 1 
                        z[t] += zc[c]                    
                    else: 
                        d[t] = 1
                        z[t] = zc[c]

                if gc[c] > 0:
                    if t in g:
                        g[t] += gc[c]
                        gn[t] += 1
                        ax[t] += math.sin(ac[c])
                        ay[t] += math.cos(ac[c])   
                    else:
                        g[t] = gc[c]
                        gn[t] = 1
                        ax[t] = math.sin(ac[c])
                        ay[t] = math.cos(ac[c])      

                if ll[0] in ['Swamp','Marsh','Wetland']: nwl += 1
                if ll[0] == 'Waterbody': nlak += 1

            if wshd.lak[sid] | (lakf>0 and nlak>nwl and (nlak+nwl)/n>lakf): # setting sws as lake HRU
                self.hrus[sid] = "lake" #{170,1.0}
                sz, sd = 0., 0.
                for t,dd in d.items():
                    sd += dd
                    sz += z[t]
                self.zga[sid] = float(sz/sd)
                cc+=1
            else:
                dd, sa = dict(), dict()
                dn = 0.0
                for t,v in d.items():
                    if v/n > minf: 
                        dd[t] = v/n
                        dn += v/n
                        if gn[t]==0:
                            sa[t] = (float(z[t]/v),0.,0.)
                        else:
                            gg = math.atan(g[t]/gn[t]) # rad
                            aa = (math.atan2(ax[t]/gn[t],ay[t]/gn[t]) + 2 * np.pi) % (2 * np.pi) # [0 to 2Pi] (raven requires [0 to 2Pi] over [-Pi to Pi])
                            sa[t] = (float(z[t]/v),gg,aa)
                
                # normalize
                for t,v in dd.items(): dd[t]/=dn
                self.hrus[sid] = dd
                self.zga[sid] = sa
                cc += len(dd)

        print(' {} distinct HRUs'.format(cc))