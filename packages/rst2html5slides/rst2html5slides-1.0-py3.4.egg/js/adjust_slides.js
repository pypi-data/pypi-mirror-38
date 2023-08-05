(function($) {

    // var deck = 'div#impress'; // should be defined at ?mpress_init.js
    var slide = 'div.step';
    var totalSlides = 0;

    var paginarSlide = function(index, elem) {
        $(elem).append('<div class="pagination"><span class="pagenum">' + (index + 1) +
                       '</span> / <span class="pagetotal">' + totalSlides+ '</span></div>');
        $(".pagination_container select")
        $("<option />", {
            "value"   : index,
            "text"    : (index + 1) + '. ' + elem.id
        }).appendTo(".pagination_container select");
    };

    function updatePagination(activeSlide) {
        if (!activeSlide) {
            return
        }
        var pageNum = $(activeSlide).find('.pagenum').text();
        $('.pagination_container select').val(parseInt(pageNum) - 1);
    }

    $(function() {
        $('<div class="pagination_container">\n\
    <div class="container">\n\
        <span id="previous_slide">&lt;</span>\n\
        <select></select>\n\
        <span id="next_slide">&gt;</span>\n\
    </div>\n\
</div>').prependTo('body');
        $('#previous_slide').on('click', function() {
            var activeSlide = impress().prev();
            updatePagination(activeSlide);
        });
        $('#next_slide').on('click', function() {
            var activeSlide = impress().next();
            updatePagination(activeSlide);
        });
        $('.pagination_container select').on('change', function() {
            var activeSlide = impress().goto(parseInt(this.value));
            updatePagination(activeSlide);
        });
        totalSlides = $(slide).length;
        $(slide).each(paginarSlide);
    });


    // ref: http://tjvantoll.com/2012/06/15/detecting-print-requests-with-javascript/

    var beforePrint = function() {
        // clean up inline styles
        $('html').removeAttr('style');
        $('body').removeAttr('style');
        $(deck).removeAttr('style');
        $(slide).removeAttr('style');
        var slides = $(deck + ' > div').html();
        $(deck + ' > div').remove()
        $(deck).append(slides);
    };

    var afterPrint = function() {
    // firing just after beforePrint!
    // It's not sure if this can be changed at all:
    // http://stackoverflow.com/questions/9920397/window-onbeforeprint-and-window-onafterprint-get-fired-at-the-same-time/9920784#9920784
    //    jmpress_init();
    };

    // if (window.matchMedia) {
    //     var mediaQueryList = window.matchMedia('print');
    //     mediaQueryList.addListener(function(mql) {
    //         if (mql.matches) {
    //             beforePrint();
    //         } else {
    //             afterPrint();
    //         }
    //     });
    // }

    window.onbeforeprint = beforePrint;
    window.onafterprint = afterPrint;

})(jQuery);
