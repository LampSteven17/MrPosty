import pandas as pd
import time
import re
import numpy as np
import os
from ahk import AHK as ahk
from ahk.window import Window
import pyperclip
import pyscreenshot as ps
import pytesseract
from PIL import Image
import cv2

# PUT SHF EXECUTABLE LOCATION HERE #############################################
SHF = "C:/Program Files (x86)/University of Washington/SHFM/SHFM.exe"
################################################################################

# PUT AHK EXECUTABLE HERE ######################################################
ahk = ahk(executable_path='C:/Program Files/AutoHotkey/AutoHotkey.exe')
################################################################################

# PUT PYTESSERACT EXECUTABLE HERE ##############################################
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
################################################################################

#CONFIG FILE TO PARSE ONLY DIGITS, MAY NEED TO BE CHANGED
CONFIG = 'outputbase digys'

############################## SHF #############################################
def renderScores(datas):
    os.startfile(SHF)

    rows = datas.shape[0]
    SHF1 = []
    SHF2 = []
    SHF5 = []


############## CHANGE FROM ROWS IF NEEDED
    for i in range(rows):
        win = ahk.find_window(title=b'Seattle Heart Failure Model Calculator')

        res = parseSHF(str(datas['Age'][i]),
                      (datas['Gender'][i] - 1),
                      int(floatNan(datas['NYHA'][i])),
                      str(datas['Wt'][i]),
                      str(datas['EjF'][i]),
                      str(datas['BPSYS'][i]),
                      datas['ISCH'][i],
                      datas['ACE'][i],
                      datas['BET'][i],
                      str(datas['FurosemideDse'][i]),
                      str(datas['Bumetanide'][i]),
                      str(datas['Torsemide'][i]),
                      str(datas['HGB'][i]),
                      str(datas['WBC'][i]),
                      str(datas['URIC'][i]),
                      str(datas['TOTChol'][i]),
                      str(datas['SOD'][i]),
                      datas['PACE'][i],
                      datas['ICD'][i]

                      )

        print("SHF1: " + res[0] + " SHF2: " + res[1] + " SHF5: " + res[2])

        SHF1.append(res[0])
        SHF2.append(res[1])
        SHF5.append(res[2])



    if (len(SHF1) != rows):
        for i in range (rows - len(SHF1)):
            SHF1.append("")
            SHF2.append("")
            SHF5.append("")

    datas["SHF1"] = SHF1
    datas["SHF2"] = SHF2
    datas["SHF5"] = SHF5

def nanCheck(var):
    return var if var != "nan" else ""

def floatNan(var):
    return 0 if np.isnan(var) else var

def switchNYHA(x):
    return {
        1: 468,
        2: 487,
        3: 523,
        4: 563
    }.get(x, 563)

def parseSHF(AGE, SEX, NYHA, WT, EF, BP, ISCH, ACE, BET, FUR, BUM, TOR, HGB, LYM, URIC, CHOL, SOD, PACE, ICD):
    AGE=nanCheck(AGE) #WHYYYYYYYYYYY FIX THIS DEAR HEAVENS
    SEX=nanCheck(SEX)
    NYHA=nanCheck(NYHA)
    WT=nanCheck(WT)
    EF=nanCheck(EF)
    BP=nanCheck(BP)
    ISCH=nanCheck(ISCH)
    ACE=nanCheck(ACE)
    BET=nanCheck(BET)
    FUR=nanCheck(FUR)
    BUM=nanCheck(BUM)
    TOR=nanCheck(TOR)
    HGB=nanCheck(HGB)
    LYM=nanCheck(LYM)
    URIC=nanCheck(URIC)
    CHOL=nanCheck(CHOL)
    SOD=nanCheck(SOD)
    PACE=nanCheck(PACE)
    ICD=nanCheck(ICD)

# ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !
# PIXEL ADJUSMENTS FOR SHF, ADJUST NUMBERS BELOW IF NOT CLICKING RIGHT AREAS ###
    ahk.click(939, 648) #RESETS EVERYTHING TO DEFAULTS


    ahk.double_click(160, 356)
    ahk.type(AGE)

    ahk.click(189, 403)
    ahk.click(175, (442 if SEX else 426))

    ahk.click(189,439)
    ahk.click(172,switchNYHA(NYHA))

    ahk.double_click(163, 483)
    ahk.type(WT)

    ahk.double_click(170, 521)
    ahk.type(EF)

    ahk.double_click(167, 561)
    ahk.type(BP)

    if not ISCH:
        ahk.click(47, 607)

    if not ACE:
        ahk.click(249, 355)

    if BET:
        ahk.click(249,401)

    ahk.double_click(557, 355)
    ahk.type(FUR)

    ahk.double_click(550, 400)
    ahk.type(BUM)

    ahk.double_click(554, 443)
    ahk.type(TOR)

    ahk.double_click(858,360)
    ahk.type(HGB)

    ahk.double_click(851, 403)
    ahk.type(LYM)

    ahk.double_click(848, 441)
    ahk.type(URIC)

    ahk.double_click(857, 481)
    ahk.type(CHOL)

    ahk.double_click(857, 481)
    ahk.type(SOD)

    if PACE:
        ahk.click(949,397)

    if ICD:
        ahk.click(949,440)
# ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !

    return grabResultsSHF()

def grabResultsSHF():

# ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !
#MORE PIXEL ADJUSTMENTS -> X1,Y1,X2,Y2 TO FORM BOX AROUND RESULTS TO GRAB IMAGE
    cords = [[156,200,204,235],[229,200,277,235],[302,200,350,235]]
# ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !
    results=[]

    for i in range(3):

        shot = ps.grab(bbox=cords[i])
        shot.save("results.png")



        img = cv2.imread('results.png')
        scale = 2
        img = cv2.resize(img, (img.shape[1]*scale,img.shape[0]*scale), interpolation=cv2.INTER_AREA)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        kernel = np.ones((3,3), np.uint8)


        CONFIG = '--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789%'

        #SEE THE IMAGE IT CREATES
        #cv2.imshow('FIXED', img)
        #cv2.waitKey(0)

        cv2.imwrite("results.png", img)

        var = pytesseract.image_to_string(Image.open('results.png'),config=CONFIG)

        results.append(re.sub("[^0-9\-\.]","",var))


    #print("Y1: " + results[0] + " Y2: " + results[1] + " Y3: " + results[2])
    return results
