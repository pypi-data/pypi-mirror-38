import os
import TM_CommonPy as TM

def WriteDictToTxtFile(cDict,sName):
    with open(sName,'w') as vFile:
        for vKey, vValue in cDict.items():
            vFile.write("{0:38} {1}\n".format(vKey,vValue))

def OrdString(sString):
    if not len(sString):
        return "<empty>"
    else:
        sString = str(sString)
        cReturning = "{"
        for c in sString:
            cReturning += c+"("+str(ord(c)) + "),"
        return cReturning[:-1]+"}"
