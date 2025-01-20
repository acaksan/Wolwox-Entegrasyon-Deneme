$(document).ready(function() {
    // Sidebar toggle
    $('#sidebarCollapse').on('click', function() {
        $('#sidebar').toggleClass('active');
        $('#content').toggleClass('active');
    });

    // Mobil menü için otomatik kapanma
    if ($(window).width() <= 768) {
        $('#sidebar').addClass('active');
        $('#content').addClass('active');
    }

    // Pencere boyutu değiştiğinde kontrol et
    $(window).resize(function() {
        if ($(window).width() <= 768) {
            $('#sidebar').addClass('active');
            $('#content').addClass('active');
        }
    });

    // Menü öğelerine tıklama
    $('#sidebar ul li a').click(function(e) {
        // Alt menü varsa toggle yap
        var $submenu = $(this).next('ul');
        if ($submenu.length) {
            e.preventDefault();
            $submenu.slideToggle();
            $(this).parent().toggleClass('active');
        }
    });

    // Aktif menü öğesine scroll
    if ($('#sidebar li.active').length) {
        var activeItem = $('#sidebar li.active');
        var sidebarScrollTop = $('#sidebar').scrollTop();
        var itemOffset = activeItem.offset().top;
        var sidebarOffset = $('#sidebar').offset().top;
        
        $('#sidebar').animate({
            scrollTop: sidebarScrollTop + itemOffset - sidebarOffset - 100
        }, 200);
    }
});
