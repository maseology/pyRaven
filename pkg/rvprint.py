

def columns(f,a,ncol=10):
    nrow = int(len(a)/ncol)
    for i in range(nrow):
        f.write("      "+" ".join('{:10}'.format(x) for x in a[ncol*i:ncol*(i+1)])+"\n")
    if len(a)>ncol*nrow:
        f.write("      "+" ".join('{:10}'.format(x) for x in a[ncol*nrow:])+"\n")
