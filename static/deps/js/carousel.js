const thumbnailsDivWidth = 526;
const thumbnailWidth = 150;

function moveImagesLeft(){
    const thumbnailImages = document.querySelectorAll('.thumbnails img');
    const itemToRemove = thumbnailImages[0]
    document.querySelector('.thumbnails').appendChild(itemToRemove)
    itemToRemove.remove
}

function moveImagesRight(){
    const thumbnailImages = document.querySelectorAll('.thumbnails img');
    const itemToRemove = thumbnailImages[thumbnailImages.length - 1]
    const firstItem = thumbnailImages[0]
    document.querySelector('.thumbnails').insertBefore(itemToRemove, firstItem)
    itemToRemove.remove
}

function updateCarousel(direction) {
    if (direction === 'next') {
        moveImagesLeft()
    } else if (direction === 'prev') {
        moveImagesRight()
    }
}

function changeImage(src) {
    document.getElementById('mainImage').src = src;
}

document.addEventListener('DOMContentLoaded', function() {
    // add click events on carousel left-right buttons
    const prevControl = document.getElementById('prevControl');
    const nextControl = document.getElementById('nextControl');
    prevControl.addEventListener('click', () => updateCarousel('prev'));
    nextControl.addEventListener('click', () => updateCarousel('next'));

    // move all thumbnails to the center of div.
    const thumbnailsWidth = thumbnailWidth * document.querySelectorAll('.thumbnails img').length
    const currentOffset = thumbnailsDivWidth < thumbnailsWidth
        ? (thumbnailsDivWidth - thumbnailsWidth) / 2
        :0 ;
    document.querySelector('.thumbnails').style.transform = `translateX(${currentOffset}px)`;
});


