// scripts.js
// 오늘 날짜 가져오기
const today = new Date();
const todayDate = today.getDate();
const currentMonth = today.getMonth() + 1; // 월은 0부터 시작

// 현재 월 표시
const monthElement = document.getElementById("current-month");
monthElement.textContent = `${currentMonth}월`;

// 오늘 날짜 강조
const dateElement = document.getElementById(`date-${todayDate}`);
if (dateElement) {
    dateElement.classList.add("selected");
}