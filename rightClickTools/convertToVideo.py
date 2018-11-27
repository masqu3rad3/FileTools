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
import subprocess

class converter(object):
    def __init__(self, selfDir=None):
        super(converter, self).__init__()

        self.compatibleVideos = [".avi", ".mov", ".mp4", ".flv", ".webm", ".mkv", ".mp4"]
        self.compatibleImages = [".tga", ".jpg", ".exr", ".png", ".pic"]

        if not selfDir:
            print "selfdir not defined"
            self.ffmpeg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ffmpeg.exe")
            self.ffprobe = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ffprobe.exe")
        else:
            print "selfdir defined"
            self.ffmpeg = os.path.join(os.path.dirname(selfDir), "ffmpeg.exe")
            self.ffprobe = os.path.join(os.path.dirname(selfDir), "ffprobe.exe")

        print "ffmpeg: %s\nffprobe: %s" %(self.ffmpeg, self.ffprobe)
        print "Sd", selfDir
        raw_input("press cont")

    def _loadJson(self, file):
        """Loads the given json file"""
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                return data
        except ValueError:
            msg = "Corrupted JSON file => %s" % file
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
        userDir = os.path.expanduser("~")
        rightClickDir = os.path.join(userDir, "RightClickTools")
        if not os.path.isdir(rightClickDir):
            os.makedirs(rightClickDir)

        conversionLUT_file = os.path.join(rightClickDir, "conversionLUT.json")
        if os.path.isfile(conversionLUT_file):
            try:
                with open(conversionLUT_file, 'r') as f:
                    data = json.load(f)
                    return data
            except ValueError:
                msg = "Corrupted JSON file => %s" % conversionLUT_file
                raise Exception(msg)
        else:
            # dump defaults
            presets_default={
                "preset1": {
                    "videoCodec": "-c:v libx264",
                    "audioCodec": "-c:a aac",
                    "speed": "-preset ultrafast",
                    "compression": "-crf 23",
                    "resolution": "-s 1280x720",
                    "foolproof": "-vf scale=ceil(iw/2)*2:ceil(ih/2)*2"
                },
                "preset2": {
                    "videoCodec": "-c:v libx264",
                    "audioCodec": "-c:a aac",
                    "speed": "-preset ultrafast",
                    "compression": "-crf 23",
                    "resolution": "-s 1280x720",
                    "foolproof": "-vf scale=ceil(iw/2)*2:ceil(ih/2)*2"
                },
                "preset3": {
                    "videoCodec": "-c:v libx264",
                    "audioCodec": "-c:a aac",
                    "speed": "-preset ultrafast",
                    "compression": "-crf 23",
                    "resolution": "-s 1280x720",
                    "foolproof": "-vf scale=ceil(iw/2)*2:ceil(ih/2)*2"
                },
                "preset4": {
                    "videoCodec": "-c:v libx264",
                    "audioCodec": "-c:a aac",
                    "speed": "-preset ultrafast",
                    "compression": "-crf 23",
                    "resolution": "-s 1280x720",
                    "foolproof": "-vf scale=ceil(iw/2)*2:ceil(ih/2)*2"
                },
                "preset5": {
                    "videoCodec": "-c:v libx264",
                    "audioCodec": "-c:a aac",
                    "speed": "-preset ultrafast",
                    "compression": "-crf 23",
                    "resolution": "-s 1280x720",
                    "foolproof": "-vf scale=ceil(iw/2)*2:ceil(ih/2)*2"
                }
            }
            self._dumpJson(presets_default, conversionLUT_file)
            return presets_default

    def _formatImageSeq(self, filePath):
        """
        Checks the path if it belongs to a sequence and formats it ready to be passes to FFMPEG
        :param filePath: a single member of a sequence
        :return: (String) Formatted path
        """

        sourceDir, sourceFile = os.path.split(filePath)
        seqList = pyseq.get_sequences(sourceDir)
        theSeq = self._findItem(sourceFile, seqList)
        if not theSeq:
            msg = "Cannot get the sequence list."
            raise Exception(msg)

        formattedName = "{0}{1}{2}".format(theSeq.head(), theSeq._get_padding(), theSeq.tail())
        formattedPath = os.path.normpath(os.path.join(sourceDir, formattedName))
        return formattedPath

    def queryAudio(self, sourcePath):
        print "ASDF", self.ffprobe
        command = [self.ffprobe, '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', sourcePath]
        # command = [self.ffprobe, '-v quiet', '-print_format json', '-show_format', '-show_streams', 'quiet', '-pretty', sourcePath]
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # print json.encoder(p.communicate())

        # r = json.load(p.communicate())
        # print r

        out, err = p.communicate()
        print "==========output=========="
        print out
        if err:
            print "========= error ========"
            print err

        # p = subprocess.Popen([self.ffprobe, '-show_format', '-pretty', '-loglevel quiet', '-i %s' %sourcePath],
        #                      stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # print p.communicate()

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

        if ext in self.compatibleVideos:
            type = "video"
            iFlag = '-i "%s"' %sourcePath
        elif ext in self.compatibleImages:
            type = "image"
            iFlag = '-i "%s"' %(self._formatImageSeq(sourcePath))
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
            return
        command = '{0} {1} {2} {3} {4} {5} -ignore_unknown {6} "{7}"'.format(
            self.ffmpeg,
            iFlag,
            presetLUT["videoCodec"],
            presetLUT["compression"],
            presetLUT["audioCodec"],
            presetLUT["resolution"],
            presetLUT["foolproof"],
            output
        )
        # subprocess.Popen([command], shell=True)
        print command
        raw_input("press any key to continue")
        os.system(command)

if __name__ == '__main__':

    if not os.path.isabs(sys.argv[0]):
        loc = os.path.abspath(__file__)
    else:
        loc = sys.argv[0]
    print loc
    app = converter(loc)

    # app.convert(sys.argv[1], sys.argv[2])
    app.convert(os.path.normpath(u'%s' %sys.argv[1]), "preset1")
    # app.queryAudio(os.path.normpath(u'%s' %sys.argv[1]))


