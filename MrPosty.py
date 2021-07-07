# Created by Steven Lamp 07/05/21
# MAKE SURE Mr.Posty is running in the same directory as the csv you wish to use

import pandas as pd
import time
import re
import requests
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# PUT NAME OF FILE HERE ########################################################
FILENAME = "ESCAPEAllDataSingleValue.csv"
################################################################################

GWTG = "https://www.mdcalc.com/gwtg-heart-failure-risk-score"

def main():

    daty = getDataFromCsv()

    renderScoresGWTG(daty)

    print(daty)
    daty.to_csv("OUTFILE.csv")





def getDataFromCsv():
    frame = pd.read_csv(FILENAME, header = 0)
    return frame.replace(r'^\s*$', np.nan, regex=True)


def renderScoresGWTG(datas):
    driver = webdriver.Firefox() #SWITCH TO: Chrome() IF NEEDED
    driver.get(GWTG)

    rows = datas.shape[0]
    results = []

# NUMBER OF TIMES TO RUN, CHANGE ROWS TO SOME OTHER NUM FOR TESTS ##############
    for i in range(12):
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

def grabResults(driver):
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

        return grabResults(driver)


    return ""






if __name__ == "__main__":
    main()
