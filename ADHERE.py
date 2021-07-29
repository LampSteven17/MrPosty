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

############################## ADHERE ##########################################
def renderScores(driver, datas, url):

    driver.get(url)

    rows = datas.shape[0]
    results = []

        # NUMBER OF TIMES TO RUN, CHANGE ROWS TO SOME OTHER NUM FOR TESTS
    for i in range(rows):
        try:
            res = parseADHERE(driver, datas['BUN'][i], datas['BPSYS'][i], datas['CRT'][i])
        except:
            print("TIMEOUT BUG")

        print("ADHERE: " + res)
        results.append(res)

    if (len(results) != rows):
        for i in range (rows - len(results)):
            results.append("")

    datas["ADHERE"] = results

def parseADHERE(driver, BUN, BPSYS, CRT):
    driver.refresh() #SO IT DOESNT KEEP ADDING DATA TO THE PAGE

    if(BUN != "nan" and BPSYS != "nan"):

        if BUN >= 43:
            driver.find_element_by_css_selector('#bun > div:nth-child(2)').click()
        else:
            driver.find_element_by_css_selector('#bun > div:nth-child(1)').click()

        if BPSYS < 115:
            driver.find_element_by_css_selector('#sbp > div:nth-child(2)').click()
        else:
            driver.find_element_by_css_selector('#sbp > div:nth-child(1)').click()


        if (BUN >= 43 and BPSYS < 115 and CRT != "nan"):
            try:
                waiter  = WebDriverWait(driver, 5).until( #TIMEOUT SET TO 15 SECONDS
                    ec.visibility_of_element_located(
                        (By.CSS_SELECTOR, 'div.input:nth-child(3)')
                    )
                )

                if CRT >= 2.75:
                    driver.find_element_by_css_selector('#cr > div:nth-child(2)').click()
                else:
                    driver.find_element_by_css_selector('#cr > div:nth-child(1)').click()

            except:
                #TIMEOUT, WILL RETURN NOTHING EVEN IF SOMETHING EVENTUALLY LOADS
                print("TIMEOUT")
                return ""

        return grabResultsADHERE(driver)

    return ""

def grabResultsADHERE(driver):
    try:
        waiter  = WebDriverWait(driver, 15).until( #TIMEOUT SET TO 15 SECONDS
            ec.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div.result:nth-child(1) > div:nth-child(2)')
            )
        )


        elm = driver.find_element_by_css_selector('div.result:nth-child(1) > div:nth-child(2)')
        resulty = re.sub("[^0-9\-\.]","",elm.text)

        return resulty


    except:
        #TIMEOUT, WILL RETURN NOTHING EVEN IF SOMETHING EVENTUALLY LOADS
        print("TIMEOUT")
        return ""

    return ""
