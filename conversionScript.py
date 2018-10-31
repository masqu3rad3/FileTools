import os


searchDir = os.path.normpath("E:\\_Sel")

flvList = [x for x in os.listdir(searchDir) if x.endswith(".flv")]

for x in flvList:
    name, ext = os.path.splitext(x)
    fromPath = os.path.join(searchDir,x)
    toPath = os.path.join(searchDir,"%s.mp4" %name)
    # print "Sdf", toPath
    print "converting %s" %x
    os.system('ffmpeg.exe -i "{0}" -c:v libx264 -crf 20 -c:a aac -strict -2 "{1}"'.format(fromPath, toPath))
