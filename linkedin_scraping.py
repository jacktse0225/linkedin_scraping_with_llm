from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import pyperclip
from function import generate_summary, save_as_txt, init_selenium
import ast

excel_file_path = 'linkedin_url.xlsx'
df = pd.read_excel(excel_file_path)
driver, actions = init_selenium()
list = []

for index, row in df.iterrows():
    url = row['URL']
    print(f"Processing URL: {url}")
    driver.get(url)
    user_confirm = input("Press Enter To Continue")
    if user_confirm == "":
        time.sleep(1)
        actions.key_down(Keys.CONTROL).send_keys('a').perform()
        time.sleep(1)
        actions.key_down(Keys.CONTROL).send_keys('c').perform()
        time.sleep(1)
        copied_content = pyperclip.paste().lower()
        save_as_txt(str(copied_content), f"output.txt")
        with open(f"output.txt", 'r', encoding='utf-8') as file:
            copied_text = file.read()
        try:
            summary = generate_summary(copied_text)
            dict_input = summary.choices[0].message.content
            dict_input = ast.literal_eval(dict_input)
            dict_input.update({'linkedin_url':url})
        except:
            dict_input = {}
            print(f"Fail to get the info from URL: {url}")
        list.append(dict_input)
        print(dict_input)
driver.quit()
df = pd.DataFrame(list)
df.to_excel("scraping_result.xlsx", index=False)