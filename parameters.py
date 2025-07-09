



class Params:
    # pyRaven parameters
    hru_minf = 0.0       # minimumm proportion of land use/surficial geology combination covering a catchment retained as a modelled HRU
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
    MAX_PERC_RATE_MULT = 1.0

    # land use parameters
    LAKE_PET_CORR = 1.0
    MELT_FACTOR = 3.5
    REFREEZE_FACTOR = 3.0
    MIN_MELT_FACTOR = 15.0
    MAX_MELT_FACTOR = 18.0
    DD_MELT_TEMP = 0.4
    DD_AGGRADATION = 0.1
    REFREEZE_EXP = 0.6
    DD_REFREEZE_TEMP = -1.8
    HMETS_RUNOFF_COEFF = 0.4
    HBV_BETA = 1.0

    # soil parameters
    PET_CORRECTION = 1.0
    FIELD_CAPACITY = 0.3
    SAT_WILT = 0.05
    MAX_CAP_RISE_RATE = 1.1216

    # routing parameters
    GAMMA_SHAPE = 2.2
    GAMMA_SCALE = 1.6
    GAMMA_SHAPE2 = 11.2
    GAMMA_SCALE2 = 0.4

    # interception parameters
    RAIN_ICEPT_FACT = 0.06
    SNOW_ICEPT_FACT = 0.04
    MAX_CAPACITY = 0.675
    MAX_SNOW_CAPACITY = 2.5

    # baseflow
    BASEFLOW_COEFF = 0.007
    BASEFLOW_N = 1.0
    INTERFLOW_COEFF = 0.04 # mm added

    def set(self, pset):
        for k,v in pset.items():
            p = k.strip()
            v = float(v)
            if hasattr(self,p.upper()):
                setattr(self, p.upper(), v)
            elif p=='maxbas':
                self.TIME_CONC = v
            else:
                print(" ** Warning: unknown parameter specified: {} {}".format(p,v))
            # match k.upper():
            #     case "TIME_CONC" | "MAXBAS": self.TIME_CONC = v
            #     case "TIME_LAG": self.TIME_LAG = v
            #     case "RAINSNOW_TEMP": self.RAINSNOW_TEMP = v
            #     case "RAINSNOW_DELTA": self.RAINSNOW_DELTA = v
            #     case "SNOW_SWI": self.SNOW_SWI = v
            #     case "SNOW_SWI_MIN": self.SNOW_SWI_MIN = v
            #     case "SNOW_SWI_MAX": self.SNOW_SWI_MAX = v
            #     case "SWI_REDUCT_COEFF": self.SWI_REDUCT_COEFF = v
            #     case "AVG_ANNUAL_RUNOFF": self.AVG_ANNUAL_RUNOFF = v
            #     case "LAKE_PET_CORR": self.LAKE_PET_CORR = v
            #     case "MELT_FACTOR": self.MELT_FACTOR = v
            #     case "REFREEZE_FACTOR": self.REFREEZE_FACTOR = v
            #     case _:
            #         print(" ** Warning: unknown parameter specified: {} {}".format(k,v))


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