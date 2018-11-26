import os
import pyseq

def _findItem(itemPath, seqlist):
    for x in seqlist:
        if x.contains(itemPath):
            return x

testDir = os.path.normpath("M:\\Projects\\Molped_PedDemo_Shortcut_181003\\images\\shot01\\v002\\beauty")
testSel = "shot01_beauty_v002_.0037.exr"

seqList = pyseq.get_sequences(testDir)

theSeq = _findItem(testSel, seqList)
if not theSeq:
    msg = "Cannot get the sequence list."
    print msg
else:
    print "found"
    print theSeq.head()
    print theSeq._get_padding()

    print "{0}{1}{2}".format(theSeq.head(), theSeq._get_padding(), theSeq.tail())




