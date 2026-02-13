
from pymmio import files as mmio
from pyRaven import batchfile, rvi_gr4j, rvh_lumped, rvp_gr4j, rvc_gr4j, rvp_channels, rvt_OWRCapi


# the simple GR4J model
# Perrin, C., Michel, C., & Andréassian, V. (2003). Improvement of a parsimonious model for streamflow simulation. Journal of hydrology, 279(1-4), 275-289.
def buildLumped(root, nam, desc, builder, ver, wshd, params, ts, dtb, dte):
    mmio.mkDir(root + "input")
    mmio.mkDir(root + "output")
    rvi_gr4j.write(root, nam, builder, ver, dtb, dte, None, ts)            
    rvh_lumped.write(root, nam, desc, builder, ver, wshd) # structure
    rvp_gr4j.write(root, nam, desc, builder, ver, params) # parameters
    rvc_gr4j.write(root, nam, desc, builder, ver, None, None) # initial conditions
    batchfile.write(root, nam, ver) 
