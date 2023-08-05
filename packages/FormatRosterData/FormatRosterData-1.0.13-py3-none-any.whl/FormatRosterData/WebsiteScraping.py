import os
import openpyxl
import TM_CommonPy as TM
import lxml.html
import requests
from FormatRosterData._Logger import FRDLog
import FormatRosterData as FRD

def IsHeaderRow(vItem):
    bNumberColFound = False
    bNameColFound = False
    for i in range(len(vItem)-1):
        if "no" == DigForText(vItem[i])[0:2].lower():
            bNumberColFound = True
        if "name" == DigForText(vItem[i])[0:4].lower():
            bNameColFound = True
            if bNumberColFound and bNameColFound:
                break
    return bNumberColFound and bNameColFound

def IsBodyGrid(vItem):
    for i in range(len(vItem)-1):
        if hasattr(vItem[i],"tag") and "tr" == vItem[i].tag[0:2] and len(vItem) > 2:
            return True

def GetRosterTable(vTree):
    try:
        return vTree.xpath('//table')[-1]
    except IndexError:
        return

def GetWorkbook(sURL):
    FRDLog.debug(TM.FnName()+"`Open. sURL:"+sURL)
    #---Get RosterTable
    vRosterPage = requests.get(sURL)
    tree = lxml.html.fromstring(vRosterPage.content)
    vRosterTable = GetRosterTable(tree)
    if vRosterTable is None:
        FRDLog.warning(TM.FnName()+"`Could not find RosterTable")
        return
    #---Search for 1dHeader and 2dBody
    vHeader = None
    vBody = None
    if IsBodyGrid(vRosterTable):
        vBody = vRosterTable
    for vFirstIter in vRosterTable: #Maybe could be cleaner
        if vHeader is None and IsHeaderRow(vFirstIter): #casting vHeader as bool causes warning
            vHeader = vFirstIter
        if vBody is None and IsBodyGrid(vFirstIter):
            vBody = vFirstIter
        if vBody is not None and vHeader is not None:
            break
        for vSecondIter in vFirstIter:
            if vHeader is None and IsHeaderRow(vSecondIter):
                vHeader = vSecondIter
            if vBody is None and IsBodyGrid(vSecondIter):
                vBody = vSecondIter
            if vBody is not None and vHeader is not None:
                break
            for vItem in vSecondIter:
                if vHeader is None and IsHeaderRow(vItem):
                    vHeader = vItem
                if vBody is None and IsBodyGrid(vItem):
                    vBody = vItem
                if vBody is not None and vHeader is not None:
                    break
    if vHeader is None and vBody is None:
        FRDLog.warning(TM.FnName()+"`Could find neither RosterHeader nor RosterBody")
        return
    if vHeader is None:
        FRDLog.warning(TM.FnName()+"`Could not find RosterHeader")
        return
    if vBody is None:
        FRDLog.warning(TM.FnName()+"`Could not find RosterBody")
        return
    #-if header is in body, take it out.
    for i in range(len(vBody)-1):
        if vBody[i] == vHeader:
            vBody = vBody[i+1:]
            break
    #---Convert vHeader and vBody to openpyxl workbook
    vWorkbook = openpyxl.Workbook()
    vSheet = vWorkbook.active
    for iCol, vItem in enumerate(vHeader):
        vSheet[TM.openpyxl.PosByXY(iCol,0)] = TM.RemoveWhitespace(DigForText(vItem))
    for iRow, vRow in enumerate(vBody):
        for iCol, vItem in enumerate(vRow):
            vSheet[TM.openpyxl.PosByXY(iCol,iRow+1)] = DigForText_IncludeTails_NoLabel(vItem) #Row gets +1 for header.
    FRDLog.debug(TM.FnName()+"`Close")
    return vWorkbook

def DigForText(vElem):
    for _ in range(15):
        if isinstance(vElem.text,str) and not TM.RemoveWhitespace(vElem.text) in ("",None):
            return vElem.text
        try:
            vElem = vElem[0]
        except IndexError:
            return ""
    return ""

def IfNoneBeNothing(s):
    return '' if s is None else s

def GetChildrenTails(vElem):
    sTails = ""
    for vChild in vElem:
        sTails += IfNoneBeNothing(vChild.tail)
    return sTails

def DigForText_IncludeTails_NoLabel(vElem): #Why are people writing text in the tails of sub elements?
    for _ in range(15):
        sReturning = (IfNoneBeNothing(vElem.text)+GetChildrenTails(vElem)).strip(None)
        sReturning = " ".join(sReturning.split())
        if not sReturning == "":
            return sReturning
        else:
            if len(vElem) and not (vElem[0].tag == 'span' and 'class' in vElem[0].attrib and vElem[0].attrib['class'] == 'label'): #if child has elements and it's a label
                vElem = vElem[0]
            else:
                return ""
    return ""

def ScrapeNameToURLDict(eSportCatagory):
    if eSportCatagory == FRD.SportCatagory.Basketball_Men:
        sURL = 'http://www.espn.com/mens-college-basketball/team/roster/_/id/120'
        #---Get vList
        vRosterPage = requests.get(sURL)
        tree = lxml.html.fromstring(vRosterPage.content)
        #vList = tree.xpath('//*[@id="fittPageContainer"]/div[3]/div[2]/div[1]/div[1]/section/section/div[1]/div/select[1]')[0]
        vList = tree.xpath('//select[@class="dropdown__select"]')[1] #Perhaps there is a more reliable xpath
        #---
        cNameToURL = dict()
        for vItem in vList:
            if "More NCAAM teams" == DigForText(vItem): #Irrelevant key and value
                continue
            cNameToURL[DigForText(vItem)] = "http://www.espn.com" + vItem.attrib['data-url']
        return cNameToURL
    elif eSportCatagory == FRD.SportCatagory.Basketball_Women:
        sURL = 'http://www.espn.com/womens-college-basketball/team/roster/_/id/120'
        #---Get vList
        vRosterPage = requests.get(sURL)
        tree = lxml.html.fromstring(vRosterPage.content)
        #vList = tree.xpath('//*[@id="fittPageContainer"]/div[3]/div[2]/div[1]/div[1]/section/section/div[1]/div/select[1]')[0]
        vList = tree.xpath('//select[@class="select-box"]')[0] #Perhaps there is a more reliable xpath
        #---
        cNameToURL = dict()
        for vItem in vList:
            if DigForText(vItem) in ("Women's College Basketball Teams","More NCAAM teams"): #Irrelevant key and value
                continue
            cNameToURL[DigForText(vItem)] = "http:" + vItem.attrib['value']
        return cNameToURL
    return dict()

def GetPosInTree(vTree,vElem):
    for i, vItem in enumerate(vTree.iter("*")):
        if vItem == vElem:
            return i

def GetTitle(sURL):
    vRosterPage = requests.get(sURL)
    tree = lxml.html.fromstring(vRosterPage.content)
    #---Get RosterTable
    vRosterPage = requests.get(sURL)
    tree = lxml.html.fromstring(vRosterPage.content)
    vRosterTable = GetRosterTable(tree)
    if vRosterTable is None:
        FRDLog.warning(TM.FnName()+"`Could not find RosterTable for reference.")
        return
    #---
    cPossibleTitles = tree.xpath('//h1')
    vPossibleRosterTitle = None
    iRosterPosInTree = GetPosInTree(tree,vRosterTable)
    iPossibleRosterTitlePosInTree = 0
    for vItem in cPossibleTitles:
        iItemPosInTree = GetPosInTree(tree,vItem)
        if iItemPosInTree < iRosterPosInTree and iItemPosInTree >= iPossibleRosterTitlePosInTree:
                vPossibleRosterTitle = vItem
                iPossibleRosterTitlePosInTree = GetPosInTree(tree,vPossibleRosterTitle)
    if vPossibleRosterTitle is None:
        FRDLog.warning(TM.FnName()+"`Could not find Title.")
        return
    else:
        sRosterTitle = TM.RemoveWhitespace(DigForText(vPossibleRosterTitle)).rstrip("Roster")
    FRDLog.debug("Extracted Title:"+sRosterTitle)
    return sRosterTitle
