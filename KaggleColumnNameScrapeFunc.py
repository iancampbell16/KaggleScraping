from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys


def ScrapeColumnNames(driver, action, tableName):

    completed = False

    try:
        # scroll down so elements are clickable
        driver.maximize_window()
        scrollto = driver.find_element(
            By.XPATH, '//*[@id="site-content"]/div[3]/div[5]/div[2]/div[2]/div/div[1]/div')
        driver.execute_script("arguments[0].scrollIntoView()", scrollto)

        # find out if there is an About element on the table
        hasAbout = False
        firstElementText = driver.find_element(
            By.XPATH, '//*[@id="site-content"]/div[3]/div[5]/div[2]/div[2]/div/div[1]/div/div[3]/div[1]').text
        if firstElementText:
            hasAbout = True

        # find deepest element that can be specified by ID
        content = driver.find_element(By.ID, 'site-content')

        # navigate to the deepest element common to the column select button and the column titles
        commonnode = content.find_element(
            By.XPATH, './div[3]/div[5]/div[2]/div[2]/div/div/div')

        # branch1 will go to the element with the column select button
        branch1_1 = commonnode.find_elements(By.XPATH, './*')[1]
        branch1_2 = branch1_1.find_elements(By.XPATH, './*')[0]
        columnSelector = branch1_2.find_elements(By.XPATH, './*')[1]

        # check if all columns are selected
        columnSelector_text = driver.find_element(
            By.XPATH, '//*[@id="site-content"]/div[3]/div[5]/div[2]/div[2]/div/div[1]/div/div[2]/div/div[2]/div/p')
        columnSelector_values = columnSelector_text.text.split(' ')[::2]

        # if all columns arent selected, select all
        if not (columnSelector_values[0] == columnSelector_values[1]):

            # click on columnSelector
            action.move_to_element(columnSelector).click().perform()

            # wait to be able to find select all
            columnSelectAll = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/main/div/div/div[4]/div[3]/div[5]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div/div'))
            )

            # click on columnSelectAll
            action.move_to_element(columnSelectAll).click().perform()

            # find the apply button
            spans = columnSelector.find_elements(By.TAG_NAME, 'span')
            applyButton = spans[-1]

            # click on applyButton
            action.move_to_element(applyButton).click().perform()

            # wait to render
            time.sleep(2)

        # branch2 will go to the element with the column titles
        branch2_1 = commonnode.find_elements(By.XPATH, './*')[2]
        if hasAbout:
            branch2_2 = branch2_1.find_elements(By.XPATH, './*')[3]
        else:
            branch2_2 = branch2_1.find_elements(By.XPATH, './*')[2]
        branch2_3 = branch2_2.find_elements(By.XPATH, './*')[0]

        # make list of the elements which contain desired info
        elementsList = branch2_3.find_elements(By.XPATH, './*')
        columns = []
        for element in elementsList:
            child = element.find_element(By.XPATH, './*')
            columnType = child.find_element(By.TAG_NAME, 'i').text
            columnName = child.find_element(By.TAG_NAME, 'span').text
            columns.append((columnName, columnType))

        completed = True

    except Exception:
        print('Error: ', *sys.exc_info(), sep='\n')

    if completed:

        # arrange in form of sql command
        varc = ['flag', 'calendar_today', 'text_format', 'vpn_key', 'link']
        floa = ['navigation', 'grid_3x3']
        sqlCommand = ''
        for column in columns:
            if sqlCommand:
                sqlCommand += ', '
            sqlCommand += ''.join(column[0].split('/')[0].split(' '))
            if column[1] in varc:
                sqlCommand += ' VARCHAR(255)'
            elif column[1] in floa:
                sqlCommand += ' FLOAT'
            else:
                print('New Type!')
        sqlCommand = 'CREATE TABLE ' + tableName + ' (' + sqlCommand + ');'
        return sqlCommand

    else:

        return ''


if __name__ == '__main__':

    PATH = "Path to chromedriver"
    s = Service(PATH)
    driver = webdriver.Chrome(service=s)

    url = "https://www.kaggle.com/datasets/programmerrdai/co2-levels-globally-from-fossil-fuels"
    driver.get(url)

    action = ActionChains(driver)

    titleElement = driver.find_element(
        By.XPATH, '//*[@id="site-content"]/div[3]/div[2]/div/div[2]/div[1]/h1')
    tablename = '_'.join(titleElement.text.split(' '))

    print(ScrapeColumnNames(driver, action, tablename))

    driver.quit()
