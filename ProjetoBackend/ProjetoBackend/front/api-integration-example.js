/**
 * Integração com a API do Backend - Amores Instituto
 * 
 * Este arquivo contém exemplos de como integrar o frontend com os endpoints da API
 * Copie as funções e adapte ao seu script.js conforme necessário
 */

// ============================================
// ⚙️ CONFIGURAÇÃO BASE
// ============================================

const API_BASE_URL = 'http://localhost:8000/api/v1';

// ============================================
// 🏛️ FUNÇÕES PARA INSTITUIÇÃO
// ============================================

/**
 * Carrega as informações da instituição para preencher o modal "Sobre"
 */
async function carregarInfoInstituicao() {
    try {
        const response = await fetch(`${API_BASE_URL}/instituicao/principal/`);
        
        if (!response.ok) {
            throw new Error(`Erro: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Atualizar modal com dados reais
        console.log('Dados da instituição:', data);
        
        // Você pode usar os dados assim:
        // document.querySelector('.about-text').textContent = data.descricao;
        // document.querySelector('.pix-key-container span').textContent = `Chave PIX (${data.tipo_chave_pix}): ${data.chave_pix}`;
        
        return data;
    } catch (error) {
        console.error('Erro ao carregar informações:', error);
        return null;
    }
}

/**
 * Copia a chave PIX da API em vez de usar valor fixo
 */
async function copyPixFromAPI() {
    try {
        const instituicao = await carregarInfoInstituicao();
        
        if (instituicao) {
            navigator.clipboard.writeText(instituicao.chave_pix).then(() => {
                const copyBtn = document.querySelector('.btn-copy');
                const originalText = copyBtn.innerHTML;
                copyBtn.innerHTML = '<i class="fa-solid fa-check"></i> Copiado!';
                copyBtn.style.backgroundColor = '#00A859';
                
                setTimeout(() => {
                    copyBtn.innerHTML = originalText;
                    copyBtn.style.backgroundColor = '';
                }, 2000);
            });
        }
    } catch (error) {
        console.error('Erro ao copiar PIX:', error);
        alert('Erro ao copiar a chave PIX, tente manualmente.');
    }
}

// ============================================
// 📅 FUNÇÕES PARA AGENDAMENTO
// ============================================

/**
 * Submeter formulário de agendamento para a API
 */
async function submitAgendamento(event) {
    event.preventDefault();
    
    // Coletar dados do formulário
    const nome = document.getElementById('name').value;
    const data_visita = document.getElementById('date').value;
    const horario_preferencial = document.getElementById('time').value + ':00'; // Adiciona segundos
    
    // Validar dados
    if (!nome || !data_visita || !horario_preferencial) {
        alert('Por favor, preencha todos os campos!');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/agendamentos/api/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                nome: nome,
                data_visita: data_visita,
                horario_preferencial: horario_preferencial
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            console.log('Agendamento criado:', data);
            alert(`Sua visita foi agendada com sucesso!\n\nData: ${data_visita}\nHorário: ${horario_preferencial}\n\nEntraremos em contato em breve.`);
            closeModal('scheduleModal');
            
            // Limpar formulário
            document.querySelector('.schedule-form').reset();
        } else {
            console.error('Erro na resposta:', data);
            alert('Erro ao agendar visita. Tente novamente!');
        }
    } catch (error) {
        console.error('Erro ao enviar agendamento:', error);
        alert('Erro de conexão. Verifique se o servidor está rodando!');
    }
}

/**
 * Listar todos os agendamentos (para uso administrativo)
 */
async function listarAgendamentos() {
    try {
        const response = await fetch(`${API_BASE_URL}/agendamentos/api/listar/`);
        
        if (!response.ok) {
            throw new Error(`Erro: ${response.status}`);
        }
        
        const agendamentos = await response.json();
        console.log('Agendamentos:', agendamentos);
        
        return agendamentos;
    } catch (error) {
        console.error('Erro ao listar agendamentos:', error);
        return [];
    }
}

// ============================================
// 🔌 INTEGRAÇÃO COM O CÓDIGO EXISTENTE
// ============================================

/**
 * Use essas funções para atualizar o script.js existente:
 * 
 * 1. Substitua a função copyPix() por:
 *    - copyPixFromAPI()
 * 
 * 2. Atualize o evento onsubmit do formulário de agendamento:
 *    - De: onsubmit="event.preventDefault(); alert(...)"
 *    - Para: onsubmit="submitAgendamento(event)"
 * 
 * 3. Carregue os dados ao iniciar a página:
 *    - Adicione no final do script.js: carregarInfoInstituicao();
 */

// ============================================
// 📊 EXEMPLOS DE USO
// ============================================

/*
// Exemplo 1: Carregar dados ao abrir modal "Sobre"
function openModalAbout() {
    carregarInfoInstituicao().then(data => {
        if (data) {
            // Atualizar elementos do modal com dados reais
            openModal('aboutModal');
        }
    });
}

// Exemplo 2: Verificar status da API
async function verificarStatusAPI() {
    try {
        const response = await fetch(`${API_BASE_URL}/instituicao/`);
        if (response.ok) {
            console.log('✅ API está respondendo corretamente');
        } else {
            console.error('❌ API retornou erro:', response.status);
        }
    } catch (error) {
        console.error('❌ Erro de conexão com a API:', error);
    }
}

// Chamar ao carregar a página
document.addEventListener('DOMContentLoaded', verificarStatusAPI);
*/
