$(document).ready(function(event){
    $('.slider').slick({
        dots: false,
        infinite: true,
        speed: 800,
        slidesToShow: 1,
        slidesToScroll: 1,
        asNavFor: '.slider-nav',
        arrows: false,
    });

    $('.slider-nav').slick({
        dots: false,
        infinite: true,
        speed: 800,
        slidesToShow: 4, 
        slidesToScroll: 1,
        asNavFor: '.slider',
        focusOnSelect: true,
        arrows: false,
    });
    $('.slider-arrows .slick-prev1').click(function() {
        $('.slider').slick('slickPrev');
    });
    
    $('.slider-arrows .slick-next1').click(function() {
        $('.slider').slick('slickNext');
    });
});



// поле ввода количества

function toggleInput(button) {
    const inputDiv = button.nextElementSibling; // Находим div с input
    if (inputDiv.style.display === "none" || inputDiv.style.display === "") {
        inputDiv.style.display = "flex"; // Показываем input
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