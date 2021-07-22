# Created by Steven Lamp 07/05/21
# MAKE SURE Mr.Posty is running in the same directory as the csv you wish to use

import pandas as pd
import time
import re
import numpy as np
from selenium import webdriver

import GWTG
import MAGGIC
import ADHERE

# UNCOMMENT FOR SHF APPPLICATION ###############################################
#import SHF
# MAY NEED TO MAKE EDITS IN SHF.py (INCLUDED IN REPO) ##########################



# ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !
# PUT NAME OF FILE HERE ########################################################
FILENAME = "ESCAPEAllDataSingleValue.csv"
################################################################################

# PUT DRIVER FOR BOWSER ON COMPUTER HERE #######################################
# FIREFOX (DEFAULT INCLUDED IN REPO)
DRIVER = webdriver.Firefox() #DRIVER = webdriver.Firefox(executable_path=r'\my\path\to\geckodriver')
# CHOOSE ONLY 1, FIREFOX OR CHROME
# CHROME
#DRIVER = webdriver.Chrome(executable_path=r'\my\path\to\chromedriver')
################################################################################
# ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !


# URL's, SHOULDNT NEED TO BE CHANGED UNLESS URL CHANGES ########################
gwtgURL = "https://www.mdcalc.com/gwtg-heart-failure-risk-score"
maggicURL = "http://www.heartfailurerisk.org/"
adhereURL = "https://www.mdcalc.com/acute-decompensated-heart-failure-national-registry-adhere-algorithm"









def main():

    daty = getDataFromCsv()

# ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !
# UNCOMMENT FOR GWTG ###########################################################
    GWTG.renderScores(DRIVER, daty, gwtgURL) # DEFAULT SET TO RUN ON GWTG

# UNCOMMENT FOR MAGGIC #########################################################
    #MAGGIC.renderScores(DRIVER, daty, maggicURL)

# UNCOMMENT FOR ADHERE #########################################################
    #ADHERE.renderScores(DRIVER, daty, adhereURL)



    DRIVER.quit()
# END OF SELENIUM OPS ##########################################################

# BEGIN APP-BASED OPS#########################################################
#####UNCOMMENT FOR SHF##########################################################
    #SHF.renderScores(daty) #extra touchy
# ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !

    print(daty)
    daty.to_csv("OUTFILE.csv", index = False)

def getDataFromCsv():
    frame = pd.read_csv(FILENAME, header = 0)
    return frame.replace(r'^\s*$', np.nan, regex=True)


if __name__ == "__main__":
    main()
