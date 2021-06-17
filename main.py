

# from pkg import buildBasinSM


# # build.HBV("M:/Peel/Raven-PWRMM21/PWRMM21.raven")


# buildBasinSM.BasinMelt("M:/OWRC-BasinRaven/OWRCbasin.raven")






import pandas as pd
from simpledbf import Dbf5

print('running..')
dbf = Dbf5("C:/Users/Mason/Desktop/Durham100U_ESGRA_Endpoint.dbf")
df = dbf.to_dataframe()

print(len(df.index))


print(df.columns)
df = df[df['FinalDistan'] > 500]
df = df[df['Status'] != 'Termainted_NoExit']


print(df.head())
print(len(df.index))


