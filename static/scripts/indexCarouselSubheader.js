$(document).ready(function(){
    $('.slider').slick({
      autoplay: true,
      autoplaySpeed: 5000, // Adjust the speed as needed (in milliseconds)
      speed: 500,          // Adjust animation speed as needed
      slidesToShow: 1,      // Only show one slide at a time
      slidesToScroll: 1,    // Scroll one slide at a time
      arrows: false,       // Hide arrows
      dots: false,          // Show dots at the bottom
    });
});