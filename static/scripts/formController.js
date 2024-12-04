const options = document.getElementById('options');
const toggleOptions = document.getElementById('toggleOptions')
const closeButton1 = document.getElementById('close1')
const closeButton2 = document.getElementById('close2')
$('html').removeClass('modal-open');
document.getElementById('toggleOptions').onclick = function () {
    options.style.display = 'flex';
    toggleOptions.style.display = 'none'
    $('body').removeClass('modal-open');
    $('#emailModal, #callModal').on('hidden.bs.modal', function () {
        $(this).find('form')[0].reset(); // Сбрасываем форму
        if ($('.modal:visible').length === 0) {
            document.body.classList.remove('modal-open'); // убираем класс, если нет открытых модалей
        }
    });
};

document.getElementById('close').onclick = function () {
    options.style.display = 'none';
    toggleOptions.style.display = 'flex'

    $('body').removeClass('modal-open');
    $('#emailModal, #callModal').on('hidden.bs.modal', function () {
        $(this).find('form')[0].reset(); // Сбрасываем форму
        if ($('.modal:visible').length === 0) {
            document.body.classList.remove('modal-open'); // убираем класс, если нет открытых модалей
        }
    });
};

document.getElementById('close1').onclick = function () {
    options.style.display = 'none';
    toggleOptions.style.display = 'flex'
    $('body').removeClass('modal-open');
    $('#emailModal, #callModal').on('hidden.bs.modal', function () {
        $(this).find('form')[0].reset(); // Сбрасываем форму
        if ($('.modal:visible').length === 0) {
            document.body.classList.remove('modal-open'); // убираем класс, если нет открытых модалей
        }
    });

};

document.getElementById('close2').onclick = function () {
    options.style.display = 'none';
    toggleOptions.style.display = 'flex'
    $('body').removeClass('modal-open');
    $('#emailModal, #callModal').on('hidden.bs.modal', function () {
        $(this).find('form')[0].reset(); // Сбрасываем форму
        if ($('.modal:visible').length === 0) {
            document.body.classList.remove('modal-open'); // убираем класс, если нет открытых модалей
        }
    });

};