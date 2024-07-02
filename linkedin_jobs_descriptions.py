import sqlite3
import requests
from bs4 import BeautifulSoup
import time

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
            html_description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_job_details(job_url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(job_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Espera para garantir que todo o conteúdo seja carregado
        time.sleep(3)

        # Printar o HTML completo da página
        print("HTML da página:", soup.prettify())

        title_element = soup.select_one("h1.top-card-layout__title")
        company_element = soup.select_one("a.topcard__org-name-link")
        location_element = soup.select_one("span.topcard__flavor--bullet")
        description_element = soup.select_one("div.jobs-box__html-content.jobs-description-content__text")
        company_logo_element = soup.select_one("img.ivm-view-attr__img--centered")
        
        title = title_element.get_text(strip=True) if title_element else "Título não encontrado"
        company = company_element.get_text(strip=True) if company_element else "Empresa não encontrada"
        location = location_element.get_text(strip=True) if location_element else "Localização não encontrada"
        
        # Captura o HTML completo dentro da div de descrição
        description_div = soup.find("div", class_="jobs-box__html-content jobs-description-content__text")
        html_description = str(description_div) if description_div else "Descrição HTML não encontrada"
        description = description_div.get_text(strip=True) if description_div else "Descrição não encontrada"
        
        company_logo = company_logo_element['src'] if company_logo_element else "Logotipo não encontrado"

        # Debug prints
        print(f"Job URL: {job_url}")
        print(f"Title: {title}")
        print(f"Company: {company}")
        print(f"Location: {location}")
        print(f"Description Element: {description_element}")
        print(f"Description DIV: {description_div}")
        print(f"Description (text): {description[:100]}")  # Print first 100 characters of description
        print(f"Company Logo: {company_logo}")
        print(f"HTML Description: {html_description[:100]}")  # Print first 100 characters of HTML description

        return title, company, location, description, company_logo, html_description
    except Exception as e:
        print(f"Erro ao extrair os detalhes da vaga: {job_url}, erro: {e}")
        return "", "", "", "", "", ""

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

def insert_job_into_db(db_path, title, company, location, link, description, company_logo, html_description):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jobs (title, company, location, link, description, company_logo, html_description) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (title, company, location, link, description, company_logo, html_description))
    conn.commit()
    conn.close()

def process_links(db_path, links):
    for job in links:
        job_id, link = job
        print(f"Processando a vaga com o link: {link}")
        title, company, location, description, company_logo, html_description = get_job_details(link)
        if title and company and description:
            print(f"Inserindo dados da vaga {job_id} no banco de dados.")
            insert_job_into_db(db_path, title, company, location, link, description, company_logo, html_description)
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
