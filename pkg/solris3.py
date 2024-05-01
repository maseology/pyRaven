
# 11	Open Beach/Bar 
# 21	Open Sand Dune 
# 23	Treed Sand Dune
# 41	Open Cliff and Talus
# 43	Treed Cliff and Talus
# 51	Open Alvar 
# 52	Shrub Alvar
# 53	Treed Alvar 
# 64	Open Bedrock
# 65	Sparse Treed
# 81	Open Tallgrass Prairie
# 82	Tallgrass Savannah
# 83	Tallgrass Woodland
# 90	Forest
# 91	Coniferous Forest
# 92	Mixed Forest
# 93	Deciduous Forest
# 131	Treed Swamp
# 135	Thicket Swamp 
# 140	Fen
# 150	Bog
# 160	Marsh
# 170	Open Water
# 191	Plantations – Tree Cultivated
# 192	Hedge Rows
# 193	Tilled
# 201	Transportation
# 202	Built-Up Area– Pervious
# 203	Built-Up Area– Impervious
# 204	Extraction–Aggregate
# 205	Extraction –Peat/Topsoil
# 250	Undifferentiated
# 255   Nodata

# TO

# 0	    noflow
# 1	    Waterbody
# 2	    ShortVegetation
# 3	    TallVegetation
# 4	    Urban
# 5	    Agriculture
# 6	    Forest
# 7	    Meadow
# 8	    Wetland
# 9	    Swamp
# 10	Marsh
# 11	Channel
# 12	Lake
# 13	Barren
# 14	SparseVegetation
# 15	DenseVegetation


__switcher = {
        11: ("Barren", "Bare"),
        21: ("Barren", "Bare"),
        23: ("Barren", "MixedVegetation"),
        41: ("Barren", "Bare"),
        43: ("Barren", "MixedVegetation"),
        51: ("Barren", "ShortVegetation"),
        52: ("Barren", "Shrub"),
        53: ("Barren", "MixedVegetation"),
        64: ("Barren", "Bare"),
        65: ("ShortVegetation", "MixedVegetation"),
        81: ("ShortVegetation", "ShortVegetation"),
        82: ("ShortVegetation", "MixedVegetation"),
        83: ("TallVegetation", "MixedVegetation"),
        90: ("Forest", "MixedVegetation"),
        91: ("Forest", "Coniferous"),
        92: ("Forest", "MixedVegetation"),
        93: ("Forest", "Deciduous"),
        131: ("Swamp", "MixedVegetation"),
        135: ("Swamp", "MixedVegetation"),
        140: ("Wetland", "ShortVegetation"),
        150: ("Wetland", "ShortVegetation"),
        160: ("Marsh", "ShortVegetation"),
        170: ("Waterbody", "Bare"),
        191: ("TallVegetation", "MixedVegetation"),
        192: ("DenseVegetation", "Shrub"),
        193: ("Agriculture", "ShortVegetation"),
        201: ("Barren", "Bare"),
        202: ("Urban", "MixedVegetation"),
        203: ("noflow", "Bare"),
        204: ("noflow", "Bare"),
        205: ("ShortVegetation", "ShortVegetation"),
        250: ("Agriculture", "ShortVegetation"),
        255: ("Agriculture", "ShortVegetation"),
        -9999: ("Agriculture", "ShortVegetation")
    }

def xr(solrisID): return __switcher[solrisID]

def xrr(): return dict([(v,k) for k,v in __switcher.items()])