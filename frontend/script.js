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

// Função para exibir as vagas com estilo melhorado
function displayJobs(jobs) {
    const resultsDiv = document.getElementById('job-results');
    resultsDiv.innerHTML = '';  // Limpa os resultados anteriores

    if (jobs.length === 0) {
        resultsDiv.innerHTML = '<p>Nenhuma vaga encontrada.</p>';
        return;
    }

    jobs.forEach(job => {
        const jobElement = document.createElement('div');
        jobElement.classList.add('job-card');

        // Extrai o tipo de contrato e modalidade de trabalho a partir da descrição
        const tipoContrato = job.descricao.includes('Efetivo') ? 'Efetivo' : 'Freelancer';  // Exemplo básico
        const modalidadeTrabalho = job.descricao.includes('Remoto') ? 'Remoto' : 'Presencial';  // Exemplo básico

        jobElement.innerHTML = `
            <div class="job-header">
                <div class="icon-frame">
                    <i class="fi fi-ss-building"></i> <!-- Ícone do prédio -->
                </div>
                <div class="job-company">
                    <p>${job.empresa}</p>
                </div>
            </div>
            <div class="job-content">
                <div class="job-title">
                    <i class="fi fi-sc-briefcase"></i> ${job.titulo} <!-- Ícone da maleta -->
                </div>
                <div class="job-labels">
                    <span class="job-type">
                        <i class="fi fi-ss-briefcase"></i> ${tipoContrato} <!-- Ícone para tipo de contrato -->
                    </span>
                    <span class="job-modality">
                        <i class="fi fi-ss-building"></i> ${modalidadeTrabalho} <!-- Ícone para modalidade -->
                    </span>
                </div>
                <div class="job-description short">
                    ${job.descricao.substring(0, 100)}... <!-- Mostra uma prévia curta -->
                </div>
                <button class="see-more">Ver mais</button>
                <button href="${job.link}" target="_blank" class="job-link">Acessar Vaga</button>
            </div>
        `;

        // Adiciona evento para expandir a descrição
        const seeMoreBtn = jobElement.querySelector('.see-more');
        const descriptionDiv = jobElement.querySelector('.job-description');

        seeMoreBtn.addEventListener('click', function() {
            if (descriptionDiv.classList.contains('short')) {
                descriptionDiv.classList.remove('short');
                descriptionDiv.innerHTML = job.descricao;  // Mostra a descrição completa
                seeMoreBtn.innerText = 'Ver menos';
            } else {
                descriptionDiv.classList.add('short');
                descriptionDiv.innerHTML = `${job.descricao.substring(0, 100)}...`;  // Mostra descrição curta novamente
                seeMoreBtn.innerText = 'Ver mais';
            }
        });

        resultsDiv.appendChild(jobElement);
    });
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
