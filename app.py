from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import getpass
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import sys

class GradeBot:
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
        opts.headless = True
        self.bot = webdriver.Firefox(options=opts)

    def login(self):
        # Goto site
        bot = self.bot
        bot.get("https://my.concordia.ca/psp/upprpr9/?cmd=login&languageCd=ENG")
        time.sleep(1)

        print("Logging in...")

        # Locate and populate user and pwd fields.
        user_field = bot.find_element_by_class_name('form_login_username')
        pwd_field = bot.find_element_by_class_name('form_login_password')
        user_field.clear()
        pwd_field.clear()
        user_field.send_keys(self.username)
        pwd_field.send_keys(self.password)
        pwd_field.send_keys(Keys.RETURN)
        time.sleep(6)

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
        time.sleep(4)

    def goto_grades(self, semester):
        """Get to grade section after clicking on the radio button corresponding to the user input for 'semester'.

        Arguments:
            semester {String} -- Semester from Fall 2016 to Winter 2020.
        """
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

    def output_vmg(self):
        """
        Output what is seen at 'view my grades'
        """
        bot = self.bot

        # GRADES
        bot.find_element_by_xpath('//input[@class="PSPUSHBUTTON"][@name="DERIVED_SSS_SCT_SSR_PB_GO"][@type="button"]').click()
        print("✓ " + semester + " grades fetched.")

        # Save current url to html
        time.sleep(1.5)
        with open('grades.html', 'w') as f:
            f.write(bot.page_source)
        site = os.getcwd() + '/grades.html'
        page = open(site)
        soup = BeautifulSoup(page.read(), 'lxml')
        os.remove('grades.html')

        # Parse
        grades = []
        table = soup.find('table', {'class': 'PSLEVEL1GRIDWBO'})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            grades.append([ele for ele in cols])

        # Convert to dataframe
        grades_df = pd.DataFrame(grades).drop([0])
        unwanted = [x for x in range(6,len(grades_df.columns))]
        grades_df = grades_df.drop(grades_df.columns[unwanted], axis=1)
        grades_df = grades_df.drop([1])
        grades_df.columns = ['Class', 'Description', 'Units', 'Grading', 'Letter Grade', 'Grade Points']

        # DISTRIBUTION
        bot.find_element_by_xpath('//a[@class="PSHYPERLINK"][@id="ICTAB_1_54"]').click()
        print('✓ ' + semester + " distribution fetched.\n")

        time.sleep(1.5)
        with open('dist.html', 'w') as f:
            f.write(bot.page_source)

        site = os.getcwd() + '/dist.html'
        page = open(site)
        soup = BeautifulSoup(page.read(), 'lxml')
        os.remove('dist.html')

        # Parse
        dist = []
        table = soup.find('table', {'class': 'PSLEVEL1GRID'})
        table_body = table.find('tbody')

        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            dist.append([ele for ele in cols])

        # Convert to dataframe
        dist_df = pd.DataFrame(dist).drop([0])

        dist_df.insert(0, 'Class', grades_df.Class)
        dist_df.columns = ['Class', 'A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F', 'FNS', 'R','NR']

        # Fixing missing class name in cell (1, 1)
        dist_df.Class = dist_df.Class.shift(-1)
        dist_df.Class.loc[dist_df.shape[0]] = grades_df.Class[grades_df.shape[0]+1]

        print(grades_df.to_string(index=False) + '\n\n' + dist_df.to_string(index=False) + '\n')

if __name__ == '__main__':

    # Accept user input for username, password and semester
    user = input('Username: ')
    pwd = getpass.getpass()
    semester = input('Semester: ')
    checker = GradeBot(user, pwd)

    # Login
    checker.login()

    # Fetch grades
    checker.goto_grades(semester)
    checker.output_vmg()
