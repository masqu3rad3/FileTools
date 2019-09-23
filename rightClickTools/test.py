import os
import pyseq
reload(pyseq)
#
# def _findItem(itemPath, seqlist):
#     for x in seqlist:
#         if x.contains(itemPath):
#             return x

testDir = os.path.normpath("E:\\testingArea\\defaultsTest_defaultsTest_defaultsTest_190627\\Playblasts\\Houdini\\Model\\testMin\\v001")
# testSel = "shot01_beauty_v002_.0037.exr"

seqList = pyseq.get_sequences(testDir)
print seqList
# theSeq = _findItem(testSel, seqList)
# if not theSeq:
#     msg = "Cannot get the sequence list."
#     print msg
# else:
#     print "found"
#     print theSeq.head()
#     print theSeq._get_padding()
#
#     print "StartFrame", theSeq.start()
#     startFrame = theSeq.start()
#     startFrameAsStr = str(startFrame).format((theSeq._get_padding()))
#     print "HERD", startFrameAsStr
#
#     print "{0}{1}{2}".format(theSeq.head(), theSeq._get_padding(), theSeq.tail())
#
#


