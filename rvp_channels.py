

def default_trap(root, nam):
    with open(root + nam + ".rvp","a") as f:
        f.write('\n# -------------------\n')
        f.write('# channel profile:\n')
        f.write('# -------------------\n')

        f.write(':ChannelProfile default_trap\n')
        f.write(' :Bedslope 0.001\n')
        f.write(' :SurveyPoints\n')
        f.write('     0  5\n')
        f.write('    55  0\n')
        f.write('    65  0\n')
        f.write('   120  5\n')
        f.write(' :EndSurveyPoints\n')
        f.write(' :RoughnessZones\n')
        f.write('     0  0.035\n')
        f.write(' :EndRoughnessZones\n')
        f.write(':EndChannelProfile\n\n')


def default8point(root, nam, wshd):
    tw, th = 20, 5 # terrace width and height (1/4 slope)
    bw, bh = 2, 2 # bank width and height
    
    with open(root + nam + ".rvp","a") as f:
        f.write('\n# -------------------\n')
        f.write('# channel profiles:\n')
        f.write('# -------------------\n')
    
        f.write(':RedirectToFile {}-channels.rvp\n\n'.format(root + nam))

    with open(root + nam + "-channels.rvp","w") as f:

        for t in wshd.xr:
            s = wshd.s[t]
            if s.chanrough <= 0:
                print(" ** ERROR: no channel roughness specified for watershed {}".format(t))
                exit()
            if s.chanwidth <= 0:
                print(" ** ERROR: no channel width specified for watershed {}".format(t))
                exit()                
            if s.floodplwidth <= 0: s.floodplwidth = 2.5*s.chanwidth
            if s.floodplrough <- 0: s.floodplrough = 0.1

            f.write(':ChannelProfile chn_{}\n'.format(t))
            f.write(' :Bedslope {}\n'.format(s.slp))
            f.write(' :SurveyPoints\n')
            f.write('   {:12.3}{:12.3}\n'.format(0, s.elv+th))
            f.write('   {:12.3}{:12.3}\n'.format(tw, s.elv))
            f.write('   {:12.3}{:12.3}\n'.format(tw+s.floodplwidth, s.elv))
            f.write('   {:12.3}{:12.3}\n'.format(tw+bw+s.floodplwidth, s.elv-bh))
            f.write('   {:12.3}{:12.3}\n'.format(tw+bw+s.floodplwidth+s.chanwidth, s.elv-bh))
            f.write('   {:12.3}{:12.3}\n'.format(tw+2*bw+s.floodplwidth+s.chanwidth, s.elv))
            f.write('   {:12.3}{:12.3}\n'.format(tw+2*(bw+s.floodplwidth)+s.chanwidth, s.elv))
            f.write('   {:12.3}{:12.3}\n'.format(2*(tw+bw+s.floodplwidth)+s.chanwidth, s.elv+th))
            f.write(' :EndSurveyPoints\n')
            f.write(' :RoughnessZones\n')
            f.write('   {:12.3}{:12.3}\n'.format(0, s.floodplrough))
            f.write('   {:12.3}{:12.3}\n'.format(tw+s.floodplwidth, s.chanrough))
            f.write('   {:12.3}{:12.3}\n'.format(tw+2*bw+s.floodplwidth+s.chanwidth, s.floodplrough))
            f.write(' :EndRoughnessZones\n')
            f.write(':EndChannelProfile\n\n')        