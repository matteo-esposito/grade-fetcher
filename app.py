from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import getpass
from bs4 import BeautifulSoup
import pandas as pd 
import os
import time
import sys

class GradeBot():
    def __init__(self, username, password):
        """Gradebot! Your automated MyConcordia grade checker. For those stressful times
        where you are obsessively checking your grades that always seem to come out way later than expected :P
        
        Arguments:
            username {string} -- MyConcordia username
            password {string} -- MyConcordia password
        """
        self.username = username
        self.password = password
        opts = webdriver.FirefoxOptions()
        opts.headless = False
        self.bot = webdriver.Firefox(options=opts)

    def login(self):
        # Goto site
        bot = self.bot
        bot.get("https://my.concordia.ca/psp/upprpr9/?cmd=login&languageCd=ENG")
        time.sleep(1)

        # Locate and populate user and pwd fields.
        user_field = bot.find_element_by_class_name('form_login_username')
        pwd_field = bot.find_element_by_class_name('form_login_password')
        user_field.clear()
        pwd_field.clear()
        user_field.send_keys(self.username)
        pwd_field.send_keys(self.password)
        pwd_field.send_keys(Keys.RETURN)
        time.sleep(5)

        if bot.current_url == 'https://my.concordia.ca/psp/upprpr9/EMPLOYEE/EMPL/h/?tab=CU_MY_FRONT_PAGE2':
            pass
        else:
            print('Login failed.')
            print('Re-run the program.')
            sys.exit(1)
        print("✓ Logged in successfully.")

        # Goto student center and find grades
        bot.find_element_by_xpath('//a[@id="fldra_CU_MY_STUD_CENTRE" and @class="ptntop"]').click()
        time.sleep(2)
        bot.find_element_by_xpath('//a[@class="ptntop" and @role="menuitem" and @href="https://my.concordia.ca/psp/upprpr9/EMPLOYEE/EMPL/s/WEBLIB_CONCORD.CU_SIS_INFO.FieldFormula.IScript_Campus_Student_Trans?FolderPath=PORTAL_ROOT_OBJECT.CU_MY_STUD_CENTRE.CAMPUS_STUDENT_TRANSCRIPT&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder"]').click()
        time.sleep(2)

    def goto_grades(self, semester):
        bot = self.bot

        # Radio button
        bot.switch_to.frame(bot.find_element_by_name('TargetContent'))
        if semester == 'Winter 2020':
            bot.find_element_by_xpath("//input[@id='SSR_DUMMY_RECV1$sels$0$$0'][@name='SSR_DUMMY_RECV1$sels$0'][@type='radio']").click()
        elif semester == 'Fall 2019':
            bot.find_element_by_xpath("//input[@id='SSR_DUMMY_RECV1$sels$1$$0'][@name='SSR_DUMMY_RECV1$sels$0'][@type='radio']").click()
        elif semester == 'Summer 2019':
            bot.find_element_by_xpath("//input[@id='SSR_DUMMY_RECV1$sels$2$$0'][@name='SSR_DUMMY_RECV1$sels$0'][@type='radio']").click()
        elif semester == 'Winter 2019':
            bot.find_element_by_xpath("//input[@id='SSR_DUMMY_RECV1$sels$3$$0'][@name='SSR_DUMMY_RECV1$sels$0'][@type='radio']").click()
        elif semester == 'Fall 2018':
            bot.find_element_by_xpath("//input[@id='SSR_DUMMY_RECV1$sels$4$$0'][@name='SSR_DUMMY_RECV1$sels$0'][@type='radio']").click()
        elif semester == 'Summer 2018':
            bot.find_element_by_xpath("//input[@id='SSR_DUMMY_RECV1$sels$5$$0'][@name='SSR_DUMMY_RECV1$sels$0'][@type='radio']").click()
        elif semester == 'Winter 2018':
            bot.find_element_by_xpath("//input[@id='SSR_DUMMY_RECV1$sels$6$$0'][@name='SSR_DUMMY_RECV1$sels$0'][@type='radio']").click()
        elif semester == 'Fall 2017':
            bot.find_element_by_xpath("//input[@id='SSR_DUMMY_RECV1$sels$7$$0'][@name='SSR_DUMMY_RECV1$sels$0'][@type='radio']").click()
        elif semester == 'Summer 2017':
            bot.find_element_by_xpath("//input[@id='SSR_DUMMY_RECV1$sels$8$$0'][@name='SSR_DUMMY_RECV1$sels$0'][@type='radio']").click()
        elif semester == 'Winter 2017':
            bot.find_element_by_xpath("//input[@id='SSR_DUMMY_RECV1$sels$9$$0'][@name='SSR_DUMMY_RECV1$sels$0'][@type='radio']").click()
        elif semester == 'Fall 2016':
            bot.find_element_by_xpath("//input[@id='SSR_DUMMY_RECV1$sels$10$$0'][@name='SSR_DUMMY_RECV1$sels$0'][@type='radio']").click()
        else:
            print('Invalid semester')
            print('Re-run the program.')
            sys.exit(1)
        
        # Continue
        bot.find_element_by_xpath('//input[@class="PSPUSHBUTTON"][@name="DERIVED_SSS_SCT_SSR_PB_GO"][@type="button"]').click()
        print("✓ " + semester + " grades fetched.")
        
    def console_log_grades(self):
        bot = self.bot
        print("Creating grade output...")

        # Save current url to html
        time.sleep(1.5)
        with open('page.html', 'w') as f:
            f.write(bot.page_source)

        site = os.getcwd() + '/page.html'
        page = open(site)
        soup = BeautifulSoup(page.read(), 'lxml')
        os.remove('page.html')

        # Parse
        data = []
        table = soup.find('table', {'class': 'PSLEVEL1GRIDWBO'})
        table_body = table.find('tbody')

        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols]) # Get rid of empty values

        # Convert to dataframe
        df = pd.DataFrame(data).drop([0])
        unwanted = [x for x in range(6,len(df.columns))]
        df = df.drop(df.columns[unwanted], axis=1)
        df = df.drop([1])
        df.columns = ['Class', 'Description', 'Units', 'Grading', 'Letter Grade', 'Grade Points']
        print()
        print(df.to_string(index=False))
        print()

if __name__ == '__main__':

    # Accept user input
    user = input('Username: ')
    pwd = getpass.getpass()
    checker = GradeBot(user, pwd)

    # Fetch grades
    checker.login()
    semester = input('Semester: ')
    checker.goto_grades(semester)
    checker.console_log_grades()
    
