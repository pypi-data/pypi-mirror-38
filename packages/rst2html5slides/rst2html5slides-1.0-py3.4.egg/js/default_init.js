var deck = 'deck';
var slide = 'slide';

(function($) {

    var jmpress_init = function() {
        $(deck).jmpress({
            stepSelector: slide
        });
    }
    $(jmpress_init);

})(jQuery);
