$(function(){
    $("#btn_novo").click(function(){
        window.location = "/things";
    })
    var tipo_busca = getUrlParameter('tipo_busca');
    $("#tipo_busca").val(tipo_busca);
    if(tipo_busca == '4'){
         $("#dado_busca").hide();
         $("#dado_busca2").show();
         var dado_busca2 = getUrlParameter('dado_busca2');
         $("#dado_b").val(dado_busca2);
    }else{
    $("#dado_busca").show();
        $("#dado_busca2").hide();
        var dado_busca = getUrlParameter('dado_busca');
        $("#dado_busca").val(dado_busca);
    }

    $("#tipo_busca").change(function(){
        var valor_selecionado = $(this).val();
        if(valor_selecionado == '4'){
            $("#dado_busca").hide();
            $("#dado_busca2").show();
        }else{
            $("#dado_busca").show();
            $("#dado_busca2").hide();

        }

    })
})

var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};