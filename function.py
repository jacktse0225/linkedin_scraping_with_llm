from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import pyperclip
import os
import tkinter as tk
from tkinter import filedialog
import sys
import pandas as pd

def split_text(text):
    max_chunk_size = 2048
    chunks = []
    current_chunk = ""
    for sentence in text.split("."):
        if len(current_chunk) + len(sentence) < max_chunk_size:
            current_chunk += sentence + "."
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + "."
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def generate_summary(text):
    client = OpenAI(
        api_key= os.environ.get('OPENAI_API_KEY')
    )
    input_chunks = split_text(text)[0]
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Please get the the location, job title, company name, of this person, state it as a dict with this format: 'city' : city, 'state': state, 'country':country, 'job_title':job_title, 'company_name':company_name' with the following text:\n{input_chunks}\n\n",
            }
        ],
        model="gpt-4",
    )

    return chat_completion

def save_as_txt(text, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

def init_selenium():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
    driver = webdriver.Chrome()
    actions = ActionChains(driver)
    driver.execute_cdp_cmd("Page.enable", {})
    wait = WebDriverWait(driver, 10)
    return driver, actions, wait

def selenium_wait(wait):
    logo_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ivm-image-view-model')))
    return logo_element

def selenium_actions(actions):
    time.sleep(1)
    actions.key_down(Keys.CONTROL).send_keys('a').perform()
    time.sleep(1)
    actions.key_down(Keys.CONTROL).send_keys('c').perform()
    time.sleep(1)
    copied_content = pyperclip.paste().lower()
    return copied_content

def getting_file_path(multiple=False, file_type=None):
    current_directory = os.getcwd()
    root = tk.Tk()
    root.withdraw()
    file_type_dict = {"csv":(("CSV files", "*.csv"), ("All files", "*.*")), "any":"", "xlsx":(("XLSX files", "*.xlsx"), ("All files", "*.*"))}
    if multiple:
        file_path = filedialog.askopenfilenames(
            initialdir=current_directory,
            title="Select Files",
            filetypes=file_type_dict.get(file_type),
            multiple=True
        )
    else:
        file_path = filedialog.askopenfilename(
            initialdir=current_directory,
            title="Select Files",
            filetypes=file_type_dict.get(file_type),
            multiple=False
        )
    if not file_path:
        print("No files selected.")
        return sys.exit()
    return file_path

def files_to_df(file_paths, file_type=None):
    data_frames = []
    if (file_type != "csv") and (file_type != "xlsx"):
        print("Selected file type is not supported.")
        sys.exit()
        return
    if file_type == "csv":
        for file_path in file_paths:
            df_add = pd.read_csv(file_path, encoding='utf-8')
            data_frames.append(df_add)
    if file_type == "xlsx":
        for file_path in file_paths:
            df_add = pd.read_excel(file_path)
            data_frames.append(df_add)
    combined_df = pd.concat(data_frames, ignore_index=True)
    return combined_df