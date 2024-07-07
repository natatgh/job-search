import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def create_tables(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Exclui a tabela jobs se ela já existir
    cursor.execute("DROP TABLE IF EXISTS jobs")
    
    # Cria a tabela jobs com as colunas necessárias
    cursor.execute('''
        CREATE TABLE jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            link TEXT,
            description TEXT,
            company_logo TEXT,
            html_description TEXT,
            tags TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_job_details(job_url):
    try:
        # Configurações do Selenium para rodar em modo headless
        options = Options()
        #options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Inicializa o driver do Chrome
        driver = webdriver.Chrome(options=options)

        driver.get(job_url)
        time.sleep(20)  # Espera para garantir que todo o conteúdo seja carregado

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        title_element = soup.select_one("h1.top-card-layout__title")
        company_element = soup.select_one("a.topcard__org-name-link")
        location_element = soup.select_one("span.topcard__flavor--bullet")
        company_logo_element = soup.select_one("img.artdeco-entity-image--square-5")
        
        title = title_element.get_text(strip=True) if title_element else "Título não encontrado"
        company = company_element.get_text(strip=True) if company_element else "Empresa não encontrada"
        location = location_element.get_text(strip=True) if location_element else "Localização não encontrada"

        # Captura o HTML completo dentro do campo especificado pelo seletor CSS
        description_container = soup.select_one('div.description__text.description__text--rich')
        html_description = str(description_container) if description_container else "Descrição HTML não encontrada"
        description = description_container.get_text(strip=True) if description_container else "Descrição não encontrada"

        company_logo = company_logo_element['src'] if company_logo_element else "Logotipo não encontrado"

        # Captura as tags de critérios de emprego
        criteria_list = soup.select("ul.description__job-criteria-list li")
        tags = [li.get_text(strip=True) for li in criteria_list]
        tags_text = "; ".join(tags) if tags else "Tags não encontradas"

        driver.quit()
        return title, company, location, description, company_logo, html_description, tags_text
    except Exception as e:
        print(f"Erro ao extrair os detalhes da vaga: {job_url}, erro: {e}")
        return "Título não encontrado", "Empresa não encontrada", "Localização não encontrada", "Descrição não encontrada", "Logotipo não encontrado", "Descrição HTML não encontrada", "Tags não encontradas"

def read_links_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='job_links'")
    table_exists = cursor.fetchone()
    if not table_exists:
        print("A tabela job_links não existe no banco de dados.")
        conn.close()
        return []

    cursor.execute("SELECT id, link FROM job_links")
    links = cursor.fetchall()
    conn.close()
    return links

def insert_job_into_db(db_path, title, company, location, link, description, company_logo, html_description, tags):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jobs (title, company, location, link, description, company_logo, html_description, tags) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                   (title, company, location, link, description, company_logo, html_description, tags))
    conn.commit()
    conn.close()

def process_links(db_path, links):
    for job in links:
        job_id, link = job
        print(f"Processando a vaga com o link: {link}")
        title, company, location, description, company_logo, html_description, tags = get_job_details(link)
        if title and company and description:
            print(f"Inserindo dados da vaga {job_id} no banco de dados.")
            insert_job_into_db(db_path, title, company, location, link, description, company_logo, html_description, tags)
            print(f"Dados da vaga {job_id} salvos com sucesso.")
        else:
            print(f"Falha ao extrair os dados para a vaga {job_id}")

def main():
    db_path = "jobs.db"  # Atualize o caminho do banco de dados conforme necessário
    create_tables(db_path)

    links = read_links_from_db(db_path)
    if links:
        process_links(db_path, links)
    else:
        print("Nenhuma vaga encontrada no banco de dados.")

    print("Dados salvos no banco de dados")

if __name__ == "__main__":
    main()
