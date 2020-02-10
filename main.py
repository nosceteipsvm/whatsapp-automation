from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import sys, time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

CONTACTS_PATH = './contacts.txt'
targets = []
msg = 'Este es un mensaje de prueba'
driver = webdriver.Chrome('./chromedriver.exe')

def send():
    wait = WebDriverWait(driver, 600)
    wait5 = WebDriverWait(driver, 5)

    for target in targets:
        x_arg = '//span[contains(@title,' + '"' + target + '"' +')]'
        group_title = wait.until(EC.presence_of_element_located((
            By.XPATH, x_arg)))
        group_title.click()

        message = driver.find_element_by_class_name('_13mgZ')
        message.send_keys(msg)

        sendbutton = driver.find_element_by_class_name('_3M-N-')
        sendbutton.click()
        time.sleep(2)

    #driver.close()

def main():
    try:
        with open(CONTACTS_PATH) as f:
            for contact in f.readlines():
                targets.append(contact.rstrip('\n'))
    except Exception as e:
        print(e); driver.close(); sys.exit(1)

    driver.get("https://web.whatsapp.com/")

    sched = BlockingScheduler()
    # Schedule job_function to be called every 30 seconds
    sched.add_job(send, 'interval', seconds=30)
    sched.start()

if __name__=='__main__':
    main()