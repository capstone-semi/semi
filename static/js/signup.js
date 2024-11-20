document.addEventListener('DOMContentLoaded', () => {
    initializeTermsCheckbox();
    initializeGenderSelection();
    initializeModalControls();
    setupFormValidation();
});

function initializeTermsCheckbox() {
    const termsCheckbox = document.getElementById('termsAgree');
    const submitButton = document.querySelector('button[type="submit"]');
    
    if (termsCheckbox && submitButton) {
        termsCheckbox.addEventListener('change', () => {
            submitButton.disabled = !termsCheckbox.checked;
        });
    }
}

function initializeGenderSelection() {
    const genderButtons = document.querySelectorAll('.gender-btn');
    const genderInput = document.getElementById('gender');
    
    genderButtons.forEach(button => {
        button.addEventListener('click', () => {
            genderButtons.forEach(btn => btn.classList.remove('selected'));
            button.classList.add('selected');
            genderInput.value = button.getAttribute('data-value');
        });
    });
}

function initializeModalControls() {
    const modal = document.getElementById('errorModal');
    const closeModal = document.getElementById('closeModal');
    
    if (modal && closeModal) {
        closeModal.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }
}

function setupFormValidation() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
}

function handleFormSubmit(event) {
    const nickname = document.getElementById('nickname').value.trim();
    const id = document.getElementById('id').value.trim();
    const password = document.getElementById('password').value.trim();
    const age = document.getElementById('age').value.trim();
    const gender = document.getElementById('gender').value.trim();
    const termsAgree = document.getElementById('termsAgree').checked;

    let errorMessage = validateFormInputs(nickname, id, password, age, gender, termsAgree);
    
    if (errorMessage) {
        event.preventDefault();
        showModalError(errorMessage);
    }
}

function validateFormInputs(nickname, id, password, age, gender, termsAgree) {
    if (!nickname) return '닉네임을 입력해주세요.';
    if (!id) return '아이디를 입력해주세요.';
    if (!password) return '비밀번호를 입력해주세요.';
    if (!age) return '나이를 입력해주세요.';
    if (!gender) return '성별을 선택해주세요.';
    if (gender === 'unselected') return '성별을 선택해주세요.';
    if (!termsAgree) return '이용약관 및 개인정보 처리방침에 동의해주세요.';
    return '';
}

function showModalError(message) {
    const modalContent = document.querySelector('.modal-content p');
    const modal = document.getElementById('errorModal');

    if (modalContent && modal) {
        modalContent.innerText = message;
        modal.style.display = 'flex';
    }
}
