from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
import inquirer

# create options object
options = Options()

# start without actually showing a browser, comment this line out if you want to see it work
options.add_argument("--headless=new")

# start fullscreen even though minimized
options.add_argument("--start-maximized")

# disable debug text
options.add_argument('log-level=3')

# disable some more debug text that might show up in the terminal
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

# lead driver to website
driver.get('https://is-teams.aisd.net/selfserve/EntryPointHomeAction.do?parent=false')

ok = wait.until(expected_conditions.element_to_be_clickable((By.ID, "ok")))
ok.click()

attempt_login = True

while(attempt_login == True):
    # terminal login code
    questions = [
       inquirer.Text('username', message='Enter your Self Serve username'),
       inquirer.Password('password', message='Enter your password')
    ]

    answers = inquirer.prompt(questions)
    
    # get username and password input fields
    username = wait.until(expected_conditions.visibility_of_element_located((By.ID, "userLoginId")))
    password = wait.until(expected_conditions.visibility_of_element_located((By.ID, "userPassword")))

    # send the username and password to the fields
    username.send_keys(answers['username'])
    password.send_keys(answers['password'])

    okButton = wait.until(expected_conditions.element_to_be_clickable((By.ID, "ok")))
    okButton.click()
    
    # questionable code practice, you could probably replace this with some sort of wait.until()
    sleep(2)
    
    # what this does is:
    # > gets the list of all elements with class name error
    # > converts them into the text form using .text on each element
    # > adds them to a list
    a = [value.text for value in driver.find_elements(By.CLASS_NAME, "error")]
    
    # less than or equal to 3 errors signifies the last error is a failed to log in error
    if(len(a) >= 3):
        print("\n[!] Login failed. Please try again.\n")
        username = wait.until(expected_conditions.visibility_of_element_located((By.ID, "userLoginId")))
        password = wait.until(expected_conditions.visibility_of_element_located((By.ID, "userPassword")))
        
        username.clear()
        password.clear()
        
    # more than 3 errors means we have logged in (dont ask me why i dont know)
    if(len(a) < 3):
        attempt_login = False
        
tab16 = wait.until(expected_conditions.element_to_be_clickable((By.ID, "tabs-16_TAB")))
tab16.click()

wait.until(expected_conditions.visibility_of_element_located((By.ID, "gpaTableBodyTable")))
wait.until(expected_conditions.visibility_of_element_located((By.ID, "lastGpaRankTableBodyTable")))

# get elements and then split them after turning them into text
[aca, weighted, gpa, gpadate, gpats, gpatod] = (driver.find_element(By.ID, "gpaTableBodyTable")).text.split()
[rank, nic, grade, rankdate, rankts, ranktod] = (driver.find_element(By.ID, "lastGpaRankTableBodyTable")).text.split()

# tada!
print(f"\n[!] Your GPA is: {gpa}")
print(f"\n[!] Your Rank is: {rank}")
driver.quit()
