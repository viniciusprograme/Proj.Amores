function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('active');
        document.body.style.overflow = '';
    }
}

function copyPix() {
    const pixKey = "00.000.000/0001-00"; // Chave Padrão
    navigator.clipboard.writeText(pixKey).then(() => {
        const copyBtn = document.querySelector('.btn-copy');
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = '<i class="fa-solid fa-check"></i> Copiado!';
        copyBtn.style.backgroundColor = '#00A859';
        
        setTimeout(() => {
            copyBtn.innerHTML = originalText;
            copyBtn.style.backgroundColor = '';
        }, 2000);
    }).catch(err => {
        console.error('Falha ao copiar: ', err);
        alert('Erro ao copiar a chave PIX, tente manualmente.');
    });
}

// Integação com o Back-end
document.addEventListener('DOMContentLoaded', () => {
    const scheduleForm = document.getElementById('schedule-form');
    if (scheduleForm) {
        scheduleForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Agendando...';
            submitBtn.disabled = true;
            
            const name = document.getElementById('name').value;
            const date = document.getElementById('date').value;
            const time = document.getElementById('time').value;
            
            const data = {
                nome: name,
                data_visita: date,
                horario_preferencial: time
            };
            
            try {
                // A URL padrão de desenvolvimento do backend Django é http://127.0.0.1:8000
                const response = await fetch('http://127.0.0.1:8000/api/v1/agendamentos/api/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    alert('Sua visita foi agendada com sucesso! Entraremos em contato em breve.');
                    closeModal('scheduleModal');
                    scheduleForm.reset();
                } else {
                    const errorData = await response.json();
                    console.error('Erro retornado pela API:', errorData);
                    alert('Houve um erro ao agendar sua visita. Por favor, tente novamente ou verifique se os dados estão corretos.');
                }
            } catch (error) {
                console.error('Erro na requisição:', error);
                alert('Erro de conexão com o servidor. Verifique se o backend está rodando em http://127.0.0.1:8000.');
            } finally {
                submitBtn.innerHTML = originalBtnText;
                submitBtn.disabled = false;
            }
        });
    }
});
