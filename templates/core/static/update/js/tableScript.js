$(document).ready(function () {
    $('.slider').bxSlider({
        pagerCustom: '.slider-nav',
        infiniteLoop: true,
        hideControlOnEnd: true,
        captions: true,
        nextText: '',
        prevText: '',
        easing: 'jswing',
    });
});

// поле ввода количества

function toggleInput(button) {
    const inputDiv = button.nextElementSibling; // Находим div с input
    if (inputDiv.style.display === "none" || inputDiv.style.display === "") {
        inputDiv.style.display = "block"; // Показываем input
        button.style.display = "none"; // Скрываем кнопку "Добавить"
    } else {
        inputDiv.style.display = "none"; // Скрываем input
        button.style.display = "block"; // Показываем кнопку "Добавить" при скрытии поля
    }
}

function changeQuantity(button, delta) {
    const inputField = button.parentElement.querySelector('input[type="number"]');
    let currentValue = parseInt(inputField.value);
    currentValue += delta;
    if (currentValue < 0) currentValue = 0; // Убедимся, что значение не отрицательное
    inputField.value = currentValue;
}