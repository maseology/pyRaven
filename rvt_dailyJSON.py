

# build Time Series Input file (.rvt)
def write(root, nam, desc, builder, ver, met, preciponly):
    with open(root + nam + ".rvt","w") as f:
        f.write('# --------------------------------------------\n')
        f.write('# Raven temporal data (.rvt) file\n')
        f.write('# ' + desc + '\n')
        f.write('# written by ' + builder + '\n')
        f.write('# using pyRaven builder\n')
        f.write('# Raven version: ' + ver + '\n')
        f.write('# --------------------------------------------\n\n')

        f.write(':Gauge met\n')
        f.write(' :Latitude {}\n'.format(44.185))
        f.write(' :Longitude {}\n'.format(-79.479))
        f.write(' :Elevation {}\n'.format(250))
        f.write(' :MultiData\n')
        f.write('   {} {} {}\n'.format(met.dtb.strftime("%Y-%m-%d %H:%M:%S"), 1, len(met.dftem.index)))
        if preciponly:
            f.write(' :Parameters  TEMP_MAX  TEMP_MIN    PRECIP\n')
            f.write(' :Units              C         C      mm/d\n')
        else:
            f.write(' :Parameters  TEMP_MAX  TEMP_MIN  RAINFALL  SNOWFALL\n') # *** wbdc ordered ***
            f.write(' :Units              C         C      mm/d      mm/d\n')

        for _, row in met.dftem.iterrows():
            # NOTE: "+0"   https://stackoverflow.com/questions/11010683/how-to-have-negative-zero-always-formatted-as-positive-zero-in-a-python-string
            tx = round(row['Tx'],2)+0
            tn = round(row['Tn'],2)+0
            rf = row['Rf']
            sf = row['Sf']
            if preciponly:
                f.write('            {:>10.2f}{:>10.2f}{:>10.1f}\n'.format(tx, tn, rf+sf))
            else:
                f.write('            {:>10.2f}{:>10.2f}{:>10.1f}{:>10.1f}\n'.format(tx, tn, rf, sf))
        f.write(' :EndMultiData\n')              
        f.write(':EndGauge\n\n')