from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import inquirer

attempt_login = True

def login():
    sleep(2)

    questions = [
       inquirer.Text('username', message='Enter your Self Serve username'),
       inquirer.Password('password', message='Enter your password')
    ]

    answers = inquirer.prompt(questions)

    driver.find_element(By.ID, "userLoginId").send_keys(answers['username'])
    driver.find_element(By.ID, "userPassword").send_keys(answers['password'])

    sleep(2)

    driver.find_element(By.ID, "ok").click()




options = Options()
options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=options)

driver.get('https://is-teams.aisd.net/selfserve/EntryPointHomeAction.do?parent=false')

driver.find_element(By.ID, "ok").click()

while(attempt_login == True):
    login()
    sleep(2)
    a = [value.text for value in driver.find_elements(By.CLASS_NAME, "error")]
    if(len(a) >= 3):
        print("\n[!] Login failed. Please try again.\n")
        driver.find_element(By.ID, "userLoginId").clear()
        driver.find_element(By.ID, "userPassword").clear()
    if(len(a) < 3):
        attempt_login = False
        
sleep(2)

driver.find_element(By.ID, "tabs-16_TAB").click()

sleep(2)

[aca, weighted, gpa, gpadate, gpats, gpatod] = (driver.find_element(By.ID, "gpaTableBodyTable")).text.split()
[rank, nic, grade, rankdate, rankts, ranktod] = (driver.find_element(By.ID, "lastGpaRankTableBodyTable")).text.split()


print(gpa)
print(rank)

sleep(5)

driver.quit()