

def write(root, nam, hru, res):
    firstRes=True
    resColl = set()
    with open(root + nam + ".rvc","a") as f:
        if res is not None:
            if firstRes:
                firstRes=False
                f.write('\n')
            for k,v in res.items():
                if not k in hru.hrus: continue # needed when sub-setting model domain
                f.write(':InitialReservoirStage {:>10} {:>10.1f}\n'.format(k,(v.maxbound[9]+v.minbound[9])/2))
                resColl.add(k)

        for k,lusg in hru.hrus.items():
            if lusg=='lake':
                if k in resColl: continue
                if firstRes:
                    firstRes=False
                    f.write('\n')
                f.write(':InitialReservoirStage {:>10} {:>10.1f}\n'.format(k,hru.xyzga[k][2]))