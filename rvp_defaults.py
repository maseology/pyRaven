
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
vxr = {'Coniferous': (30.,7.,5.), 
            'Deciduous': (25.,4.5,5.3), 
            'MixedVegetation': (25.,4.5,5.3), 
            'Shrub': (1,1.,5.3), 
            'ShortVegetation': (.5,4.5,5.3),
            'Bare': (0.,0.,0.),
            'LAKE': (0.,0.,0.)}

def seasonalLAI(vtyp):
    if vtyp == 'Bare':
        return '  {:25}  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0\n'.format(vtyp)
    elif vtyp == 'LAKE':
        return '  {:25}  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0\n'.format(vtyp)
    elif vtyp == 'Coniferous':
        return '  {:25}  4.0  4.0  4.0  4.0  4.0  4.0  4.0  4.0  4.0  4.0  4.0  4.0\n'.format(vtyp)
    elif vtyp == 'MixedVegetation':
        return '  {:25}  2.0  2.0  2.0  2.0  2.0  3.0  4.0  4.0  4.0  3.0  2.0  2.0\n'.format(vtyp)
    else:
        return '  {:25}  0.0  0.0  0.0  0.0  1.0  2.0  4.5  4.5  3.0  2.0  0.0  0.0\n'.format(vtyp)

# soils k [mm/yr]
sgxr = {'Low': 50., 
            'LowMedium': 150., 
            'Medium': 500.,
            'MediumHigh': 1500.,
            'High': 5000.,
            'WetlandSediments': 100.,  
            'Streambed': 1000.,               
            'Unknown': 500.}