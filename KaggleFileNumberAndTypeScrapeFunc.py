from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import sys


def ScrapeFileTypes(driver):

    completed = False

    try:
        # scroll down so elements are clickable
        driver.maximize_window()
        scrollto = driver.find_element(
            By.XPATH, '//*[@id="site-content"]/div[3]/div[5]/div[2]/div[2]/div/div[1]/div')
        driver.execute_script("arguments[0].scrollIntoView()", scrollto)

        # make list of uls in filesListElement and record length of list (number of files)
        uls = driver.find_elements(
            By.XPATH, '//*[@id="site-content"]/div[3]/div[5]/div[2]/div[2]/div/div[2]/div[1]/div/ul/ul')
        numberOfFiles = len(uls)

        # find text of p class in each ul
        types = []
        for ul in uls:
            fileType = ul.find_element(By.TAG_NAME, 'p').text.split('.')[-1]
            types.append(fileType)

        completed = True

    except Exception:
        print('Error: ', *sys.exc_info(), sep='\n')

    if completed:

        return [numberOfFiles, types]

    else:

        return [0, []]


if __name__ == '__main__':
    PATH = "/Users/iancampbell/Documents/WebDriver/chromedriver"
    s = Service(PATH)
    driver = webdriver.Chrome(service=s)

    url = "https://www.kaggle.com/datasets/programmerrdai/air-pollution"
    driver.get(url)

    print(*ScrapeFileTypes(driver), sep='\n')

    driver.quit()
