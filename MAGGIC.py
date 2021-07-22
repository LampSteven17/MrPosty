import pandas as pd
import time
import re
import numpy as np
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select

############################# MAGGIC ###########################################
def renderScores(driver, datas, url):
    driver.get(url)

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

def WTH(x):
    return {
        1: 0,
        2: 2,
        3: 6,
        4: 8
    }.get(x, 0)
