from KaggleColumnNameScrapeFunc import *
from KaggleFileNumberAndTypeScrapeFunc import *


def ScrapeFile(Index):

    element = uls[Index]
    fileType = fileTypes[Index]

    # if muliptle files create individual names
    if len(uls) == 1:
        titleElement = driver.find_element(
            By.XPATH, '//*[@id="site-content"]/div[3]/div[2]/div/div[2]/div[1]/h1')
    else:
        titleElement = element.find_element(
            By.TAG_NAME, 'p')
    tablename = '_'.join(titleElement.text.split('.')[0].split(' '))
    print(Index, tablename)

    if fileType == 'csv':

        # already what ScrapeColumnNames is formatted for
        return ScrapeColumnNames(driver, action, tablename)

    elif fileType == 'xlsx':

        # need to click on file in Data Explorer then details
        FirstClick = element.find_element(By.XPATH, './div/div[3]/div')
        action.move_to_element(FirstClick).click().perform()
        time.sleep(2)
        SecondClick = element.find_element(By.XPATH, './ul/ul/div/div[3]/div')
        action.move_to_element(SecondClick).click().perform()
        time.sleep(2)

        # now can run ScrapeColumnNames
        return ScrapeColumnNames(driver, action, tablename)


PATH = "Path to chromedriver"
s = Service(PATH)
driver = webdriver.Chrome(service=s)

url = "https://www.kaggle.com/datasets/arjunprasadsarkhel/2021-olympics-in-tokyo"
driver.get(url)

action = ActionChains(driver)

completed = False

try:
    # find out how many files are on page and their types
    fileNum, fileTypes = ScrapeFileTypes(driver)

    # find list of file elements in Data Explorer
    uls = driver.find_elements(
        By.XPATH, '//*[@id="site-content"]/div[3]/div[5]/div[2]/div[2]/div/div[2]/div[1]/div/ul/ul')

    # go through fileTypes and find indexes that are scrapable
    scrapableTypes = ['csv', 'xlsx']
    scrapableIndexes = []
    for fileIndex in range(fileNum):
        fileType = fileTypes[fileIndex]
        if fileType in scrapableTypes:
            scrapableIndexes.append(fileIndex)

    # scrape each table and add the commands to a list of commands
    commands = []
    for i in scrapableIndexes:
        command = ScrapeFile(i)
        commands.append(command)

    completed = True

except Exception:
    print('Error: ', *sys.exc_info(), sep='\n')

if completed:
    print(*commands, sep='\n\n')


driver.quit()
