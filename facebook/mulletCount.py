import pdb
import pandas as pd

from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#usr = input('Enter Email Id:')
# pwd = input('Enter Password:')
usr = 'fasdfa'
pwd = 'asfdasdf'

class fbDriver:
    def __init__(self):
        self.usr = 'bousborne@gmail.com'
        self.pwd = 'Hokies.4life'
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get('https://www.facebook.com/')

    def getUsers(self):
        userName = self.driver.find_elements(By.XPATH, '//*[@id="reaction_profile_browser"]/div/div/div/div[1]')
        userUrl = self.driver.find_elements(By.XPATH, '//*[@id="reaction_profile_browser"]/div/div/div/a')

        # locate message form by_xpath
        urlList = []
        myUsers = []

        for element in range(len(userUrl)):
            urlList.append(userUrl[element].get_attribute("href"))
            myUsers.append(userName[element].text)

            print
            userName[element].text
            print
            userUrl[element].get_attribute("href")

        # dictionary of lists
        dict = {'Username': myUsers, 'Url': urlList}

        df = pd.DataFrame(dict)
        pdb.set_trace()

    def findUser(self):
        userName = self.driver.find_elements(By.XPATH, '//*[@id="reaction_profile_browser"]/div/div/div/div[1]')
        userUrl = self.driver.find_elements(By.XPATH, '//*[@id="reaction_profile_browser"]/div/div/div/a')
        search_box = self.driver.find_element(By.XPATH, "//input[@type='search']")

        search_box.send_keys("USA Mullet Championships")
        # locate message form by_xpath
        urlList = []
        myUsers = []


        search_results = self.driver.find_element(By.ID, 'jsc_c_3y')
        pdb.set_trace()
        for element in range(len(search_results)):
            pdb.set_trace()

        for element in range(len(userUrl)):
            urlList.append(userUrl[element].get_attribute("href"))
            myUsers.append(userName[element].text)

            print
            userName[element].text
            print
            userUrl[element].get_attribute("href")

        # dictionary of lists
        dict = {'Username': myUsers, 'Url': urlList}

        df = pd.DataFrame(dict)
        pdb.set_trace()


    def login(self):

        print("Opened facebook")
        sleep(1)

        username_box = self.driver.find_element(By.NAME, 'email')
        username_box.send_keys(usr)
        # print("Email Id entered")
        sleep(1)

        password_box = self.driver.find_element(By.ID, 'pass')
        password_box.send_keys(pwd)
        # print("Password entered")

        login_box = self.driver.find_element(By.NAME, 'login')
        login_box.click()

        print("Logged In")

        # search_box = driver.find_element_by_xpath("//input[@type='search']")
        search_box = self.driver.find_element(By.XPATH, "//input[@type='search']")

        # search_box.send_keys("USA Mullet Championships")
        # search_box.send_keys(Keys.ENTER)

        # pdb.set_trace()

    def goToMulletPost(self):
        self.driver.get("https://www.facebook.com/media/set/?vanity=mulletchampUSA&set=a.504415875025308")
        # https: // www.facebook.com / photo /?fbid = 504394515027444 & set = a
        # .504415875025308
        borderRadius = 'max(0px, min(8px, ((100vw - 4px) - 100%) * 9999)) / 8px'
        test = self.driver.find_elements(By.XPATH, "//div/div/div/div")
        for each in test:
            pdb.set_trace()

        test = self.driver.find_element(By.STYLE, borderRadius)
        pdb.set_trace()
def main():
    fbDrive = fbDriver()
    fbDrive.login()

    # fbDrive.findUser()
    fbDrive.goToMulletPost()
    input('Press anything to quit')
    fbDrive.driver.quit()
    print("Finished")
    print("Hello World!")

if __name__ == "__main__":
    main()




