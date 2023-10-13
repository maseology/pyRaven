
__switcher = {
        0: 'nodata',
        1: 'Low',       
        2: 'LowMedium', #'Low_Medium',
        3: 'Medium',
        4: 'MediumHigh', # 'Medium_High',
        5: 'High',
        6: 'Unknown', # variable
        7: 'Streambed', # fluvial/floodplain
        8: 'WetlandSediments', # organics
        -9999: 'nodata'
    }

def xr(surfgeoID): return __switcher[surfgeoID]

def xrr(): return dict([(v,k) for k,v in __switcher.items()])