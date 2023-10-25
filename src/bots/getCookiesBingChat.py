from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

def getCookiesBingChat():
  options = webdriver.ChromeOptions()
  options.add_argument('user-agent= Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51')
  options.add_argument('--headless')

  driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
  driver.get('https://bing.com/chat')
  wait = WebDriverWait(driver, 10)
  element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

  while True:
    try:
      wait = WebDriverWait(driver, 10)
      element = wait.until(EC.presence_of_element_located((By.ID, "b_sydConvCont")))
      if element:
        break
    except Exception as e:
      print(f'Error: {e}')
    sleep(1)

  cookies = driver.get_cookies()
  driver.quit()
  return cookies