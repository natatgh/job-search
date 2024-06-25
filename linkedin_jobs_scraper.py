from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sqlite3
import subprocess
from bs4 import BeautifulSoup

def linkedin_login(driver, username, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)

    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(username)
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(3)

def save_job_to_db(job):
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO jobs (title, company, location, link, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (job['title'], job['company'], job['location'], job['link'], job['description']))

    conn.commit()
    conn.close()

def get_job_description(driver):
    try:
        description_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.jobs-box__html-content.jobs-description-content__text"))
        )
        description_html = description_element.get_attribute("outerHTML")
        soup = BeautifulSoup(description_html, 'html.parser')
        description = soup.prettify()
        return description
    except Exception as e:
        print("Erro ao extrair a descrição da vaga:", e)
        return ""

def extract_jobs(driver):
    job_data = []
    jobs = driver.find_elements(By.CSS_SELECTOR, "ul.scaffold-layout__list-container li")

    for job in jobs:
        try:
            print("Debug: Extraindo dados da vaga") 
            title_element = job.find_element(By.CSS_SELECTOR, "h3")
            company_element = job.find_element(By.CSS_SELECTOR, "h4")
            location_element = job.find_element(By.CSS_SELECTOR, "span.job-search-card__location")
            link_element = job.find_element(By.CSS_SELECTOR, "a").get_attribute('href')

            title = title_element.text
            company = company_element.text
            location = location_element.text
            link = link_element

            job.click()  # Clica na vaga para abrir a descrição
            time.sleep(2)  # Espera para a descrição carregar

            description = get_job_description(driver)

            print(f"Debug: Dados extraídos - Title: {title}, Company: {company}, Location: {location}, Link: {link}")
            job_data.append({"title": title, "company": company, "location": location, "link": link, "description": description})
            save_job_to_db({"title": title, "company": company, "location": location, "link": link, "description": description})
        except Exception as e:
            print("Erro ao extrair dados da vaga:", e)

    return job_data

def main():
    # Criar a tabela jobs antes de iniciar a raspagem
    subprocess.run(["python", "create_tables.py"])

    search_keyword = "Python"  # Palavra-chave de busca
    linkedin_url = f"https://www.linkedin.com/jobs/search/?keywords={search_keyword}&origin=JOBS_HOME_SEARCH_BUTTON&refresh=true"

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    username = "natatgh@gmail.com"
    password = "ig37wNwi956Z"
    
    linkedin_login(driver, username, password)

    driver.get(linkedin_url)
    time.sleep(3)

    while True:
        job_data = extract_jobs(driver)

        for job in job_data:
            print(f"Title: {job['title']}\nCompany: {job['company']}\nLocation: {job['location']}\nLink: {job['link']}\nDescription: {job['description']}\n")

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "button.jobs-search-pagination__button--next")
            if not next_button.is_enabled():
                break
            next_button.click()
            time.sleep(3)
        except Exception as e:
            print("Erro ao clicar no botão 'Avançar':", e)
            break

    driver.quit()

if __name__ == "__main__":
    main()
