function continueLogin() {
    const userId = document.getElementById('id').value.trim();
    const password = document.getElementById('password').value.trim();

    if (!userId || !password) {
        showErrorModal("입력 오류", "아이디와 비밀번호를 모두 입력해주세요.");
        return;
    }

    fetch('login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: userId, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // 로그인 성공, 홈 페이지로 리다이렉트
            window.location.href = '/home';
        } else {
            // 로그인 실패, 모달창 표시
            showErrorModal("로그인 실패", data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showErrorModal("오류", "로그인 중 오류가 발생했습니다.");
    });
}


function showErrorModal(title, message) {
    const modal = document.getElementById('errorModal');
    document.getElementById('modalTitle').innerText = title;
    document.getElementById('modalMessage').innerText = message;
    modal.style.display = 'flex';
}

// 모달 닫기 버튼 이벤트 리스너
document.getElementById('closeModal').addEventListener('click', function() {
    document.getElementById('errorModal').style.display = 'none';
});

// 모달 외부 클릭 시 모달 닫기
window.onclick = function(event) {
    const modal = document.getElementById('errorModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}
