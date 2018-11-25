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


import os
import pyseq

def convertToVideo(sourcePath):
    compatibleVideos= ["avi", "mov", "mp4", "flv", "webm", "mkv"]
    compatibleImages= ["tga", "jpg", "exr", "png", "pic"]
    ext = os.path.splitext(sourcePath)[1]

    type = ""
    if ext in compatibleVideos:
        type = "video"
    elif ext in compatibleImages:
        type = "image"
    else:
        print "Selected item is not a compatible video or image file"
        return

    if type == "image":
        # gather sequence
        pass

