

from pkg import buildHBV, buildBasin, buildStation
from pyInstruct import instruct


fp = "M:/CH/Raven/Raven2025.raven" #"O:/Orangeville-Raven/Orangeville.raven" #"M:/OWRC-Raven/OWRC23.raven" #"M:/MadRiverTest/Raven/MadRiverRaven.raven" #"M:/OWRC-Raven/OWRC22.raven" #"O:/Raven-snowmelt/OWRC-snowpack.raven" #"M:/Schomberg-Raven/SchombergBasin.raven" #"M:/Peel/Raven-PWRMM21/PWRMM21.raven"


ins = instruct.build(fp)
if ins.mode == "HBV":
    buildHBV.HBV(ins)
elif ins.mode == 'BasinSnowmelt':
    buildBasin.BasinMelt(ins)
elif ins.mode.lower() == 'snowmelt':
    buildStation.StationMelt(ins)
elif ins.mode == '':
    print('Raven builder "mode" not provided in ' + fp)
else:
    print('Raven builder mode "{}" not found'.format(ins.mode))

