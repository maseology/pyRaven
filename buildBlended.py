
from pymmio import files as mmio
from pyRaven import batchfile, rvi_blended, rvh_lumped, rvp_blended, rvc_blended


# the "blended" Raven model
# after: Mai, J., Craig, J.R., Tolson, B.A., 2020. Simultaneously determining global sensitivities of model parameters and model structure. Hydrology and Earth System Sciences 24, 5835–5858
def buildLumped(root, nam, desc, builder, ver, wshd, params, ts, dtb, dte):
    mmio.mkDir(root + "input")
    mmio.mkDir(root + "output")
    rvi_blended.write(root, nam, builder, ver, dtb, dte, None, ts)            
    rvh_lumped.write(root, nam, desc, builder, ver, wshd, True) # structure
    rvp_blended.write(root, nam, desc, builder, ver, params) # parameters
    rvc_blended.write(root, nam, desc, builder, ver, None, None) # initial conditions
    batchfile.write(root, nam, ver) 
