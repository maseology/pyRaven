
import shutil

# create .bat file
def write(root, nam, ver):
    # shutil.copyfile("C:\\Program Files\\Raven\\Raven.exe", root + 'Raven' + ver + '.exe')
    # shutil.copyfile("E:\\Sync\\@dev\\Raven\\x64\\Release\\Raven.exe", root + 'Raven' + ver + '.exe')
    shutil.copyfile("E:\\Sync\\@dev\\Raven-bin\\Raven.exe", root + 'Raven' + ver + '.exe')
    with open(root + nam + ".bat","w") as f:
        f.write('@ECHO OFF\n')        
        f.write('Raven' + ver + '.exe "' + nam + '"\n')
        f.write('ECHO.\n')
        f.write('ECHO Run complete. Please press any key to close window.\n')
        f.write('PAUSE>NUL\n')

    