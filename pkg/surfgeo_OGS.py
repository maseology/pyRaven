
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


def convertOGStoRelativeK(d):
    x = xrr()
    x['Variable'] = x['Unknown']
    x['Fluvial'] = x['Streambed']
    x['Organic'] = x['WetlandSediments']
    ogs = {
        0: 'Variable',      # Waterbody
        10: 'Low',          # Precambrian bedrock
        20: 'Low',          # Bedrock-drift complex in Precambrian terrain
        21: 'Low',          # Bedrock-drift complex in Precambrian terrain: Primarily till cover
        22: 'Low',          # Bedrock-drift complex in Precambrian terrain: Primarily stratified drift cover
        30: 'Variable',     # Sedimentary (Paleozoic) bedrock
        40: 'Variable',     # Bedrock-drift complex in Paleozoic terrain
        41: 'Variable',     # Bedrock-drift complex in Paleozoic terrain: Primarily till cover
        50: 'Medium',       # Till (Diamicton)
        51: 'Medium',       # Till: Silty sand to sand-textured till on Precambrian terrain
        52: 'LowMedium',    # Till: Stone-poor, sandy silt to silty sand-textured till on Paleozoic terrain
        53: 'Medium',       # Till: Stony, sandy silt to silty sand-textured till on Paleozoic terrain
        54: 'Low',          # Till: Clay to silt-textured till (derived from glaciolacustrine deposits or shale)
        55: 'Variable',     # Till: Undifferentiated older tills, may include stratified deposits
        60: 'High',         # Ice-contact stratified deposits
        61: 'High',         # Ice-contact stratified deposits: In moraines, eskers, kames and crevasse fills
        62: 'High',         # Ice-contact stratified deposits: In subaquatic fans
        70: 'High',         # Glaciofluvial deposits: Sandy deposits
        71: 'High',         # Glaciofluvial deposits: Gravelly deposits
        72: 'High',         # Glaciofluvial deposits
        80: 'Low',          # Fine-textured glaciolacustrine deposits
        81: 'Low',          # Fine-textured glaciolacustrine deposits: Massive to well laminated
        82: 'Low',          # Fine-textured glaciolacustrine deposits: Interbedded silt and clay and gritty, pebbly flow till and rainout deposits
        90: 'High',         # Coarse-textured glaciolacustrine deposits
        91: 'High',         # Coarse-textured glaciolacustrine deposits: Deltaic deposits
        92: 'High',         # Coarse-textured glaciolacustrine deposits: Littoral deposits
        93: 'High',         # Coarse-textured glaciolacustrine deposits: Foreshore and basinal deposits
        120: 'Fluvial',     # Older alluvial deposits
        130: 'Low',         # Fine-textured lacustrine deposits
        140: 'High',        # Coarse-textured lacustrine deposits
        142: 'High',        # Coarse-textured lacustrine deposits: Littoral deposits
        143: 'High',        # Coarse-textured lacustrine deposits: Foreshore and basinal deposits
        170: 'MediumHigh',  # Eolian deposits
        190: 'Fluvial',     # Modern alluvial deposits
        200: 'Organic',     # Organic Deposits
        210: 'Variable'     # Fill
    }    
    return {k:x[ogs[v]] for k,v in d.items()}