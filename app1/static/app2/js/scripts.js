function load_button(btn) {
   $("#"+btn).addClass("m-progress");
   $("#"+btn).attr("disabled", "true");
}

function normal_button(btn) {
   $("#"+btn).removeClass("m-progress");
   document.getElementById(btn).disabled = false;
}

function voltar() { history.go(-1); }

window.onscroll = function(){
    var top = window.pageYOffset || document.documentElement.scrollTop;

    if( top > 50 ) {
        $("#img_topo").css("display", "block");
    } else {
        $("#img_topo").css("display", "none");
    }
}

$(document).ready(function() {
    $('#img_topo').click(function(){
        $('html, body').animate({scrollTop:0}, 'slow');
        return false;
    });

    $('#menu_fixo').scrollToFixed();

    $(".dropdown").hover(
        function() { $(this).addClass("open");
        },
        function() { $(this).removeClass("open");
    });

    $('.dropdown').click(function () {
        var target = $(this).find('img');
        target.attr('src', 'imagens/ArrowDown_menu.png');
    });
 });

var $btnAumentar = $("#btnAumentar");
var $btnDiminuir = $("#btnDiminuir");
var $elemento = $("body #content").find("*");
var fonts = [];

function obterTamanhoFonte() {
    for (var i = 0; i < $elemento.length; i++) {
        fonts.push(parseFloat($elemento.eq(i).css('font-size')));
    }
}
obterTamanhoFonte();
$btnAumentar.on('click', function() {
    for (var i = 0; i < $elemento.length; i++) {
        ++fonts[i];
        $elemento.eq(i).css('font-size', fonts[i]);
    }
});

$btnDiminuir.on('click', function() {
    for (var i = 0; i < $elemento.length; i++) {
        --fonts[i];
        $elemento.eq(i).css('font-size', fonts[i]);
    }
});

$('#btnSublinhar').click(function () {
    if ($("#content").hasClass('links_sublinhados')) {
        $("#content").removeClass('links_sublinhados');
    } else {
        $("#content").addClass('links_sublinhados');
    }
});

$('#btnGrayscale').click(function () {
    if ($("#content").hasClass('grayscale')) {
        $("#content").removeClass('grayscale');
    } else {
        $("#content").addClass('grayscale');
    }
});

$('#btnReset').click(function () {
    localStorage.setItem("contrastState", false);
    $("body").removeClass("contrast");
    $("#content").removeClass('grayscale');
    $("#content").removeClass('links_sublinhados');

    for (var i = 0; i < $elemento.length; i++) {
        $elemento.eq(i).css('font-size', '');
    }
});

(function () {
    var Contrast = {
        storage: 'contrastState',
        cssClass: 'contrast',
        currentState: null,
        check: checkContrast,
        getState: getContrastState,
        setState: setContrastState,
        toogle: toogleContrast,
        updateView: updateViewContrast
    };

    window.toggleContrast = function () { Contrast.toogle(); };

    Contrast.check();

    function checkContrast() {
        this.updateView();
    }

    function getContrastState() {
        return localStorage.getItem(this.storage) === 'true';
    }

    function setContrastState(state) {
        localStorage.setItem(this.storage, '' + state);
        this.currentState = state;
        this.updateView();
    }

    function updateViewContrast() {
        var body = document.body;

        if (this.currentState === null)
            this.currentState = this.getState();

        if (this.currentState)
            body.classList.add(this.cssClass);
        else
            body.classList.remove(this.cssClass);
    }

    function toogleContrast() {
        this.setState(!this.currentState);
    }
})();

function showAutoCloseTimerMessage(titulo, texto, tempo, tipo) {
    swal({
        title: titulo,
        text: texto,
        timer: tempo,
        html: true,
        type: tipo,
        showConfirmButton: false
    });
}

function showNotification(message, type, from, align, icone){
    $.notify({
        icon: icone,
        message: message

    },{
        type: type,
        timer: 4000,
        placement: {
            from: from,
            align: align
        }
    });
}