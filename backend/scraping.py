from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def buscar_vagas(linguagens, modalidade='', contrato='', limite_vagas=50):
    # Configurações do Selenium para rodar em modo headless
    options = Options()
    options.add_argument('--headless')  # Modo headless
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Inicializa o driver do Chrome
    driver = webdriver.Chrome(options=options)

    todas_vagas = []  # Para armazenar todas as vagas de todas as tecnologias

    for linguagem in linguagens:
        vagas = []  # Para armazenar as vagas de cada tecnologia específica
        print(f"\nIniciando a busca de vagas para: {linguagem}")

        # URL de exemplo para buscar vagas relacionadas à linguagem
        url = f'https://portal.gupy.io/job-search/term={linguagem}'
        driver.get(url)

        # Aguarda até que os elementos de vagas estejam presentes
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a.sc-4d881605-1'))  # Seleciona os links de vagas
            )
            print(f"Página carregada para {linguagem}. Iniciando scraping...")
        except Exception as e:
            print(f"Erro ao carregar a página para {linguagem}: {e}")
            continue  # Passa para a próxima linguagem em caso de erro

        # Loop para rolar a página e carregar mais vagas até atingir o limite de 50 vagas por tecnologia
        last_height = driver.execute_script("return document.body.scrollHeight")
        while len(vagas) < limite_vagas:
            print(f"Realizando scroll para carregar mais vagas ({len(vagas)} vagas encontradas até agora para {linguagem})...")

            # Rola até o final da página
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Espera 3 segundos para permitir o carregamento das novas vagas

            # Atualiza a altura da página após o scroll
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print(f"Nenhuma nova vaga encontrada para {linguagem} após o scroll.")
                break  # Sai do loop se não houver mais vagas para carregar
            last_height = new_height

            # Extrai o HTML da página após o scroll
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Localiza os elementos de vagas
            vagas_html = soup.find_all('a', class_='sc-4d881605-1')  # Classe usada nos links de vagas

            for vaga_html in vagas_html:
                if len(vagas) >= limite_vagas:
                    break  # Interrompe quando atingir o limite de vagas por tecnologia

                titulo = vaga_html.find('h3').text if vaga_html.find('h3') else 'Sem título'
                empresa = vaga_html.find('p', class_='sc-bBXxYQ').text if vaga_html.find('p', class_='sc-bBXxYQ') else 'Sem empresa'
                descricao = vaga_html.get('aria-label', 'Sem descrição')  # Obtém a descrição a partir do atributo 'aria-label'
                link = vaga_html.get('href', 'Sem link')  # Obtém o link da vaga

                # Aplica os filtros de modalidade e contrato
                if (modalidade.lower() in descricao.lower() or modalidade == '') and \
                   (contrato.lower() in descricao.lower() or contrato == ''):
                    vaga = {
                        'titulo': titulo,
                        'empresa': empresa,
                        'descricao': descricao,
                        'link': link
                    }
                    vagas.append(vaga)

            print(f"{len(vagas_html)} novas vagas encontradas para {linguagem}. Total de vagas até agora para {linguagem}: {len(vagas)}.")

        todas_vagas.extend(vagas)  # Adiciona as vagas da tecnologia atual à lista geral
        print(f"Finalizada busca de vagas para {linguagem}. Total de vagas encontradas: {len(vagas)}")

    driver.quit()
    print(f"Scraping finalizado. Total de vagas encontradas para todas as linguagens: {len(todas_vagas)}.")
    return todas_vagas
