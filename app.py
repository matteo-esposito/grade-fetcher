# -*- coding: UTF-8 -*-

"""
Author: Matteo Esposito
Date: Fall 2019
"""

import os
import sys
import time
import pandas as pd
import getpass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from configs.config import cfg
from utils import timenow

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
        """Uses username and password to login to the student portal.
        """
        # Goto site
        bot = self.bot
        bot.get("https://my.concordia.ca/psp/upprpr9/?cmd=login&languageCd=ENG")
        time.sleep(1)

        # print("Logging in...")

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
        # print("✓ Logged in successfully.")

        # Goto student center and find grades
        bot.find_element_by_xpath(
            '//a[@id="fldra_CU_MY_STUD_CENTRE" and @class="ptntop"]').click()
        time.sleep(2)
        bot.find_element_by_xpath('//a[@class="ptntop" and @role="menuitem" and @href="https://my.concordia.ca/psp/upprpr9/EMPLOYEE/EMPL/s/WEBLIB_CONCORD.CU_SIS_INFO.FieldFormula.IScript_Campus_Student_Trans?FolderPath=PORTAL_ROOT_OBJECT.CU_MY_STUD_CENTRE.CAMPUS_STUDENT_TRANSCRIPT&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder"]').click()
        time.sleep(4)

    def goto_grades(self, semester, old_format=False):
        """Get to grade section after clicking on the radio button corresponding to the user input for 'semester'.

        Arguments:
            semester {String} -- Semester from Fall 2016 to Winter 2020.
            old_format {bool} -- Perform additional button click post-app update.
        """
        bot = self.bot

        # Change semester view.
        bot.switch_to.frame(bot.find_element_by_name('TargetContent'))
        if not old_format:
            bot.find_element_by_xpath('//input[@class="PSPUSHBUTTON"][@name="DERIVED_SSS_SCT_SSS_TERM_LINK"]'
                                      '[@id="DERIVED_SSS_SCT_SSS_TERM_LINK"][@type="button"]').click()
            time.sleep(2)

        # Semester selection
        if semester not in cfg['semester_mapping'].keys():
            print('Unsupported/invalid semester. Choose semester between Fall 2016 and Winter 2020.')
            sys.exit(1)

        idval = cfg['semester_mapping'][semester]
        chosen_id = "SSR_DUMMY_RECV1$sels$" + str(idval) + "$$0"
        bot.find_element_by_xpath("//input[@id=" + "\'" + chosen_id + "\'" + "][@name='SSR_DUMMY_RECV1$sels$0'][@type='radio']").click()


    def output_vmg(self):
        """Output what is seen at 'view my grades' on myconcordia portal.
        """
        bot = self.bot

        # GRADES
        bot.find_element_by_xpath('//input[@class="PSPUSHBUTTON"][@name="DERIVED_SSS_SCT_SSR_PB_GO"][@type="button"]').click()

        # Save current url to html
        time.sleep(1.5)
        with open('grades.html', 'w') as f:
            f.write(bot.page_source)
        site = os.getcwd() + '/grades.html'
        page = open(site)
        soup = BeautifulSoup(page.read(), features="html.parser")
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
        unwanted = [x for x in range(6, len(grades_df.columns))]
        grades_df = grades_df.drop(grades_df.columns[unwanted], axis=1)
        grades_df = grades_df.drop([1])
        grades_df.columns = ['Class', 'Description',
                             'Units', 'Grading', 'Letter Grade', 'Grade Points']

        # DISTRIBUTION
        bot.find_element_by_xpath(
            '//a[@class="PSHYPERLINK"][@id="ICTAB_1_54"]').click()

        time.sleep(1.5)
        with open('dist.html', 'w') as f:
            f.write(bot.page_source)

        site = os.getcwd() + '/dist.html'
        page = open(site)
        soup = BeautifulSoup(page.read(), features="html.parser")
        os.remove('dist.html')

        # Parse distribution table
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
        dist_df.columns = ['Class', 'A+', 'A', 'A-', 'B+', 'B', 'B-',
                           'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F', 'FNS', 'R', 'NR']

        # Fixing missing class name in cell (1, 1)
        dist_df.Class = dist_df.Class.shift(-1)
        dist_df.Class.loc[dist_df.shape[0]] = grades_df.Class[grades_df.shape[0]+1]

        bot.quit()
        return grades_df, dist_df

    def send_message(self, grades_table, distribution_table, bot_pwd):
        """SMTP/ESMTP client for automated emails.

        Arguments:
            grades_table {dataframe} -- Grade table
            distribution_table {dataframe} -- Grade distribution table
            bot_pwd {string} -- Sender email password
        """

        # General setup
        msg = MIMEMultipart()
        msg['From'] = cfg['source_email']
        msg['To'] = cfg['target_email']
        msg['Subject'] = "New Grade!"

        # Structure the tables to be featured in the email.
        table1 = """
        <html>
          <head></head>
          <body>
            {0}
          </body>
        </html>
        """.format(grades_table.to_html())

        whitespace = """
        <html>
          <head></head>
          <body>
            
          </body>
        </html>
        """

        table2 = """\
        <html>
          <head></head>
          <body>
            {0}
          </body>
        </html>
        """.format(distribution_table.to_html())
        msg.attach(MIMEText(table1, 'html'))
        msg.attach(MIMEText(whitespace, 'html'))
        msg.attach(MIMEText(table2, 'html'))

        # Send the message and quit.
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(msg['From'], bot_pwd)
        text = msg.as_string()  # You now need to convert the MIMEMultipart object to a string to send
        server.sendmail(msg['From'], msg['To'], text)
        server.quit()

if __name__ == '__main__':

    # Accept user input for username, passwords and semester
    user = input('Username: ')
    pwd = getpass.getpass()
    bot_pwd = getpass.getpass()
    semester = input('Semester: ')
    checker = GradeBot(user, pwd)
    old_grades = pd.DataFrame({"Letter Grade": ["", "", "", ""]})

    while True:
        # Instantiate bot with command-line-args and login
        checker = GradeBot(user, pwd)
        checker.login()

        # Fetch grades
        checker.goto_grades(semester)
        grades, distribution = checker.output_vmg()

        # Print tables depending on config option.
        if cfg['options']['console_log_tables']:
            print(grades.to_string(index=False) + '\n\n' + distribution.to_string(index=False) + '\n')

        # Compare to previous version and send email if different.
        if list(grades['Letter Grade']) != list(old_grades['Letter Grade']):
            checker.send_message(grades, distribution, bot_pwd)
            print(timenow() + "******Email sent.")
        else:
            print(timenow() + "No changes detected.")

        # Store copy of previous grade matrix for future comparisons.
        old_grades = grades.copy()

        # Run every 30 min
        time.sleep(cfg['options']['time_interval'])
