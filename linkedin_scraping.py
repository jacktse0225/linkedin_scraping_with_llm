import pandas as pd
from function import generate_summary, save_as_txt, init_selenium, selenium_actions, selenium_wait, getting_file_path
import ast

def main():
    linkedin_url_file_path = getting_file_path(False, 'xlsx')
    df = pd.read_excel(linkedin_url_file_path)
    driver, actions, wait = init_selenium()
    list = []
    login_url = 'https://www.linkedin.com/uas/login?session_redirect=%2Foauth%2Fv2%2Flogin-success%3Fapp_id%3D4445964%26auth_type%3DAC%26flow%3D%257B%2522state%2522%253A%2522851dc56495aa5af8d26b646b9248e36b%2522%252C%2522scope%2522%253A%2522r_liteprofile%2Br_emailaddress%2522%252C%2522authFlowName%2522%253A%2522generic-permission-list%2522%252C%2522appId%2522%253A4445964%252C%2522authorizationType%2522%253A%2522OAUTH2_AUTHORIZATION_CODE%2522%252C%2522currentSubStage%2522%253A0%252C%2522creationTime%2522%253A1712668300404%252C%2522currentStage%2522%253A%2522LOGIN_SUCCESS%2522%252C%2522redirectUri%2522%253A%2522https%253A%252F%252Fauthenticate.v6-prod-use1.talentnet.community%252Fauth%252Flinkedin%252Fcallback%2522%257D&fromSignIn=1&trk=oauth&cancel_redirect=%2Foauth%2Fv2%2Flogin-cancel%3Fapp_id%3D4445964%26auth_type%3DAC%26flow%3D%257B%2522state%2522%253A%2522851dc56495aa5af8d26b646b9248e36b%2522%252C%2522scope%2522%253A%2522r_liteprofile%2Br_emailaddress%2522%252C%2522authFlowName%2522%253A%2522generic-permission-list%2522%252C%2522appId%2522%253A4445964%252C%2522authorizationType%2522%253A%2522OAUTH2_AUTHORIZATION_CODE%2522%252C%2522currentSubStage%2522%253A0%252C%2522creationTime%2522%253A1712668300404%252C%2522currentStage%2522%253A%2522LOGIN_SUCCESS%2522%252C%2522redirectUri%2522%253A%2522https%253A%252F%252Fauthenticate.v6-prod-use1.talentnet.community%252Fauth%252Flinkedin%252Fcallback%2522%257D'
    driver.get(login_url)
    user_confirm = input("Press Enter To Continue after loggin in: ")

    for index, row in df.iterrows():
        url = row['URL']
        print(f"Processing URL: {url}")
        driver.get(url)
        try:
            wait_element = selenium_wait(wait)
            copied_content = selenium_actions(actions)
            save_as_txt(str(copied_content), f"output.txt")
            with open(f"output.txt", 'r', encoding='utf-8') as file:
                copied_text = file.read()
            try:
                summary = generate_summary(copied_text)
                dict_input = summary.choices[0].message.content
                dict_input = ast.literal_eval(dict_input)
                dict_input.update({'linkedin_url':url})
            except Exception as e:
                dict_input = {}
                print(f"Failed to generate summary from URL: {url}")
        except Exception as e:
            dict_input = {}
            print(f"Failed to process URL: {url}")

        list.append(dict_input)
        print(dict_input)
    driver.quit()
    df = pd.DataFrame(list)
    df.to_excel("scraping_result.xlsx", index=False)

if __name__ == "__main__":
    main()