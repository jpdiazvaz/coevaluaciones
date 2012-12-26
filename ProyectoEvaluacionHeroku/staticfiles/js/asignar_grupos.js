
$(document).ready(function() {

  $('.checkbox').change(function() {
    $.getJSON('obtener_alumnos',{id: $(this).attr('id'), checked: $(this).children().attr('checked')},
    function(datos){
        var id = datos[0];
        var checked = datos[1];
        
        if(checked=="checked"){
        	for (var i = 2; i < datos.length; i+=2) {		    	
        		$('#tabla_sin_grupos tbody').append('<tr class="'+id+'"><td>'+datos[i]+'</td><td>'+datos[i+1]+'</td></tr>');
                
        	};
        }
        else{
            $('#tabla_sin_grupos tbody tr').each(function(){
                if($(this).hasClass(id)) $(this).remove();
            });
            $('#tabla_grupos_asignados tbody tr').each(function(){
                if($(this).hasClass(id)) $(this).remove();
            });
        }
        ordenar_alfabeticamente(event);
    });
    return false;
  });



  function func_nueva_distribucion(){
      $("#tabla_de_grupos tbody tr").each(function (){
          var gr = $(this).text();            
          $("#tabla_grupos_asignados tbody tr").each(function(){
              if ($(this).hasClass(gr)){
                  $(this).removeClass("selected");
                  $(this).removeClass("lastSelected");
                  $(this).removeClass(gr);
                  jQuery($(this)).appendTo('#tabla_sin_grupos tbody');
                  $(this).fadeIn(4);
              }
          });
      });
      $("#tabla_de_grupos tbody tr").remove();
      tamano = 0;
      ordenar_alfabeticamente(event);
  };



  function func_cargar_distribucion(){
    if ($("#tabla_cargar_distribucion tbody").children().length <= 0){
      return;
    }
    var ramos = "";
    $('.checkbox').each(function() {
      var chk = $(this).children().attr('checked');
      if ( chk == "checked" ){
          ramos += ($(this).attr('id')) + ",";
      }
    });
    var distribucion;
    $("#tabla_cargar_distribucion tbody tr").each(function(){
      if ($(this).hasClass('selected')){
        distribucion = $(this).children(":first-child");
        distribucion = distribucion.text();
      }
    });

    $.getJSON('cargar_distribucion',{distribucion:distribucion},
      function(datos){
        /// limpiar todo ///
        func_nueva_distribucion();
        /// crear grupos ///
        var grupos_totales = datos[datos.length - 1];
        for (var i=0;i < grupos_totales;i++){
          crear_grupo();
        }
        /// asignar alumnos a grupos ///
        for (var i=0;i < datos.length;i+=2){
          $("#tabla_sin_grupos tbody tr").each(function(){
            if ($(this).children(":first-child").text() == datos[i]){  
              $(this).addClass("Grupo "+datos[i+1]);
              $(this).appendTo('#tabla_grupos_asignados tbody');
              $(this).fadeOut(4);
            }
          });
        }
        $("#tabla_de_grupos tbody").children(':last-child').children(':first-child').trigger('click');
      });
  };

  function solicitar_distribuciones(){
    var ramos = "";
    $('.checkbox').each(function() {
        var chk = $(this).children().attr('checked');
        if ( chk == "checked" ){
            ramos += ($(this).attr('id')) + ",";
        }
    });
    $.getJSON('solicitar_distribuciones',{ramos:ramos},
      function(datos){
        $('#tabla_cargar_distribucion tbody').empty();
        /// llenar tabla con los datos ///
        for (var i=0;i< datos.length;i+=3){
          $('#tabla_cargar_distribucion tbody').append('<tr class = "'+datos[i]+'"><td>'+datos[i]+'</td><td>'+datos[i+1]+'</td><td>'+datos[i+2]+'</td></tr>');
        }

        $("#msg-error").remove();
        if ($("#tabla_cargar_distribucion tbody").children().length <= 0){
          $('#tabla_cargar_distribucion').fadeOut(0);
          $('#tabla_cargar_distribucion').parent().append('<div id="msg-error"><center><p><strong>No hay distribuciones disponibles</strong></p></center></div>');
        }
        else{
          $('#tabla_cargar_distribucion').fadeIn(0);
        }
      });
  };


  function func_guardar_distribucion() {
      var informacion = new Array();
      var c = 0;
      $("#tabla_grupos_asignados tbody tr").each(function(){
          if ($(this).hasClass("selected")){ $(this).removeClass("selected");}
          if ($(this).hasClass("lastSelected")){ $(this).removeClass("lastSelected");}
          dato1 = $(this).attr("class").split(" ");
          dato2 = $(this).text().split(" ");
          ramo = dato1[0];
          grupo_asignado = dato1[2];
          rut_alumno  =dato2[0].substring(0,dato2[0].indexOf("-")+2);
          informacion[c] = new Array();
          informacion[c][0] = ramo;
          informacion[c][1] = grupo_asignado;
          informacion[c][2] = rut_alumno;
          c++;
      });
     $.getJSON('guardar_distro',$.param ({informacion:informacion},true), function(datos){
      alert(datos);
     });
  };


   $('#guardar_distribucion').click(func_guardar_distribucion);
   $("#solicitar-distribuciones").click(solicitar_distribuciones);
   $("#cargar-distribucion").click(func_cargar_distribucion);
   $("#nueva-distribucion").click(func_nueva_distribucion);
});

