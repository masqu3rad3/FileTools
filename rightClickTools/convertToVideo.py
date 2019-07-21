# Converts selected video (or sequence) to video
# uses ffmpeg

# may have a small menu for:
    # Compression (low(mail), medium(wetransfer), high(production)
    # Resolution ('Half-HD', 'HD', 'Original'

# -----
# NOTES
# -----
# Flags
# -----

# -y (global)
# Overwrite output files without asking.

# ffmpeg -i INPUT -map 0 -c:v libx264 -c:a copy OUTPUT
# encodes all video streams with libx264 and copies all audio streams.
#
# For each stream, the last matching c option is applied, so
#
# ffmpeg -i INPUT -map 0 -c copy -c:v:1 libx264 -c:a:137 libvorbis OUTPUT
# will copy all the streams except the second video, which will be encoded with libx264, and the 138th audio, which will be encoded with libvorbis.


# Seems good ->
# ffmpeg -i testVid.avi -c:v libx264 -preset ultrafast -crf 23 -c:a copy testOut.mp4

# from sequence ->
# ffmpeg -i originalSeq.%04d.jpg -c:v libx264 -preset ultrafast -crf 23 -s 1280x720 testOutSeq.mp4

# MAKE SURE THE DIMENSIONS ARE EVEN
# ffmpeg -i originalSeq.%04d.jpg -c:v libx264 -preset ultrafast -crf 23 -vf "scale=ceil(iw/2)*2:ceil(ih/2)*2" testOutSeq.mp4



import sys
import os
import pyseq
import json
import shutil
# import subprocess

class converter(object):
    def __init__(self, selfDir=None, presetName=None):
        super(converter, self).__init__()

        self.compatibleVideos = [".avi", ".mov", ".mp4", ".flv", ".webm", ".mkv", ".mp4", ".3gp"]
        self.compatibleImages = [".tga", ".jpg", ".exr", ".png", ".pic", ".dpx"]


        if not selfDir:
            selfDir = os.path.abspath(__file__)

        # get external file paths
        self.ffmpeg = os.path.join(os.path.dirname(selfDir), "ffmpeg.exe")
        # self.ffprobe = os.path.join(os.path.dirname(selfDir), "ffprobe.exe")
        self.conversionLUT = os.path.join(os.path.dirname(selfDir), "conversionLUT.json")


    def _loadJson(self, file):
        """Loads the given json file"""
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                return data
        except ValueError:
            msg = "Corrupted JSON file => %s" % file
            print msg
            raw_input("press any key to exit")
            raise Exception(msg)

    def _dumpJson(self, data, file):
        """Saves the data to the json file"""
        name, ext = os.path.splitext(file)
        tempFile = "{0}.tmp".format(name)
        with open(tempFile, "w") as f:
            json.dump(data, f, indent=4)
        shutil.copyfile(tempFile, file)
        os.remove(tempFile)

    def _findItem(self, itemPath, seqlist):
        """finds out which sequence the given file belongs to among the given sequence list"""
        for x in seqlist:
            if x.contains(itemPath):
                return x

    def _get_conversionDict(self):
        """Loads the the conversion dictionary"""

        if os.path.isfile(self.conversionLUT):
            data = self._loadJson(self.conversionLUT)
            return data
        else:
            # dump defaults
            presets_default={
                "mailQuality": {
                    "videoCodec": "-c:v libx264",
                    "audioCodec": "-c:a aac",
                    "speed": "-preset ultrafast",
                    "compression": "-crf 23",
                    "resolution": "-s 1280x720",
                    "foolproof": "-vf scale=ceil(iw/2)*2:ceil(ih/2)*2"
                },
                "mediumQuality": {
                    "videoCodec": "-c:v libx264",
                    "audioCodec": "-c:a aac",
                    "speed": "-preset fast",
                    "compression": "-crf 23",
                    "resolution": "",
                    "foolproof": "-vf scale=ceil(iw/2)*2:ceil(ih/2)*2"
                },
                "highQuality": {
                    "videoCodec": "-c:v libx264",
                    "audioCodec": "-c:a aac",
                    "speed": "-preset medium",
                    "compression": "-crf 7",
                    "resolution": "",
                    "foolproof": "-vf scale=ceil(iw/2)*2:ceil(ih/2)*2"
                }
            }
            self._dumpJson(presets_default, self.conversionLUT)
            return presets_default

    def _formatImageSeq(self, filePath):
        """
        Checks the path if it belongs to a sequence and formats it ready to be passes to FFMPEG
        :param filePath: a single member of a sequence
        :return: (String) Formatted path, (int) Starting frame
        """

        sourceDir, sourceFile = os.path.split(filePath)
        seqList = pyseq.get_sequences(sourceDir)
        theSeq = self._findItem(sourceFile, seqList)
        if not theSeq:
            msg = "Cannot get the sequence list."
            raise Exception(msg)

        formattedName = "{0}{1}{2}".format(theSeq.head(), theSeq._get_padding(), theSeq.tail())
        formattedPath = os.path.normpath(os.path.join(sourceDir, formattedName))
        return formattedPath, theSeq.start()

    # def queryAudio(self, sourcePath):
    #     command = [self.ffprobe, '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', sourcePath]
    #     # command = [self.ffprobe, '-v quiet', '-print_format json', '-show_format', '-show_streams', 'quiet', '-pretty', sourcePath]
    #     p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #     # print json.encoder(p.communicate())
    #
    #     # r = json.load(p.communicate())
    #     # print r
    #
    #     out, err = p.communicate()
    #     print "==========output=========="
    #     print out
    #     if err:
    #         print "========= error ========"
    #         print err
    #
    #     # p = subprocess.Popen([self.ffprobe, '-show_format', '-pretty', '-loglevel quiet', '-i %s' %sourcePath],
    #     #                      stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #     # print p.communicate()

    def convert(self, sourcePath, presetName):
        # print sourcePath
        # sourcePath = unicode(sourcePath.replace(" ", "_"))
        # print sourcePath
        # if selfLoc:
        #     baseDir = os.path.split(selfLoc)[0]
        #     self.ffmpeg = os.path.join(baseDir, "ffmpeg.exe")
        #     self.ffprobe = os.path.join(baseDir, "ffprobe.exe")

        if not os.path.isfile(self.ffmpeg):
            print "ffmpeg.exe is missing"
            raw_input("Press any key to abort")
            return
        conversionLUT = self._get_conversionDict()
        try:
            presetLUT = conversionLUT[presetName]
        except KeyError:
            msg = "Preset Name is not defined in the conversionLUT.json"
            raise Exception(msg)

        ext = os.path.splitext(sourcePath)[1]

        if ext.lower() in self.compatibleVideos:
            iFlag = '-i "%s"' %sourcePath
        elif ext in self.compatibleImages:
            filename, startFrame = self._formatImageSeq(sourcePath)
            iFlag = '-start_number %s -i "%s"' %(startFrame, filename)
            presetLUT["audioCodec"] = ""

        else:
            print "Selected item is not a compatible video or image file"
            raw_input("Press any key to abort")
            return

        base, ext = os.path.splitext(sourcePath)
        output = "%s_%s.mp4" %(base, presetName)
        if os.path.isfile(output):
            msg = "%s already exists. Quitting" %output
            print msg
            raw_input("Press any key to exit")
            return
        # os.system requires an extra quote in the beginning to deal with spaces in folder names
        command = '""{0}" {1} {2} {3} {4} {5} -ignore_unknown {6} "{7}"'.format(
            self.ffmpeg,
            iFlag,
            presetLUT["videoCodec"],
            presetLUT["compression"],
            presetLUT["audioCodec"],
            presetLUT["resolution"],
            presetLUT["foolproof"],
            output
        )

        os.system(command)

if __name__ == '__main__':

    if not os.path.isabs(sys.argv[0]):
        loc = os.path.abspath(__file__)
    else:
        loc = sys.argv[0]
    print loc
    app = converter(loc)

    try:
        presetName = sys.argv[2]
    except IndexError:
        presetName = "mailQuality"


    # app.convert(sys.argv[1], sys.argv[2])
    app.convert(os.path.normpath(u'%s' %sys.argv[1]), presetName)
    # app.queryAudio(os.path.normpath(u'%s' %sys.argv[1]))


