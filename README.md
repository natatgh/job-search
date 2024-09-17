
# Sistema de Busca de Vagas

Este projeto é um sistema de busca de vagas de emprego que realiza scraping de vagas em plataformas como Gupy e exibe os resultados de forma paginada. O sistema permite que o usuário selecione várias tecnologias para busca e aplique filtros como modalidade de trabalho e tipo de contrato. 

## Funcionalidades

- Busca de vagas de emprego em diferentes tecnologias.
- Seleção de várias linguagens de programação.
- Filtros de modalidade de trabalho (remoto, presencial, híbrido).
- Filtros de tipo de contrato (efetivo, PJ, freelancer).
- Exibição paginada dos resultados, mostrando 10 vagas por vez.
- Notificação ao usuário enquanto as vagas estão sendo carregadas.
- Carregamento dinâmico de mais vagas com o botão "Ver mais".
- Sistema de scraping que coleta até 50 vagas por tecnologia selecionada.

## Tecnologias Utilizadas

### Frontend:
- **HTML**: Estrutura da página.
- **CSS**: Estilização da página, incluindo responsividade.
- **JavaScript**: Interatividade, manipulação do DOM e integração com o backend.

### Backend:
- **Python (Flask)**: Servidor backend para receber requisições de busca e realizar o scraping.
- **Selenium**: Biblioteca para automatização de navegação e scraping de páginas web dinâmicas.
- **BeautifulSoup**: Biblioteca para parsear e extrair dados de HTML.

### Banco de Dados:
- **SQLite**: Utilizado como banco de dados temporário durante o desenvolvimento.

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/sistema-busca-vagas.git
    cd sistema-busca-vagas
    ```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scriptsctivate
    ```

3. Instale as dependências:
    ```bash
    pip install -r backend/requirements.txt
    ```

4. Execute o servidor Flask:
    ```bash
    python backend/app.py
    ```

5. Abra o `index.html` no navegador:
    - Acesse o arquivo `frontend/index.html` diretamente em seu navegador (usando uma extensão de servidor local ou configurando uma solução local, como o Live Server do VSCode).

## Como Usar

1. Na página inicial, selecione as tecnologias que deseja buscar utilizando as checkboxes.
2. Clique no botão "Buscar Vagas".
3. As vagas encontradas serão exibidas em grupos de 10. Para ver mais vagas, clique no botão "Ver mais vagas".
4. Utilize os filtros de "Modalidade de Trabalho" e "Tipo de Contrato" para refinar os resultados.
5. Caso queira remover os filtros e voltar a ver todas as vagas, altere os filtros para "Qualquer" ou desmarque os checkboxes.

## Estrutura do Projeto

```bash
├── backend
│   ├── app.py               # Servidor Flask
│   ├── scraping.py          # Funções de scraping
│   ├── database.py          # Configuração do banco de dados
│   └── requirements.txt     # Dependências do projeto
├── frontend
│   ├── index.html           # Página principal
│   ├── style.css            # Estilos da página
│   └── script.js            # Lógica de frontend
├── tests
│   ├── test_backend.py      # Testes do backend
│   └── test_scraping.py     # Testes do scraping
└── README.md
```

## Melhorias Futuras

- Implementação de autenticação de usuário.
- Agendamento de buscas automáticas e notificações de novas vagas.
- Integração com outras plataformas de emprego.
- Deploy da aplicação em um servidor online (como Heroku ou AWS).

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests no GitHub.

## Licença

Este projeto está licenciado sob a licença MIT.
