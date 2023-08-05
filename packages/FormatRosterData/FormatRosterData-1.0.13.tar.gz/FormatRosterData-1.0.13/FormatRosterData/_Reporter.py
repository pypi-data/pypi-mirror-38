from FormatRosterData._Logger import FRDLog
from FormatRosterData._Logger import vFormatter
import logging
import enum

class Reporter():
    """Collects error messages to be reported"""

    def __init__(self):
        self.cNameToURLErrorMsgs = []
        self.cGetOldWorkbookMsgs = []
        self.cUnmatchedFileNames = []
        self.cFormattingErrorFileNames = []
        self.cSuccessfulFormatFileNames = []

    @staticmethod
    def _ReportCollection(cCollection,sTitleMsg):
        if cCollection:
            FRDLog.info("\t"+str(len(cCollection)) + " " + sTitleMsg)
            for sFileName in cCollection:
                FRDLog.info(sFileName)

    def WriteReport(self):
        FRDLog.info("---Report---")
        #-
        #I didn't want to include the successes in the report, but they should still be logged
        self._ReportCollection(self.cSuccessfulFormatFileNames,"SUCCESSFULLY FORMATTED FILES")
        #-Add Report.txt handler to FRDLog
        vFileHandler = logging.FileHandler("__Report.txt")
        vFileHandler.setFormatter(logging.Formatter('%(message)s'))
        vFileHandler.setLevel(1)
        FRDLog.addHandler(vFileHandler)
        #-
        self._ReportCollection(self.cNameToURLErrorMsgs,"NAME TO URL ERRORS")
        self._ReportCollection(self.cGetOldWorkbookMsgs,"GET OLD WORKBOOK ERRORS")
        self._ReportCollection(self.cFormattingErrorFileNames,"ERROR FILES")
        self._ReportCollection(self.cUnmatchedFileNames,"UNMATCHED")
        if not self.cNameToURLErrorMsgs and not self.cGetOldWorkbookMsgs and not self.cFormattingErrorFileNames and not self.cUnmatchedFileNames:
            FRDLog.info("There were no errors.")
        #-Remove Report.txt handler from FRDLog
        FRDLog.handlers.remove(vFileHandler)
