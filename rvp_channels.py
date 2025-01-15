

def write(root, nam, wshd):
    if wshd.haschans:
        default8point(root, nam, wshd)
    else:
        default_trap(root, nam)


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


def trapezoid(f, chname, w=10.0, s=0.001, n=0.035):
    f.write(':ChannelProfile {}\n'.format(chname))
    f.write(' :Bedslope {:5.3f}\n'.format(s))
    f.write(' :SurveyPoints\n')
    f.write('   {:12.3f}{:12.3f}\n'.format(0., 5.))
    f.write('   {:12.3f}{:12.3f}\n'.format(5*w+5, 0.))
    f.write('   {:12.3f}{:12.3f}\n'.format(6*w+5, 0.))
    f.write('   {:12.3f}{:12.3f}\n'.format(11*w+10, 5.))
    f.write(' :EndSurveyPoints\n')
    f.write(' :RoughnessZones\n')
    f.write('     0  {}\n'.format(n))
    f.write(' :EndRoughnessZones\n')
    f.write(':EndChannelProfile\n\n')        


def default8point(root, nam, wshd):
    tw, th = 20., 5. # terrace width and height (1/4 slope)
    bw, bh = 0.5, 1. # bank width and height
    
    with open(root + nam + ".rvp","a") as f:
        f.write('\n# -------------------\n')
        f.write('# channel profiles:\n')
        f.write('# -------------------\n')
    
        f.write(':RedirectToFile {}-channels.rvp\n\n'.format(nam))

    with open(root + nam + "-channels.rvp","w") as f:
        for t in wshd.xr:
            if wshd.lak[t]:
                trapezoid(f, 'lak_{}  # {}'.format(t, wshd.nam[t]))
            else:
                s = wshd.s[t]
                if s.chanwidth <= 0:
                    print(" ** ERROR: no channel width specified for watershed {}".format(t))
                    exit()   
                if s.chanrough <= 0: s.chanrough = 0.035
                if s.valleywidth <= 0: s.valleywidth = 2.5*s.chanwidth
                if s.floodplrough <= 0: s.floodplrough = 0.1

                if s.valleywidth <= s.chanwidth:
                    trapezoid(f, 'chn_{}  # {} {}'.format(t, wshd.nam[t], wshd.info[t]),s.chanwidth,s.slp,s.chanrough)
                else:
                    fpw = (s.valleywidth-s.chanwidth)/2 # floodplain width
                    f.write(':ChannelProfile chn_{}  # {} {}\n'.format(t, wshd.nam[t], wshd.info[t]))
                    f.write(' :Bedslope {:5.3f}\n'.format(s.slp))
                    f.write(' :SurveyPoints\n')
                    f.write('   {:12.3f}{:12.3f}\n'.format(0., s.elv+th))
                    f.write('   {:12.3f}{:12.3f}\n'.format(tw, s.elv))
                    f.write('   {:12.3f}{:12.3f}\n'.format(tw+fpw, s.elv))
                    f.write('   {:12.3f}{:12.3f}\n'.format(tw+bw+fpw, s.elv-bh))
                    f.write('   {:12.3f}{:12.3f}\n'.format(tw+bw+fpw+s.chanwidth, s.elv-bh))
                    f.write('   {:12.3f}{:12.3f}\n'.format(tw+2*bw+fpw+s.chanwidth, s.elv))
                    f.write('   {:12.3f}{:12.3f}\n'.format(tw+2*(bw+fpw)+s.chanwidth, s.elv))
                    f.write('   {:12.3f}{:12.3f}\n'.format(2*(tw+bw+fpw)+s.chanwidth, s.elv+th))
                    f.write(' :EndSurveyPoints\n')
                    f.write(' :RoughnessZones\n')
                    f.write('   {:12.3f}{:12.3f}\n'.format(0., s.floodplrough))
                    f.write('   {:12.3f}{:12.3f}\n'.format(tw+fpw, s.chanrough))
                    f.write('   {:12.3f}{:12.3f}\n'.format(tw+2*bw+fpw+s.chanwidth, s.floodplrough))
                    f.write(' :EndRoughnessZones\n')
                    f.write(':EndChannelProfile\n\n')        