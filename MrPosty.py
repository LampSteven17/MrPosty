# Created by Steven Lamp 07/05/21
# MAKE SURE Mr.Posty is running in the same directory as the csv you wish to use

import pandas as pd
import time
import re
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
import os
from ahk import AHK as ahk

# PUT NAME OF FILE HERE ########################################################
FILENAME = "AllDataBEST.csv"
################################################################################

GWTG = "https://www.mdcalc.com/gwtg-heart-failure-risk-score"
MAGGIC = "http://www.heartfailurerisk.org/"
SHF = "C:/Program Files (x86)/University of Washington/SHFM/SHFM.exe"
ahk = ahk(executable_path='C:/Program Files/AutoHotkey/AutoHotkey.exe')


def main():

    daty = getDataFromCsv()

    #renderScoresGWTG(daty)
    #renderScoresMAGGIC(daty)
    renderScoresSHF(daty)

    print(daty)
    daty.to_csv("OUTFILE.csv", index = False)#SO IT DOESNT PRINT A COULMN WITH 1-8000

def getDataFromCsv():
    frame = pd.read_csv(FILENAME, header = 0)
    return frame.replace(r'^\s*$', np.nan, regex=True)

############################## SHF #############################################

def renderScoresSHF(datas):
    os.startfile(SHF)

    win = ahk.find_window(title=b'Seattle Heart Failure Model Calculator')

    rows = datas.shape[0]
    SHF1 = []
    SHF2 = []
    SHF5 = []

############## CHANGE FROM ROWS IF NEEDED
    for i in range(10):

        res = parseSHF(str(datas['Age'][i]),
                      (datas['Gender'][i] - 1),
                      int(datas['NYHA'][i]),
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
                      datas['PACE'][i]





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

def switchNYHA(x):
    return {
        1: 468,
        2: 487,
        3: 523,
        4: 563
    }.get(x, 563)

def parseSHF(AGE, SEX, NYHA, WT, EF, BP, ISCH, ACE, BET, FUR, BUM, TOR, HGB, LYM, URIC, CHOL, SOD, PACE):
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

    print(PACE)


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


















    return ["","",""]




############################# MAGGIC ###########################################
def WTH(x):
    return {
        1: 0,
        2: 2,
        3: 6,
        4: 8
    }.get(x, 0)

def renderScoresMAGGIC(datas):
    driver = webdriver.Firefox() #SWITCH TO: Chrome() IF NEEDED
    driver.get(MAGGIC)

    #CLICK THE ACCEPT BUTTON: #accept-terms
    driver.find_element_by_css_selector('#accept-terms').click()


    rows = datas.shape[0]
    scores = []
    Y1 = []
    Y3 = []

############## CHANGE FROM ROWS IF NEEDED
    for i in range(rows):

        res = parseMAGGIC(driver,
                          str(datas['Age'][i]),
                          (datas['Gender'][i] - 1),
                          datas['DIAB'][i],
                          datas['COPD'][i],
                          (0 if datas['SMOKING'][i] < 1 else 1),
                          str(WTH(datas['NYHA'][i])),
                          datas['BET'][i],
                          datas['ACE'][i],
                          str(datas['EjF'][i]),
                          str(datas['CRT'][i] * 88.4),
                          str(datas['BPSYS'][i]),
                          str(datas['BMI'][i])
                          )

        print("MAGGIC: " + res[0] + " Y1: " + res[1] + " Y3: " + res[2])

        scores.append(res[0])
        Y1.append(res[1])
        Y3.append(res[2])



    driver.quit()
    if (len(scores) != rows):
        for i in range (rows - len(scores)):
            scores.append("")
            Y1.append("")
            Y3.append("")

    datas["MAGGIC"] = scores
    datas["Y1"] = Y1
    datas["Y3"] = Y3


def parseMAGGIC(driver, AGE, SEX, DIAB, COPD, SMOKE, NYHA, BB, ACE, EJF, CRT, BPSYS, BMI):
    driver.refresh() #SO IT DOESNT KEEP ADDING DATA TO THE PAGE

    #this is lowkey a nightmare need to fix asp.
    if (AGE != "nan" and SEX != "nan" and DIAB != "nan" and SMOKE != "nan"
        and NYHA != "nan" and BB != "nan" and ACE != "nan" and EJF != "nan"
        and CRT != "nan" and BPSYS != "nan" and BMI != "nan"):

        driver.find_element_by_css_selector('#age').send_keys(AGE)

        #MUST CLICK BEFORE ENTERING GENDER STUPID DROPDOWN ANIMATIONS
        driver.find_element_by_css_selector('#diabetic-yes' if DIAB else '#diabetic-no').click()
        time.sleep(.25)

        sexy = Select(driver.find_element_by_css_selector('#gender'))
        sexy.select_by_value('1' if SEX else '0')

        driver.find_element_by_css_selector('#copd-yes' if COPD else '#copd-no').click()
        ########## ALL YESS SINCE NO CLOUMN IN DATA #####################
        driver.find_element_by_css_selector('#heart-failure-yes').click()
        #################################################################
        driver.find_element_by_css_selector('#smoker-yes' if SMOKE else '#smoker-no' ).click()

        nyhaSel = Select(driver.find_element_by_css_selector('#nyha'))
        nyhaSel.select_by_value(NYHA)

        driver.find_element_by_css_selector('#beta-blockers-yes' if BB else '#beta-blockers-no').click()
        driver.find_element_by_css_selector('#ace-yes' if ACE else '#ace-no' ).click()
        driver.find_element_by_css_selector('#ejection-fraction').send_keys(EJF)
        driver.find_element_by_css_selector('#creatinine').send_keys(CRT)
        driver.find_element_by_css_selector('#bp').send_keys(BPSYS)
        driver.find_element_by_css_selector('#bmi').send_keys(BMI)

        return grabResultsMAGGIC(driver)


    return ["","",""]


def grabResultsMAGGIC(driver):

    driver.find_element_by_css_selector('#calculate').click()

    try:
        waiter  = WebDriverWait(driver, 15).until( #TIMEOUT SET TO 15 SECONDS
            ec.visibility_of_element_located(
                (By.CSS_SELECTOR, '#score-result')
            )
        )

        resulty = []
        scoresToGrab = ['#score-result', '#risk-1-result', '#risk-3-result']

        for score in scoresToGrab:
            tempy = driver.find_element_by_css_selector(score)
            r = re.sub("[^0-9\-\.]","",tempy.text)
            resulty.append(r)

        return resulty


    except:
        #TIMEOUT, WILL RETURN NOTHING EVEN IF SOMETHING EVENTUALLY LOADS
        print("TIMEOUT")
        return ["","",""]







############################## GWTG ############################################
def renderScoresGWTG(datas):
    driver = webdriver.Firefox() #SWITCH TO: Chrome() IF NEEDED
    driver.get(GWTG)

    rows = datas.shape[0]
    results = []

################ NUMBER OF TIMES TO RUN, CHANGE ROWS TO SOME OTHER NUM FOR TESTS
    for i in range(rows):
        res = parseGWTG(driver, str(datas['BPSYS'][i]),
                                   str(datas['BUN'][i]),
                                   str(datas['SOD'][i]),
                                   str(datas['Age'][i]),
                                   str(datas['HR'][i]),
                                   datas['COPD'][i],
                                   (datas['Race'][i] - 1)
                        )

        print("GWTG: " + res)
        results.append(res)



    driver.quit()
    if (len(results) != rows):
        for i in range (rows - len(results)):
            results.append("")

    datas["GWTG"] = results

def grabResultsGWTG(driver):
    try:
        waiter  = WebDriverWait(driver, 15).until( #TIMEOUT SET TO 15 SECONDS
            ec.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div.result:nth-child(1) > h2:nth-child(1)')
            )
        )


        elm = driver.find_element_by_css_selector('div.result:nth-child(1) > h2:nth-child(1)')
        resulty = re.sub("[^0-9\-]","",elm.text)

        return resulty


    except:
        #TIMEOUT, WILL RETURN NOTHING EVEN IF SOMETHING EVENTUALLY LOADS
        print("TIMEOUT")
        return ""


def parseGWTG(driver, BPSYS, BUN, SOD, AGE, HR, COPD, BLACK):
    driver.refresh() #SO IT DOESNT KEEP ADDING DATA TO THE PAGE

    if (BPSYS != "nan" and BUN != "nan" and SOD != "nan" and AGE != "nan" and HR != "nan"):
        driver.find_element_by_id("input_sbp").send_keys(BPSYS)
        driver.find_element_by_id("input_bun").send_keys(BUN)
        driver.find_element_by_id("input_na").send_keys(SOD)
        driver.find_element_by_id("input_age").send_keys(AGE)
        driver.find_element_by_id("input_hr").send_keys(HR)

        #COPD DEFAULTS TO NO
        copdBtn = driver.find_element_by_css_selector('#copd > div:nth-child(1)')

        if COPD:
            copdBtn = driver.find_element_by_css_selector('#copd > div:nth-child(2)')

        driver.execute_script("arguments[0].scrollIntoView();", copdBtn)
        ActionChains(driver).move_to_element(copdBtn).click().perform()



        #BLACK DEFAULTS TO NO
        blackBtn = driver.find_element_by_css_selector('#black > div:nth-child(1)')

        if BLACK:
            blackBtn = driver.find_element_by_css_selector('#black > div:nth-child(2)')


        driver.execute_script("arguments[0].scrollIntoView();", blackBtn)
        ActionChains(driver).move_to_element(blackBtn).click().perform()

        return grabResultsGWTG(driver)


    return ""






if __name__ == "__main__":
    main()
