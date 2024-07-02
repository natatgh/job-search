from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sqlite3

def linkedin_login(driver, username, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)

    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(username)
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(3)

def create_job_links_table():
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def save_job_link_to_db(job_link):
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO job_links (link)
        VALUES (?)
    ''', (job_link,))

    conn.commit()
    conn.close()

def extract_jobs_html(driver):
    job_elements = driver.find_elements(By.CSS_SELECTOR, "ul.scaffold-layout__list-container li")

    for index, job_element in enumerate(job_elements):
        try:
            print(f"Debug: Extraindo HTML da vaga {index + 1}")
            job_html = job_element.get_attribute('outerHTML')
            print(job_html)

            try:
                # Aumentar o tempo de espera para garantir que o elemento esteja carregado
                job_link_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a.job-card-container__link.job-card-list__title.job-card-list__title--link"))
                )
                job_link = job_link_element.get_attribute("href")
                print(f"Link da vaga {index + 1}: {job_link}")
                save_job_link_to_db(job_link)
            except Exception as e:
                print(f"Link da vaga {index + 1} não encontrado: {e}")
        except Exception as e:
            print(f"Erro ao extrair HTML da vaga {index + 1}: {e}")
            continue

def main():
    create_job_links_table()

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
        extract_jobs_html(driver)

        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.jobs-search-pagination__button--next"))
            )
            next_button.click()
            time.sleep(3)
        except Exception as e:
            print("Erro ao clicar no botão 'Avançar':", e)
            break

    driver.quit()

if __name__ == "__main__":
    main()
