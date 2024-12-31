
# landuse [IMPERM, FOREST_COV]
luxr = {'TallVegetation': (0.,1.), 
            'ShortVegetation': (0.,.1), 
            'DenseVegetation': (0.,1.), 
            'Forest': (0.,1.), 
            'Agriculture': (0.,1.), 
            'Waterbody': (0.,0.), 
            'Urban': (.85,0.), 
            'Swamp': (0.,.85),
            'Marsh': (0.,.25),  
            'Wetland': (0.,.25),  
            'Barren': (0.,0.),               
            'noflow': (0.,0.),
            'LAKE': (0.,0.)}


# vegetation [MAX_HT, MAX_LAI, MAX_LEAF_COND]
vxr = {'Coniferous': (3.,4.5,5.), 
            'Deciduous': (3.,4.5,5.), 
            'MixedVegetation': (3.,4.5,5.), 
            'Shrub': (1,2.5,5.), 
            'ShortVegetation': (.5,4.5,5.),
            'Bare': (0.,0.,.0001),
            'LAKE': (0.,0.,0.)}


# soils k [mm/yr]
sgxr = {'Low': 50., 
            'LowMedium': 150., 
            'Medium': 500.,
            'MediumHigh': 1500.,
            'High': 5000.,
            'WetlandSediments': 100.,  
            'Streambed': 1000.,               
            'Unknown': 500.}