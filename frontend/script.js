let allJobs = [];  // Armazena todas as vagas recebidas
let currentIndex = 0;  // Índice atual para o carregamento de vagas
const jobsPerPage = 10;  // Número de vagas a serem exibidas por vez

document.getElementById('job-search-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const linguagemElements = document.querySelectorAll('input[name="linguagem"]:checked');
    const linguagens = Array.from(linguagemElements).map(el => el.value);  // Pega todas as linguagens selecionadas

    if (linguagens.length === 0) {
        alert('Por favor, selecione pelo menos uma linguagem.');
        return;
    }

    // Exibe a mensagem de carregamento
    document.getElementById('loading-message').style.display = 'block';

    // Faz requisição ao backend para buscar todas as vagas das linguagens selecionadas
    fetch('http://localhost:5000/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ linguagens })  // Envia a lista de linguagens
    })
    .then(response => response.json())
    .then(data => {
        allJobs = data;  // Armazena todas as vagas recebidas
        currentIndex = 0;  // Reseta o índice ao começar nova busca

        // Remove a mensagem de carregamento
        document.getElementById('loading-message').style.display = 'none';

        // Exibe as primeiras 10 vagas
        displayJobs(allJobs.slice(0, jobsPerPage));
    })
    .catch((error) => {
        console.error('Erro:', error);
        document.getElementById('loading-message').style.display = 'none';
        alert('Erro ao buscar vagas, tente novamente mais tarde.');
    });
});

// Função para exibir vagas
function displayJobs(jobs) {
    const resultsDiv = document.getElementById('job-results');
    resultsDiv.innerHTML = '';  // Limpa os resultados anteriores

    if (jobs.length === 0) {
        resultsDiv.innerHTML = '<p>Nenhuma vaga encontrada.</p>';
        return;
    }

    jobs.forEach(job => {
        const jobElement = document.createElement('div');
        jobElement.innerHTML = `
            <h3>${job.titulo}</h3>
            <p>Empresa: ${job.empresa}</p>
            <p>Descrição: ${job.descricao}</p>
            <a href="${job.link}" target="_blank">Ver detalhes</a>
        `;
        resultsDiv.appendChild(jobElement);
    });

    // Verifica se há mais vagas para mostrar e exibe o botão "Ver mais"
    if (currentIndex + jobsPerPage < allJobs.length) {
        const loadMoreBtn = document.createElement('button');
        loadMoreBtn.textContent = 'Ver mais vagas';
        loadMoreBtn.addEventListener('click', loadMoreJobs);
        resultsDiv.appendChild(loadMoreBtn);
    }
}

// Função para carregar mais vagas ao clicar em "Ver mais vagas"
function loadMoreJobs() {
    currentIndex += jobsPerPage;
    displayJobs(allJobs.slice(0, currentIndex + jobsPerPage));
}

// Função para aplicar filtros após o carregamento das vagas
function applyFilters() {
    const modalidade = document.getElementById('modalidade').value;
    const contrato = document.getElementById('contrato').value;

    let filteredJobs = allJobs;

    // Aplica o filtro de modalidade se selecionado
    if (modalidade !== '') {
        filteredJobs = filteredJobs.filter(job =>
            job.descricao.toLowerCase().includes(modalidade.toLowerCase())
        );
    }

    // Aplica o filtro de contrato se selecionado
    if (contrato !== '') {
        filteredJobs = filteredJobs.filter(job =>
            job.descricao.toLowerCase().includes(contrato.toLowerCase())
        );
    }

    // Limpa o conteúdo da div antes de exibir as vagas filtradas
    const resultsDiv = document.getElementById('job-results');
    resultsDiv.innerHTML = '';  // Limpa os resultados anteriores

    currentIndex = 0;  // Reseta o índice ao aplicar um novo filtro
    displayJobs(filteredJobs.slice(0, jobsPerPage));  // Exibe as vagas filtradas
}

// Event listeners para os filtros
document.getElementById('modalidade').addEventListener('change', applyFilters);
document.getElementById('contrato').addEventListener('change', applyFilters);
