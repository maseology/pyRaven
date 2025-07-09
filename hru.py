
import numpy as np
import math
from pyproj import Proj
from pyRaven.flags import flg

class HRU:

    def __init__(self, wshd, lulu, sglu, minf, lakf, hdem, defaultLU, defaultSG, epsg, aggregateSmallHrus):
        prj = Proj('EPSG:'+str(epsg))
        self.hrus = dict()  # swsid:  (lu,sg): fractional cover
        self.xyzga = dict() # swsid:  (lu,sg): (lat,long,elev,slope-angle,aspect)
        self.cells = dict() # cellid: (lu,sg)

        xc, yc, zc, gc, ac = dict(), dict(), dict(), dict(), dict()
        for c, tec in hdem.tem.items():
            cxy = hdem.gd.Centroid(c)
            xc[c] = float(cxy[0])
            yc[c] = float(cxy[1])
            zc[c] = float(tec.z)
            gc[c] = float(tec.g)
            ac[c] = float(tec.a)

        cc = 0
        for sid,cids in wshd.xr.items():
            dt, xt, yt, zt, gt, axt, ayt, gnt = dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict()
            n, nlak, nwl = len(cids), 0, 0
            gwz = wshd.gwz[sid]
            for c in cids:                
                # HARD-CODED DEFAULTS
                ll = defaultLU
                gg = defaultSG

                if c in lulu: ll = lulu[c]
                if c in sglu: gg = sglu[c]
                t = (ll,(gg,gwz))
                self.cells[c] = t

                # collect elevations and centroids per hru
                if zc[c]>-999:
                    if t in dt: 
                        dt[t] += 1   
                        xt[t] += xc[c]
                        yt[t] += yc[c]
                        zt[t] += zc[c]
                    else: 
                        dt[t] = 1
                        xt[t] = xc[c]
                        yt[t] = yc[c]
                        zt[t] = zc[c]

                if gc[c] > 0:
                    if t in gt:
                        gnt[t] += 1
                        gt[t] += math.atan(gc[c]) # sum slopes (convert rise/run to angle)
                        axt[t] += math.sin(ac[c]) # sum x-component of aspect
                        ayt[t] += math.cos(ac[c]) # sum y-component of aspect
                    else:
                        gnt[t] = 1
                        gt[t] = math.atan(gc[c])
                        axt[t] = math.sin(ac[c])
                        ayt[t] = math.cos(ac[c])      

                if ll[0] in ['Swamp','Marsh','Wetland']: nwl += 1 # counting the number of wetlands
                if ll[0] == 'Waterbody': nlak += 1 # counting the number of waterbodies

            if wshd.lak[sid] | (lakf>0 and nlak>nwl and (nlak+nwl)/n>lakf): # setting sws as lake HRU
                self.hrus[sid] = "lake"
                wshd.lak[sid] = True
                sx, sy, sz, sd = 0., 0., 0., 0.
                for t,dd in dt.items():
                    sd += dd
                    sx += xt[t]
                    sy += yt[t]                    
                    sz += zt[t]

                lng,lat = prj(sx/sd, sy/sd, inverse=True)
                self.xyzga[sid] = (lng,lat,sz/sd)
                cc+=1
            else:
                dd, sa = dict(), dict()

                if aggregateSmallHrus:
                # with aggregation
                    x, y, z, g, ax, ay, gn = dict(), dict(), dict(), dict(), dict(), dict(), dict()
                    def aggregate(t,tg,v,cidm=None):
                        if tg in dd:
                            dd[tg] += v
                            x[tg] += xt[t]
                            y[tg] += yt[t]
                            z[tg] += zt[t]
                            if t in gnt and gnt[t]>0:
                                if tg in g:
                                    g[tg] += gt[t]
                                    gn[tg] += gnt[t]
                                    ax[tg] += axt[t]
                                    ay[tg] += ayt[t]
                                else:
                                    g[tg] = gt[t]
                                    gn[tg] = gnt[t]
                                    ax[tg] = axt[t]
                                    ay[tg] = ayt[t]                                
                        else:
                            dd[tg] = v
                            x[tg] = xt[t]
                            y[tg] = yt[t]
                            z[tg] = zt[t]
                            if t in gnt and gnt[t]>0:
                                g[tg] = gt[t]
                                gn[tg] = gnt[t]
                                ax[tg] = axt[t]
                                ay[tg] = ayt[t]
                        if cidm is not None:
                            for c in cidm: self.cells[c]=tg

                    for t,v in dt.items():               
                        if v/n > minf: # large combination, keep as-is
                            aggregate(t,t,v)
                        else:          # small combination, aggregate to general groups
                            cidm = list()
                            for c in cids: 
                                if self.cells[c]==t: cidm.append(c)
                            if t[0][0]=='Urban':
                                aggregate(t,(("Urban", "Bare"),('LowMedium',gwz)),v,cidm)
                            else:
                                match t[1]:
                                    case 'WetlandSediments': # WetlandSediments/organics
                                        aggregate(t,(("Wetland", "ShortVegetation"),('WetlandSediments',gwz)),v,cidm)
                                    case _:
                                        match t[0][0]:
                                            case "Wetland" | "Swamp":
                                                aggregate(t,(("Wetland", "ShortVegetation"),('WetlandSediments',gwz)),v,cidm)
                                            case _: # other/natural
                                                # aggregate(t,(("ShortVegetation", "ShortVegetation"),('Unknown',gwz)),v,cidm)
                                                aggregate(t,(("ShortVegetation", "ShortVegetation"),t[1]),v,cidm)
                                # match t[1]:
                                #     case 'Streambed': # Streambed/fluvial/floodplain
                                #         aggregate(t,(("ShortVegetation", "ShortVegetation"),('Streambed',gwz)),v,cidm)
                                #     case 'WetlandSediments': # WetlandSediments/organics
                                #         aggregate(t,(("Wetland", "ShortVegetation"),('WetlandSediments',gwz)),v,cidm)
                                #     case _:
                                #         match t[0][0]:
                                #             case 'Agriculture': # agriculture
                                #                 aggregate(t,(("Agriculture", "ShortVegetation"),t[1]),v,cidm)
                                #             case "Wetland" | "Swamp":
                                #                 aggregate(t,(("Wetland", "ShortVegetation"),('WetlandSediments',gwz)),v,cidm)
                                #             case _: # other/natural
                                #                 aggregate(t,(("ShortVegetation", "ShortVegetation"),t[1]),v,cidm)

                    for t,v in dd.items(): 
                        dd[t]/=n # normalize
                        lng,lat = prj(x[t]/v, y[t]/v, inverse=True)
                        if not t in gn or gn[t]==0:
                            sa[t] = (lng,lat,z[t]/v,0.,0.)
                        else:
                            gg = g[t]/gn[t] # radians
                            aa = (math.atan2(ax[t]/gn[t],ay[t]/gn[t]) + 2 * np.pi) % (2 * np.pi) # [0 to 2pi]
                            sa[t] = (lng,lat,z[t]/v,gg,aa)
                else:
                    # no aggregation (ignores small combinations)
                    dn = 0.
                    for t,v in dt.items():
                        if v/n > minf: 
                            dd[t] = v/n
                            dn += v/n
                            lng,lat = prj(xt[t]/v, yt[t]/v, inverse=True)
                            if not t in gnt or gnt[t]==0:
                                sa[t] = (lng,lat,float(zt[t]/v),0.,0.)
                            else:
                                gg = math.atan(gt[t]/gnt[t]) # rad
                                aa = (math.atan2(axt[t]/gnt[t],ayt[t]/gnt[t]) + 2 * np.pi) % (2 * np.pi) # [0 to 2Pi] (raven requires [0 to 2Pi] over [-Pi to Pi])
                                sa[t] = (lng,lat,float(zt[t]/v),gg,aa)
                    # normalize
                    for t,v in dd.items(): dd[t]/=dn


                self.hrus[sid] = dd
                self.xyzga[sid] = sa
                cc += len(dd)
        
        self.nhru = cc
        if aggregateSmallHrus:
            print(' {} distinct HRUs (small HRUs aggregated to general types)'.format(cc))
        else:
            print(' {} distinct HRUs (small HRUs aggregated to mega HRU)'.format(cc))

    def writeHRUidBil(self, dir, nam, gd, wshd):
        # if os.path.exits(dir+nam+'-hruid.bil'): return
        d = dict()
        tt = dict()
        c = 0
        for sid,lusg in self.hrus.items():
            if lusg=='lake':
                c+=1
                for cid in wshd.xr[sid]: d[cid] = c

        for sid,lusg in self.hrus.items():
            if lusg=='lake': continue
            tt[sid] = dict()
            for t,_ in lusg.items():
                c+=1
                tt[sid][t] = c
 
        for sid,cids in wshd.xr.items():
            if not sid in tt: continue
            for c in cids:
                t = self.cells[c]
                if not t in tt[sid]:
                    d[c] = -1
                else:
                    d[c] = tt[sid][t]

        gd.saveBinaryInt(dir+nam+'-hruid.bil',d)

    def distinctTypes(self):
        # collect distinct IDs
        dlu = set()
        dsg = set()
        dveg = set()
        hasLake = False
        for _,vv in self.hrus.items():
            if vv=='lake':
                hasLake = True
            else:
                for v in vv:
                    dlu.add(v[0][0])
                    dveg.add(v[0][1])
                    if flg.gwzonemode:
                        dsg.add((v[1][0],v[1][1]))
                    else:
                        dsg.add(v[1][0])

        dlu = sorted(dlu)
        dveg = sorted(dveg)
        dsg = sorted(dsg)
        if hasLake:
            dlu.append('LAKE')
            dveg.append('LAKE')
            dsg.append('LAKE')

        return dlu, dveg, dsg