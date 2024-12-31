



class Params:
    # pyRaven parameters
    hru_minf = 0.0 # 0.05  # minimumm proportion of land use/surficial geology combination covering a catchment retained as a modelled HRU
    hru_min_lakef = -1.0 # minimum proportion of land use as lake to convert the HRU to a lake type; negative to ignore value

    # rvh
    TIME_CONC = 1.27 # aka HBV MAXBAS
    TIME_LAG = 0.0

    # global parameters
    RAINSNOW_TEMP = 0.0
    RAINSNOW_DELTA = 3.0
    SNOW_SWI = 0.05
    SNOW_SWI_MIN = 0.01
    SNOW_SWI_MAX = 0.3
    SWI_REDUCT_COEFF = 0.01
    AVG_ANNUAL_RUNOFF = 250

    # land use parameters
    LAKE_PET_CORR = 1.0
    MELT_FACTOR = 3.5
    REFREEZE_FACTOR = 3.0

    def set(self, pset):
        for k,v in pset.items():
            v = float(v)
            match k.upper():
                case "TIME_CONC" | "MAXBAS": self.TIME_CONC = v
                case "TIME_LAG": self.TIME_LAG = v
                case "RAINSNOW_TEMP": self.RAINSNOW_TEMP = v
                case "RAINSNOW_DELTA": self.RAINSNOW_DELTA = v
                case "SNOW_SWI": self.SNOW_SWI = v
                case "SNOW_SWI_MIN": self.SNOW_SWI_MIN = v
                case "SNOW_SWI_MAX": self.SNOW_SWI_MAX = v
                case "SWI_REDUCT_COEFF": self.SWI_REDUCT_COEFF = v
                case "AVG_ANNUAL_RUNOFF": self.AVG_ANNUAL_RUNOFF = v
                case "LAKE_PET_CORR": self.LAKE_PET_CORR = v
                case "MELT_FACTOR": self.MELT_FACTOR = v
                case "REFREEZE_FACTOR": self.REFREEZE_FACTOR = v
                case _:
                    print(" ** Warning: unknown parameter specified: {} {}".format(k,v))



# -------------------------------
## other
# -------------------------------
def getParameters(dpar):
    pout = {}
    if 'parameters' in dpar:
        for p,v in dpar['parameters'].items():
            p = p.upper()
            if p in ['RAINSNOW_TEMP','RAINSNOW_DELTA']:
                if not 'global' in pout: pout['global']={}
                pout['global'][p]=float(v)
            else:
                print('**WARNING: unknown parameter specified**')
    
    return pout