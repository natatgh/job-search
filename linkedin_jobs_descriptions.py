import sqlite3
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def linkedin_login(driver, username, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)

    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(username)
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(3)

def create_tables():
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            link TEXT,
            description TEXT
        )
    ''')

    conn.commit()
    conn.close()

def get_job_description(driver, job_url):
    try:
        driver.get(job_url)
        time.sleep(3)
        description_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.jobs-box__html-content.jobs-description-content__text"))
        )
        description_html = description_element.get_attribute("outerHTML")
        return description_html.strip()
    except Exception as e:
        print("Erro ao extrair a descrição da vaga:", e)
        return ""

def read_jobs_from_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, company, location, link FROM jobs")
    jobs = cursor.fetchall()
    conn.close()
    return jobs

def update_job_description_in_db(db_name, job_id, description):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE jobs SET description = ? WHERE id = ?", (description, job_id))
    conn.commit()
    conn.close()

def process_links(driver, db_name, jobs, batch_size=5):
    for i in range(0, len(jobs), batch_size):
        batch = jobs[i:i+batch_size]

        # Abrir links em novas guias
        for index, job in enumerate(batch):
            job_id, title, company, location, link = job
            print(f"Abrindo a vaga {i + index + 1}: {title}")
            driver.execute_script(f"window.open('{link}', '_blank');")
            time.sleep(2)  # Espera para garantir que a página carregue

        # Alternar entre as guias e extrair descrições
        for handle in driver.window_handles[1:]:
            driver.switch_to.window(handle)
            time.sleep(3)  # Espera para garantir que a página carregue
            description = get_job_description(driver, driver.current_url)
            job_id = batch[driver.window_handles.index(handle) - 1][0]
            update_job_description_in_db(db_name, job_id, description)
            print(f"Descrição extraída para a vaga {job_id}")

        # Fechar todas as guias abertas
        for handle in driver.window_handles[1:]:
            driver.switch_to.window(handle)
            driver.close()

        # Voltar para a guia principal
        driver.switch_to.window(driver.window_handles[0])

def main():
    db_name = "jobs.db"
    create_tables()

    username = "natatgh@gmail.com"  # Substitua pelo seu email do LinkedIn
    password = "ig37wNwi956Z"  # Substitua pela sua senha do LinkedIn

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    linkedin_login(driver, username, password)

    jobs = read_jobs_from_db(db_name)
    process_links(driver, db_name, jobs, batch_size=5)

    driver.quit()
    print("Descrições salvas no banco de dados")

if __name__ == "__main__":
    main()
