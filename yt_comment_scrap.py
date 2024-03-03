import time
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_comments(link):
    data=[]
    url= link

    option=ChromeOptions()
    option.add_argument("--headless")
    option.add_argument("--mute-audio")

    with Chrome(options=option) as driver:
        wait = WebDriverWait(driver,10)
        driver.get(url)
        time.sleep(5)

        driver.execute_script("document.querySelector('video').pause()")
        height = driver.execute_script("return document.documentElement.scrollHeight")

        for item in range(5): 
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            time.sleep(1)

            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height==height:
                break
            height=new_height

        for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content-text"))):
            data.append(comment.text)

    return data
'''     

    # If we want to save the crawled comments as csv file

    with open('comment.csv','w',encoding='utf-8',newline='') as file:

        header='comments'
        writerObj = csv.writer(file)
        writerObj.writerow([header])

        for comment in data:
            writerObj.writerow([comment])

'''         