(function($) {
    $(document).ready(function(event) {
        var $slider = $('.slider'),
            $sliderNav = $('.slider-nav');

        $slider.slick({
            dots: false,
            infinite: true,
            speed: 800,
            slidesToShow: 1,
            slidesToScroll: 1,
            asNavFor: $sliderNav,
            arrows: false,
        });

        $sliderNav.slick({
            dots: false,
            infinite: true,
            speed: 800,
            slidesToShow: 4,
            slidesToScroll: 1,
            asNavFor: $slider,
            focusOnSelect: true,
            arrows: false,
        });

        $('.slider-arrows .slick-prev1').click(function() {
            $slider.slick('slickPrev');
        });

        $('.slider-arrows .slick-next1').click(function() {
            $slider.slick('slickNext');
        });
    });
})(jQuery);