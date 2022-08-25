
(function ($) {
    "use strict";

    /*[ Load page ]
    ===========================================================*/
    $(".animsition").animsition({
        inClass: 'fade-in',
        outClass: 'fade-out',
        inDuration: 1500,
        outDuration: 800,
        linkElement: '.animsition-link',
        loading: true,
        loadingParentElement: 'html',
        loadingClass: 'animsition-loading-1',
        loadingInner: '<div class="loader05"></div>',
        timeout: false,
        timeoutCountdown: 5000,
        onLoadEvent: true,
        browser: [ 'animation-duration', '-webkit-animation-duration'],
        overlay : false,
        overlayClass : 'animsition-overlay-slide',
        overlayParentElement : 'html',
        transition: function(url){ window.location.href = url; }
    });
    
    /*[ Back to top ]
    ===========================================================*/
    var windowH = $(window).height()/2;

    $(window).on('scroll',function(){
        if ($(this).scrollTop() > windowH) {
            $("#myBtn").css('display','flex');
        } else {
            $("#myBtn").css('display','none');
        }
    });

    $('#myBtn').on("click", function(){
        $('html, body').animate({scrollTop: 0}, 300);
    });


    /*==================================================================
    [ Fixed Header ]*/
    var headerDesktop = $('.container-menu-desktop');
    var wrapMenu = $('.wrap-menu-desktop');

    if($('.top-bar').length > 0) {
        var posWrapHeader = $('.top-bar').height();
    }
    else {
        var posWrapHeader = 0;
    }
    

    if($(window).scrollTop() > posWrapHeader) {
        $(headerDesktop).addClass('fix-menu-desktop');
        $(wrapMenu).css('top',0); 
    }  
    else {
        $(headerDesktop).removeClass('fix-menu-desktop');
        $(wrapMenu).css('top', posWrapHeader - $(this).scrollTop());
    }

    $(window).on('scroll',function(){
        if($(this).scrollTop() > posWrapHeader) {
            $(headerDesktop).addClass('fix-menu-desktop');
            $(wrapMenu).css('top',0); 
        }  
        else {
            $(headerDesktop).removeClass('fix-menu-desktop');
            $(wrapMenu).css('top', posWrapHeader - $(this).scrollTop());
        } 
    });

    $(window).on('load', function() {
        let path = window.location.pathname;
        path = path.toLowerCase();
        let arr = path.split('/');
        let activeMenu = arr[1].toLowerCase();
        let liObj = $('.main-menu').children('li');

        switch (activeMenu) {
            case '':
                liObj.removeClass('active-menu');
                liObj.eq(0).addClass('active-menu');
                break;
            case 'home':
                liObj.removeClass('active-menu');
                liObj.eq(0).addClass('active-menu');
                break;
            case 'index':
                liObj.removeClass('active-menu');
                liObj.eq(0).addClass('active-menu');
                break;
            case 'products':
                liObj.removeClass('active-menu');
                liObj.eq(1).addClass('active-menu');
                break;
            case 'features':
                liObj.removeClass('active-menu');
                liObj.eq(2).addClass('active-menu');
                break;
            case 'blog':
                liObj.removeClass('active-menu');
                liObj.eq(3).addClass('active-menu');
                break;
            case 'about':
                liObj.removeClass('active-menu');
                liObj.eq(4).addClass('active-menu');
                break;
            case 'contact':
                liObj.removeClass('active-menu');
                liObj.eq(5).addClass('active-menu');
                break;
            default:
                liObj.removeClass('active-menu');
                break;

        }
    });




    /*==================================================================
    [ Menu mobile ]*/
    $('.btn-show-menu-mobile').on('click', function(){
        $(this).toggleClass('is-active');
        $('.menu-mobile').slideToggle();
    });

    var arrowMainMenu = $('.arrow-main-menu-m');

    for(var i=0; i<arrowMainMenu.length; i++){
        $(arrowMainMenu[i]).on('click', function(){
            $(this).parent().find('.sub-menu-m').slideToggle();
            $(this).toggleClass('turn-arrow-main-menu-m');
        })
    }

    $(window).resize(function(){
        if($(window).width() >= 992){
            if($('.menu-mobile').css('display') == 'block') {
                $('.menu-mobile').css('display','none');
                $('.btn-show-menu-mobile').toggleClass('is-active');
            }

            $('.sub-menu-m').each(function(){
                if($(this).css('display') == 'block') {
                    $(this).css('display','none');
                    $(arrowMainMenu).removeClass('turn-arrow-main-menu-m');
                }
            });
                
        }
    });


    /*==================================================================
    [ Show / hide modal search ]*/
    $('.js-show-modal-search').on('click', function(){
        $('.modal-search-header').addClass('show-modal-search');
        $(this).css('opacity','0');
    });

    $('.js-hide-modal-search').on('click', function(){
        $('.modal-search-header').removeClass('show-modal-search');
        $('.js-show-modal-search').css('opacity','1');
    });

    $('.container-search-header').on('click', function(e){
        e.stopPropagation();
    });

    $('.search-header').on('keyup', function (e) {
        if (e.key == 'Enter' || e.keyCode == 13) {
            let keyword = $(this).val();
            if (keyword === '') {
                e.preventDefault();
            }
        }
    });


    /*==================================================================
    [ Isotope ]*/
    var $topeContainer = $('.isotope-grid');
    var $filter = $('.filter-tope-group');

    // filter items on button click
    $filter.each(function () {
        $filter.on('click', 'button', function () {
            var filterValue = $(this).attr('data-filter');
            $topeContainer.isotope({filter: filterValue});
        });
    });

    // init Isotope
    $(window).on('load', function () {
        var $grid = $topeContainer.each(function () {
            $(this).isotope({
                itemSelector: '.isotope-item',
                layoutMode: 'fitRows',
                percentPosition: true,
                animationEngine : 'best-available',
                masonry: {
                    columnWidth: '.isotope-item'
                }
            });
        });
        if (localStorage.getItem('username')) {
            let username = localStorage.getItem('username');
            $('.username').text(username);
            let user = $('.user');
            let login = $('.login');
            login.addClass('hide');
            user.removeClass('hide');
        }
        if (localStorage.getItem('num-cart')) {
            let numCart = localStorage.getItem('num-cart');
            $('.js-show-cart').attr('data-notify', numCart);
        } else {
            $('.js-show-cart').attr('data-notify', 0);
        }
        if (localStorage.getItem('num-wish')) {
            let numWish = localStorage.getItem('num-wish');
            $('.js-show-wish').attr('data-notify', numWish);
        } else {
            $('.js-show-wish').attr('data-notify', 0);
        }
    });

    var isotopeButton = $('.filter-tope-group button');

    $(isotopeButton).each(function(){
        $(this).on('click', function(){
            for(var i=0; i<isotopeButton.length; i++) {
                $(isotopeButton[i]).removeClass('how-active1');
            }

            $(this).addClass('how-active1');
        });
    });

    /*==================================================================
    [ Filter / Search product ]*/
    $('.js-show-filter').on('click',function(){
        $(this).toggleClass('show-filter');
        $('.panel-filter').slideToggle(400);

        if($('.js-show-search').hasClass('show-search')) {
            $('.js-show-search').removeClass('show-search');
            $('.panel-search').slideUp(400);
        }    
    });

    $('.js-show-search').on('click',function(){
        $(this).toggleClass('show-search');
        $('.panel-search').slideToggle(400);

        if($('.js-show-filter').hasClass('show-filter')) {
            $('.js-show-filter').removeClass('show-filter');
            $('.panel-filter').slideUp(400);
        }    
    });


    /*==================================================================
    [ Cart ]*/
    $('.js-show-sidebar').on('click',function(){
        $('.js-sidebar').addClass('show-sidebar');
    });

    $('.js-hide-sidebar').on('click',function(){
        $('.js-sidebar').removeClass('show-sidebar');
    });

    /*==================================================================
    [ +/- num product ]*/
    $('.btn-num-product-down').on('click', function(){
        let numProduct = Number($(this).next().val());
        let input_quantity = $(this).next();
        let idItem = input_quantity.attr('data-id');
        if ($(this).next().hasClass('cart-item')) {
            let csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
            if (numProduct > 1) {
                numProduct -= 1;
                $.ajax({
                    type: 'POST',
                    url: `http://localhost:8000/cart/update/id_item=${idItem}/`,
                    typeData: 'json',
                    crossDomain: true,
                    data: {
                        csrfmiddlewaretoken: csrftoken,
                        idItem: idItem,
                        quantity: numProduct,
                    },
                    success: function (result) {
                        if (result.status_code === 200) {
                            input_quantity.val(numProduct);
                            localStorage.setItem('num-cart', result.num_cart);
                            $('.js-show-cart').attr('data-notify', result.num_cart);
                        }

                    }
                });
            }
        } else {
            if (numProduct > 1) {
                $(this).next().val(numProduct - 1);
            }
        }
    });

    $('.btn-num-product-up').on('click', function(){
        let numProduct = Number($(this).prev().val());
        let input_quantity = $(this).prev();
        let idItem = input_quantity.attr('data-id');
        if ($(this).prev().hasClass('cart-item')) {
            let csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
            numProduct += 1;
            $.ajax({
                type: 'POST',
                url: `http://localhost:8000/cart/update/id_item=${idItem}/`,
                typeData: 'json',
                crossDomain: true,
                xhrFields: {
                    withCredentials: true
                },
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    idItem: idItem,
                    quantity: numProduct,
                },
                success: function (result) {
                    if (result.status_code === 200) {
                        input_quantity.val(numProduct);
                        localStorage.setItem('num-cart', result.num_cart);
                        $('.js-show-cart').attr('data-notify', result.num_cart);
                    }
                }
            });
        } else {
            let productQuantity = input_quantity.attr('data-quantity');
            if (numProduct < productQuantity) $(this).prev().val(numProduct + 1);
        }
    });

    /*==================================================================
    [ Rating ]*/
    $('.wrap-rating').each(function(){
        var item = $(this).find('.item-rating');
        var rated = -1;
        var input = $(this).find('input');
        $(input).val(0);

        $(item).on('mouseenter', function(){
            var index = item.index(this);
            var i = 0;
            for(i=0; i<=index; i++) {
                $(item[i]).removeClass('zmdi-star-outline');
                $(item[i]).addClass('zmdi-star');
            }

            for(var j=i; j<item.length; j++) {
                $(item[j]).addClass('zmdi-star-outline');
                $(item[j]).removeClass('zmdi-star');
            }
        });

        $(item).on('click', function(){
            var index = item.index(this);
            rated = index;
            $(input).val(index+1);
        });

        $(this).on('mouseleave', function(){
            var i = 0;
            for(i=0; i<=rated; i++) {
                $(item[i]).removeClass('zmdi-star-outline');
                $(item[i]).addClass('zmdi-star');
            }

            for(var j=i; j<item.length; j++) {
                $(item[j]).addClass('zmdi-star-outline');
                $(item[j]).removeClass('zmdi-star');
            }
        });
    });
    
    /*==================================================================
    [ Show modal1 ]*/
    $('.js-show-modal1').on('click', function(e){
        e.preventDefault();
        let idProduct = $(this).attr('data-id');
        $.ajax({
            type: 'GET',
            url: `http://localhost:8000/product/id=${idProduct}/`,
            dataType: 'json',
            success: function (result) {
                if (result.product) {
                    let item = $('.slick3-dots img').attr('src', result.product.image);
                    $('.img-slick3').attr('src', result.product.image);
                    $('.hov-btn3').attr('href', result.product.image);
                }
            }
        });
        $('.js-modal1').addClass('show-modal1');
    });

    $('.js-hide-modal1').on('click', function(){
        $('.js-modal1').removeClass('show-modal1');
    });

/*==================================================================
    [ header ]*/
     $('.user').on('click', function (e) {
        e.preventDefault();
        let userSetting = $('.user-setting');
        userSetting.removeClass('hide');
    });
    $('.user-setting').on('mouseleave', function (e) {
        e.preventDefault();
        $(this).addClass('hide');
    });

    $('.categories').on('mouseenter', function (e) {
        e.preventDefault();
        let listCategories = $('.list-categories');
        listCategories.removeClass('hide');
    });
    $('.list-categories').on('mouseleave', function (e) {
        e.preventDefault();
        $(this).addClass('hide');
    });

    /*==================================================================
    [ logout ]*/
    $('.logout').on('click', function (e) {
        $.ajax({
            url: 'http://127.0.0.1:8000/logout/',
            type: 'GET',
            typeData: 'json',
            success: function (result) {
                if (result.code === 200) {
                    localStorage.removeItem('username');
                    $('.username').text('login');
                    $('.user-setting').addClass('hide');
                    $('.user').removeClass('hide');
                    localStorage.removeItem('num-cart');
                    localStorage.removeItem('num-wish');
                    window.location.href = `http://127.0.0.1:8000/`;
                }
            }
        });
    });

    /*==================================================================
    [ add item to wish ]*/
    $('.js-addwish-detail').on('click', function (e) {
        e.preventDefault();
        let added = $(this).hasClass('js-addedwish-detail');
        if (added) return;
        let id_product = $(this).attr('data-tooltip');
        if (id_product > 0) {
            $.ajax({
                type: 'GET',
                url: `http://127.0.0.1:8000/wish/add/id=${id_product}/`,
                dataType: 'json',
                crossDomain: true,
                success: function (result) {
                    //show inform add item to wish
                    $('.js-addwish-detail').each(function() {
                        let nameProduct = $('.js-name-detail').text();
                        swal(nameProduct, "is added to wishlist !", "success");
                        $(this).addClass('js-addedwish-detail');
                        // $(this).off('click');
                    });
                    if (result.num_wish) {
                        $('.js-show-wish').attr('data-notify', result.num_wish);
                        localStorage.setItem('num-wish', result.num_wish);
                    }
                },
            });
        }

    });


})(jQuery);