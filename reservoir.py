
import os
import pandas as pd

class Res:

    rvh = None

    def __init__(self, hid, nam, minstage=None, maxstage=None, fp=None):
        _, file_extension = os.path.splitext(fp)

        self.hruid = hid
        self.name = nam
        self.minstage = minstage
        self.maxstage = maxstage        

        match file_extension:
            case '.csv': # monthly rule curve
                dfres = pd.read_csv(fp)
                cols = list(dfres)
                lower, upper, rulecurve = None, None, None
                if 'lower' in cols: lower = list(dfres.lower)
                if 'upper' in cols: upper = list(dfres.upper)
                if 'rulecurve' in cols: rulecurve = list(dfres.rulecurve)
                if not lower is None:
                    if len(upper) != len(lower):
                        print(' ** Reservoir rule-curve error 1')
                self.minbound = lower
                self.maxbound = upper
                self.rule = rulecurve
            case '.rvh': # pre-written raven reservoirs files
                with open(fp, 'r') as f: self.rvh = f.read()
            case _:
                print("  ** WARNING: unknown reservoir file type: "+fp)

