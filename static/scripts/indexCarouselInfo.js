$(document).ready(function(){
    $('.sliderInfo .slider ').slick({
      autoplay: true,          // Enable autoplay
      autoplaySpeed: 5000,      // Set autoplay speed (2 seconds)
      infinite: true,          // Enable infinite looping
      slidesToShow: 1,          // Show one slide at a time
      slidesToScroll: 1,        // Scroll one slide at a time
      arrows: false,           // Hide prev/next arrows
      dots: true,              // Show dots
      dotsClass: 'slick-dots', // Use the .slick-dots class (if necessary)
      appendDots: '.slick-dots' // Append the dots to this specific container
    });
  });
  
  