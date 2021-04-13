from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import numpy as np
import time
from datetime import date
import math
from selenium.webdriver.common.keys import Keys

PROCESS_FN = False
PROCESS_VAL = False
PROCESS_CSGO = False
PROCESS_OW = False
PROCESS_AL = True


FN_DPI = 4
FN_SENS_X = 5
FN_SENS_Y = 6
FN_TARGETING = 7
FN_SCOPED = 8

VAL_EDPI = 7
VAL_SCOPED_SENS = 8

CSGO_EDPI = 8

OW_EDPI = 8

AL_DPI = 4
AL_SENS = 6
AL_SENS_MUL = 7

VAL_FILE_ID = "val_sens_"
FN_FILE_ID = "fn_sens_"
CSGO_FILE_ID = "csgo_sens_"

DATE = "{:0>2d}-{:0>2d}-{}".format(date.today().month, date.today().day, date.today().year)

CSGO_URL = 'https://prosettings.net/cs-go-pro-settings-gear-list/'
VAL_URL = 'https://prosettings.net/valorant-pro-settings-gear-list/'
FN_URL = 'https://prosettings.net/best-fortnite-settings-list/'
OW_URL = 'https://prosettings.net/overwatch-pro-settings-gear-list/'
AL_URL = 'https://prosettings.net/apex-legends-pro-settings-gear-list/'

FN_SENS_URL = 'https://gamepros.gg/mouse-sensitivity-converter/fortnite'
VAL_SENS_URL = 'https://gamepros.gg/mouse-sensitivity-converter/valorant'
CSGO_SENS_URL = 'https://gamepros.gg/mouse-sensitivity-converter/csgo'
OW_SENS_URL = 'https://gamepros.gg/mouse-sensitivity-converter/overwatch'
AL_SENS_URL = 'https://gamepros.gg/mouse-sensitivity-converter/apex-legends'

INPIT_DPI_STANDARD = '/html/body/div/div/div[1]/div/div[1]/div/div[2]/div/div/div[1]/input[1]'
INPUT_DPI_XPATH_VAL = '/html/body/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[1]/input[1]'
INPUT_DPI_XPATH_FN = INPIT_DPI_STANDARD
INPUT_DPI_XPATH_CSGO = INPIT_DPI_STANDARD
INPUT_DPI_XPATH_OW = INPIT_DPI_STANDARD
INPUT_DPI_XPATH_AL = INPIT_DPI_STANDARD

SHEET_XPATH_STANDARD = '/html/body/div[1]/div/div[1]/div/article/div/div/div/div/div/div/div[3]/div/div/div/table/tbody/*'
SHEET_XPATH_AL = '/html/body/div[1]/div/div[1]/div/article/div/div/div/div[2]/div/div/div/div/div/div/table/tbody/*'


INPUT_SENS_STANDARD = '/html/body/div/div/div[1]/div/div[1]/div/div[2]/div/div/div[1]/input[2]'
INPUT_SENS_XPATH_FN = INPUT_SENS_STANDARD
INPUT_SENS_XPATH_VAL = '/html/body/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[1]/input[2]'
INPUT_SENS_XPATH_CSGO = INPUT_SENS_STANDARD
INPUT_SENS_XPATH_OW = INPUT_SENS_STANDARD
INPUT_SENS_XPATH_AL = INPUT_SENS_STANDARD

INPUT_CM_STANDARD = '/html/body/div/div/div[1]/div/div[1]/div/div[2]/div/div/div[3]/div[2]/div[3]/input'
INPUT_CM_XPATH_FN = INPUT_CM_STANDARD
INPUT_CM_XPATH_VAL = '/html/body/div/div/div[2]/div/div[1]/div/div[2]/div/div/div[3]/div[2]/div[3]/input'
INPUT_CM_XPATH_CSGO = INPUT_CM_STANDARD
INPUT_CM_XPATH_OW = INPUT_CM_STANDARD
INPUT_CM_XPATH_AL = INPUT_CM_STANDARD

def indices_to_xpath_standard(row, column):
    return '/html/body/div[1]/div/div[1]/div/article/div/div/div/div/div/div/div[3]/div/div/div/table/tbody/tr[{}]/td[{}]'.format(row, column)
def indices_to_xpath_al(row, column):
    return "/html/body/div[1]/div/div[1]/div/article/div/div/div/div[2]/div/div/div/div/div/div/table/tbody/tr[{}]/td[{}]".format(row, column)

def get_text(browser, row, column, indices_to_xpath):
    element = None
    element_xpath = indices_to_xpath(row, column)
    while not element:
        try:
            element = browser.find_element_by_xpath(element_xpath)
        except NoSuchElementException:
            print("element not found; trying again in 2 seconds")
            time.sleep(2)
    return element.text

def set_element(browser, xpath, input):
    element = None
    while not element:
        try:
            element = browser.find_element_by_xpath(xpath)
        except NoSuchElementException:
            print("element not found; trying again in 2 seconds")
            time.sleep(2)
    element.send_keys(Keys.CONTROL, "a")
    element.send_keys(input)
    return element


def wait_load_elements(xpath):
    num_elements = 0
    while num_elements == 0:
        elements = browser.find_elements_by_xpath(xpath)

        num_elements = len(elements)
        print("element array not found; trying again in 2 seconds")
        time.sleep(2)
    return num_elements

def get_all_num(browser, error_message, element_type, pre_process = None, indices_to_xpath = None):
    out_list = []
    for i in range(1, num_elements):
        try:
            text = get_text(browser, i, element_type, indices_to_xpath)
            if (pre_process != None):
                text = pre_process(text)

            val = float(text)
        except ValueError:
            print(error_message + "error at:" + str(i))
            print("value of: " + text)
            val = math.nan
        out_list.append(val)
    return out_list

def clean(str):
    return str.replace('%', '').replace(',', '')


browser = webdriver.Chrome()
def edpi_to_cm(edpis, dpi_xpath, cm_xpath):
    out = []
    for edpi in edpis:
        set_element(browser, dpi_xpath, str(edpi))

        element = None
        while not element:
            try:
                element = browser.find_element_by_xpath(cm_xpath)
            except NoSuchElementException:
                print("CM element not found; trying again in 2 seconds")
                time.sleep(2)

        value = float(element.get_attribute("value"))
        out.append(value)
    return out

if (PROCESS_AL):
    browser.get(AL_URL)
    browser.maximize_window()
    num_elements = wait_load_elements(SHEET_XPATH_AL)
    dpis = get_all_num(browser, "al dpi ", AL_DPI, clean, indices_to_xpath_al)
    sens = get_all_num(browser, "al sens ", AL_SENS, clean, indices_to_xpath_al)
    sens_mul = get_all_num(browser, "ow edpi ", AL_SENS_MUL, clean, indices_to_xpath_al)

    num_entries = len(dpis)
    print("num al edpis: " + str(num_entries))

    edpis = []
    for (_dpi, _sens, _sens_mul) in zip(dpis, sens, sens_mul):
        if (not math.isnan(_dpi) and not math.isnan(_sens) and not math.isnan(_sens_mul)):
            edpis.append(_dpi * _sens * _sens_mul)

    # convert to cm
    browser.get(AL_SENS_URL)
    set_element(browser, INPUT_SENS_XPATH_AL, "1")

    edpis_cm = np.array(edpi_to_cm(edpis, INPUT_DPI_XPATH_AL, INPUT_CM_XPATH_AL))
    np.savetxt("al_sens.csv", edpis_cm, delimiter=",")

if (PROCESS_OW):
    browser.get(OW_URL)
    browser.maximize_window()
    num_elements = wait_load_elements(SHEET_XPATH_STANDARD)

    edpis = get_all_num(browser, "ow edpi ", OW_EDPI, clean, indices_to_xpath_standard)
    num_edpis = len(edpis)
    print("num ow edpis: " + str(num_edpis))

    # convert to cm
    browser.get(OW_SENS_URL)
    set_element(browser, INPUT_SENS_XPATH_OW, "1")

    edpis_cm = np.array(edpi_to_cm(edpis, INPUT_DPI_XPATH_OW, INPUT_CM_XPATH_OW))
    np.savetxt("ow_sens.csv", edpis_cm, delimiter=",")

if (PROCESS_CSGO):
    browser.get(CSGO_URL)
    browser.maximize_window()
    num_elements = wait_load_elements(SHEET_XPATH_STANDARD)

    edpis = get_all_num(browser, "csgo edpi ", CSGO_EDPI, clean, indices_to_xpath_standard)
    num_edpis = len(edpis)
    print("num csgo edpis: " + str(num_edpis))

    # convert to cm
    browser.get(CSGO_SENS_URL)
    set_element(browser, INPUT_SENS_XPATH_CSGO, "1")

    edpis_cm = np.array(edpi_to_cm(edpis, INPUT_DPI_XPATH_CSGO, INPUT_CM_XPATH_CSGO))
    np.savetxt("csgo_sens.csv", edpis_cm, delimiter=",")

if (PROCESS_VAL):
    browser.get(VAL_URL)
    browser.maximize_window()
    num_elements = wait_load_elements(SHEET_XPATH_STANDARD)

    edpis = get_all_num(browser, "edpi ", VAL_EDPI, clean, indices_to_xpath_standard)
    num_edpis = len(edpis)
    print("num val edpis: " + str(num_edpis))

    # convert to cm
    browser.get(VAL_SENS_URL)
    set_element(browser, INPUT_SENS_XPATH_VAL, "1")

    edpis_cm = np.array(edpi_to_cm(edpis, INPUT_DPI_XPATH_VAL, INPUT_CM_XPATH_VAL))
    np.savetxt("val_sens.csv", edpis_cm, delimiter=",")

if (PROCESS_FN):
    browser.get(FN_URL)
    browser.maximize_window()
    num_elements = wait_load_elements(SHEET_XPATH_STANDARD)

    dpis = get_all_num(browser, "dpi ", FN_DPI, clean, indices_to_xpath_standard)
    num_dpis = len(dpis)
    print("num_dpis " + str(num_dpis))

    sens_x = get_all_num(browser, "sens_x ", FN_SENS_X, clean, indices_to_xpath_standard)
    sens_y = get_all_num(browser, "sens_y ", FN_SENS_Y, clean, indices_to_xpath_standard)
    sens_targeting = get_all_num(browser, "targeting ", FN_TARGETING, clean, indices_to_xpath_standard)
    sens_scoped = get_all_num(browser, "scoped ", FN_SCOPED, clean, indices_to_xpath_standard)

    print("processing edpis_x")
    edpis_x = []
    for (_dpi, _sens) in zip(dpis, sens_x):
        if (not math.isnan(_dpi) and not math.isnan(_sens)):
            edpis_x.append(_dpi * _sens)
            print("dpi_x: {}\tsens:{}".format(_dpi, _sens))

    print("processing edpis_y")
    edpis_y = []
    for (_dpi, _sens) in zip(dpis, sens_y):
        if (not math.isnan(_dpi) and not math.isnan(_sens)):
            edpis_y.append(_dpi * _sens)

    print("processing edpis_x_targeting")
    edpis_x_targeting = []
    for (_dpi, _sens, _sens_multiplier) in zip(dpis, sens_x, sens_targeting):
        if (not math.isnan(_dpi) and not math.isnan(_sens) and not math.isnan(_sens_multiplier)):
            edpis_x_targeting.append(_dpi * _sens * _sens_multiplier/100)

    print("processing edpis_y_targeting")
    edpis_y_targeting = []
    for (_dpi, _sens, _sens_multiplier) in zip(dpis, sens_y, sens_targeting):
        if (not math.isnan(_dpi) and not math.isnan(_sens) and not math.isnan(_sens_multiplier)):
            edpis_y_targeting.append(_dpi * _sens * _sens_multiplier/100)
            
    print("processing edpis_x_scoped")
    edpis_x_scoped = []
    for (_dpi, _sens, _sens_multiplier) in zip(dpis, sens_x, sens_scoped):
        if (not math.isnan(_dpi) and not math.isnan(_sens) and not math.isnan(_sens_multiplier)):
            edpis_x_scoped.append(_dpi * _sens * _sens_multiplier/100)

    print("processing edpis_y_scoped")
    edpis_y_scoped = []
    for (_dpi, _sens, _sens_multiplier) in zip(dpis, sens_y, sens_scoped):
        if (not math.isnan(_dpi) and not math.isnan(_sens) and not math.isnan(_sens_multiplier)):
            edpis_y_scoped.append(_dpi * _sens * _sens_multiplier/100)

    # convert to cm
    browser.get(FN_SENS_URL)
    set_element(browser, INPUT_SENS_XPATH_FN, "1")

    edpis_cm_x = np.array(edpi_to_cm(edpis_x, INPUT_DPI_XPATH_FN, INPUT_CM_XPATH_FN))
    np.savetxt("fortnite_x_sens.csv", edpis_cm_x, delimiter=",")

    edpis_cm_y = np.array(edpi_to_cm(edpis_y, INPUT_DPI_XPATH_FN, INPUT_CM_XPATH_FN))
    np.savetxt("fortnite_y_sens.csv", edpis_cm_y, delimiter=",")

    edpis_cm_x_targeting = np.array(edpi_to_cm(edpis_x_targeting, INPUT_DPI_XPATH_FN, INPUT_CM_XPATH_FN))
    np.savetxt("fortnite_x_sens_targeting.csv", edpis_cm_x_targeting, delimiter=",")

    edpis_cm_y_targeting = np.array(edpi_to_cm(edpis_y_targeting, INPUT_DPI_XPATH_FN, INPUT_CM_XPATH_FN))
    np.savetxt("fortnite_y_sens_targeting.csv", edpis_cm_y_targeting, delimiter=",")

    edpis_cm_x_scoped = np.array(edpi_to_cm(edpis_x_scoped, INPUT_DPI_XPATH_FN, INPUT_CM_XPATH_FN))
    np.savetxt("fortnite_x_sens_scoped.csv", edpis_cm_x_scoped, delimiter=",")

    edpis_cm_y_scoped = np.array(edpi_to_cm(edpis_y_scoped, INPUT_DPI_XPATH_FN, INPUT_CM_XPATH_FN))
    np.savetxt("fortnite_y_sens_scoped.csv", edpis_cm_y_scoped, delimiter=",")










