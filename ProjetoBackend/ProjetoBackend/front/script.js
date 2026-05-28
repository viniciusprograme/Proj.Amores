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
