from openai import OpenAI
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

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
    return driver, actions