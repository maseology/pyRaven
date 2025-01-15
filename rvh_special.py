



"""

not used yet, just keeping notes on some useful functions

:DisableSubBasinGroup [group_name] # disable selected subbasins to calibrate only a sub model (via :SubBasinGroup)

## can choose to disable upstream subbasin group from reservoir, since flows are being overridden
# :PopulateSubBasinGroup UpstreamMitchReservoir With SUBBASINS UPSTREAM_OF 3080228
# :DisableSubBasinGroup UpstreamMitchReservoir

OR

# turning off basins downstream of Lake Adonis subbasin
:PopulateSubBasinGroup DownstreamAdonis With SUBBASINS DOWNSTREAM_OF 3079982
:DisableSubBasinGroup DownstreamAdonis



"""