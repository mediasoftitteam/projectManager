$("#materials").click(function (e) {
    let display = $("#companies-submenu").css('display');
    if(display !== 'none') {
        $("#companies-submenu").toggle(350)
    }
    $("#materials-submenu").toggle(350)
});
$(document).click(function(e) {
    let target = e.target;
    if (!$(target).is('#materials') && !$(target).parents().is('#materials')) {
        $("#materials-submenu").hide(350)
    }
});
$(document).click(function(e) {
    let target = e.target;
    if (!$(target).is('#companies') && !$(target).parents().is('#companies')) {
        $("#companies-submenu").hide(350)
    }
});

$("#companies").click(function () {
    let display = $("#materials-submenu").css('display');
    if(display !== 'none') {
        $("#materials-submenu").toggle(350)
    }
   $("#companies-submenu").toggle(350)
});
// $(".search-box").hover(function () {
//     if ($(".search-txt").css('width') === '250px'){
//         $(".fa-search").css('color', 'black')
//     }
// });
$("#header-toggler").click(function () {
   let navbar = $("#inner-header");
   let togglerIcon = $("#toggler-icon");
   if(navbar.css('right') === '-250px') {
       navbar.css('right', '0px');
       togglerIcon.removeClass('fa-bars').addClass('fa-times');
   } else {
       navbar.css('right', '-250px');
       togglerIcon.removeClass('fa-times').addClass('fa-bars');
   }
});

let x = `${($("footer").height() + $("header").height())}px`;
$("main").css('min-height', `calc(100vh - ${x})`);
let width = window.matchMedia("(min-width: 768px)");
if(width.matches){
    $(window).scroll(function () {
        let scroll = $(window).scrollTop();
        if (scroll >= 50) {
            $("#inner-header").addClass('fixed-top');
            $("main").css('margin-top', '75px');
            $("#materials-submenu").css('top', '50px');
            $("#companies-submenu").css('top', '50px');
        } else {
            $("#inner-header").removeClass('fixed-top');
            $("main").css('margin-top', '20px');
            $("#materials-submenu").css('top', '100px');
            $("#companies-submenu").css('top', '100px');
        }
    })
}
