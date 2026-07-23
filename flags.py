

class flg:
    calibrationmode=False
    gwzonemode=False # use basin zones to define GW zones (currently never changes)
    writemetfiles=False
    preciponly=False
    preciprainmelt=False
    precipactive=False
    cache=False # for large builds, cache=True will save objects like wshd.pkl and hru.pkl to reduce expensive run times