var tamano = 0;
var grupo_actual="";
var grupo_anterior="";
var borrado = 0;


var tableSelect = {
  multipleRows: function (event) {
    var td = event.target;
    var rowElement = $(td).parent();
    
    var tableBody = rowElement.parent();
    this.clearSelection();

    if (!event.shiftKey && !event.ctrlKey && !event.altKey) {
      if ($(rowElement).hasClass("selected")){ //deseleccionar si ya estaba seleccionado sin necesidad de presionar ctrl
        rowElement.removeClass("selected");
      }
      else{
        rowElement.addClass("selected");
        tableBody.children().removeClass("lastSelected");
        rowElement.addClass("lastSelected");
      }
    } 
    else if (event.ctrlKey || event.altKey) {
      if (rowElement.hasClass("selected")) {
        rowElement.removeClass("selected");
      } 
      else {
        rowElement.addClass("selected");
        tableBody.children().removeClass("lastSelected");
        rowElement.addClass("lastSelected");
      }
    } 
    else if (event.shiftKey) {
      var lastSelectedIndex = tableBody.children().index(tableBody.find(".lastSelected"));
      var clickedIndex = tableBody.children().index(rowElement);

      if (lastSelectedIndex == -1) {
        lastSelectedIndex = clickedIndex;
      }
      var minIndex = Math.min(lastSelectedIndex, clickedIndex);
      var maxIndex = Math.max(lastSelectedIndex, clickedIndex);

      // deselect all rows outside the selection interval
      var deselectedRows = tableBody.children().filter(function (index) {
        return index < minIndex || index > maxIndex;
      });

      deselectedRows.removeClass("selected");

      // select all rows in the selection interval
      var selectedRows = tableBody.children().filter(function (index) {
      return index >= minIndex && index <= maxIndex;
      });
      selectedRows.addClass("selected");
    }
  },

  singleRow: function (event,id) {
    var td = event.target;  
    var rowElement = $(td).parent();
    var tableBody = rowElement.parent();
    this.clearSelection();
    //caso despues de borrar
    if (borrado == 1){ 
      grupo_anterior=""; 
      grupo_actual = $(td).text();         
      $("#tabla_sin_grupos tbody tr").each(function(){          
        $(this).fadeIn(4);
        
      });
      borrado=1-borrado;        
    //caso sin borrar y solo cambiar de grupo
    }
    else{        
      grupo_anterior=grupo_actual;
      grupo_actual = $(td).text();
      //desvanesco el grupo anterior para mostrar el nuevo seleccionado
      $("#tabla_grupos_asignados tbody tr").each(function(){
        $(this).removeClass("selected");
        if ($(this).hasClass(grupo_anterior)){
            $(this).fadeOut(4);
        }
      });
      $("#tabla_grupos_asignados tbody tr").each(function(){
          if ($(this).hasClass(grupo_actual)){
            $(this).fadeIn(4);
          }
      });
    }
    //selecciono el nuevo grupo.
    tableBody.children().removeClass("selected");
    rowElement.addClass("selected");
  },

  clearSelection: function () {
    var sel;
    if (document.selection && document.selection.empty) {
      try {
        document.selection.empty();
      } catch (error) {}
    } 
    else if (window.getSelection) {
      sel = window.getSelection();
      if (sel && sel.removeAllRanges) {
        sel.removeAllRanges();
      }
    }
  }
};


$(document).ready(function () {

//TABLA 1
  $("#tabla_sin_grupos tbody td").attr('unselectable', 'on');
  $("#tabla_sin_grupos tbody").click(function (event) {
    tableSelect.multipleRows(event);
    });

// TABLA 2
  $("#tabla_grupos_asignados").fadeOut(0);
  $("#tabla_grupos_asignados tbody tr").attr('unselectable', 'on');
  $("#tabla_grupos_asignados tbody").click(function (event) {
    tableSelect.multipleRows(event);
    });

// TABLA 3
  $("#tabla_de_grupos tbody td").attr('unselectable', 'on');
  $("#tabla_de_grupos tbody").click(function (event) {    
    tableSelect.singleRow(event);
    if ($("#tabla_de_grupos tbody").children().hasClass('selected')){ 
      $("#tabla_grupos_asignados").fadeIn(0);
    }
    else{
      $("#tabla_grupos_asignados").fadeOut(0);
    }
  });

// MODAL CARGAR DIST
  $("#tabla_cargar_distribucion tbody td").attr('unselectable', 'on');
  $("#tabla_cargar_distribucion tbody").click(function (event) {    
    var td = event.target;  
    var rowElement = $(td).parent();
    var tableBody = rowElement.parent();
    tableBody.children().removeClass("selected");
    rowElement.addClass("selected");
  });

// BOTONES
  $("#asignar").click(function (event){
    asignar_alumno(event);
  });

  $("#desasignar").click(function (event){    
    desasignar_alumno(event);
  });

  $("#crear_grupo").click(function (event){
    crear_grupo(event);
  });
});

function asignar_alumno(event){
   $("#tabla_de_grupos tbody tr").each(function(){
    if ($(this).hasClass("selected")){              
      $("#tabla_sin_grupos tbody tr").each(function (index){
        if ($(this).hasClass("selected")){                  
          $(this).addClass(grupo_actual);
          jQuery($(this)).appendTo('#tabla_grupos_asignados tbody');
          $(this).removeClass("selected");
        }
      });
    }
  });
}

function desasignar_alumno(event){
  $("#tabla_de_grupos tbody tr").each(function(){
    if ($(this).hasClass("selected")){
      $("#tabla_grupos_asignados tbody tr").each(function (index){                     
        if ($(this).hasClass("selected")){                         
          var c1=$(this).text();                          
          $(this).removeClass(grupo_actual);
          jQuery($(this)).appendTo('#tabla_sin_grupos tbody');
          $(this).removeClass("selected");
        }
      });
    }
  });
  ordenar_alfabeticamente(event);
}

function crear_grupo(){
  var campo = "Grupo "+(++tamano);
  var num_grupo=0;

  var boton = new boton_eliminar_grupo(campo,num_grupo);
  var parent = $('<tr><td>'+campo+'</td><td></td></tr>').children(':last-child').append(boton.boton).end();
  
  //

  $("#tabla_de_grupos > tbody:last").append(parent);
  $("#tabla_de_grupos tbody").children(':last-child').children(':first-child').trigger('click');
}

function boton_eliminar_grupo(campo,num_grupo){
  this.boton = $("<button/>",{
    class:'btn btn-mini btn-danger',
    click:function (event){ 
      borrado = 1-borrado;      
    
      $("#grupo").text(''); //seteo el label en donde se encontraba que grupo estaba asignandose
      
      var grupotxt = $(this).parent().parent().children("td").text(); //dato de la primera columna Grupo X
      var grupo = parseInt(grupotxt.substring(grupotxt.indexOf(" ")+1)); //parsear a entero        
      
      num_grupo = grupo;            
      
      $("#tabla_grupos_asignados tbody tr").each(function (event){
        if ($(this).hasClass("selected")){
          $(this).removeClass("selected");
        }                    
        if ($(this).hasClass(grupotxt)){
          $(this).removeClass(grupotxt);
          jQuery($(this)).appendTo('#tabla_sin_grupos tbody');
        }                     
        
      });

      num_grupo = grupo;
      var campo = "";   
      while(num_grupo<tamano){
        campo = "Grupo "+(num_grupo+1);              
        $("#tabla_grupos_asignados tbody tr").each(function(){                                  
          $(this).fadeOut(4);
          if ($(this).hasClass(campo)){                    
            $(this).removeClass(campo);                  
            $(this).addClass("Grupo "+(num_grupo));
          }
        });
        num_grupo++;
      }
      tamano--; //cantidad de filas en la tabla de grupos
      grupo_actual="";

    
      $(this).parent().parent().parent().children(":last-child").remove();
      $(this).parent().parent().parent().children("tr").removeClass("selected"); 
      ordenar_alfabeticamente(event);
      
    } //termina evento click para eliminar grupo

  }); // termina el boton
  var icon = $("<i class='icon-remove icon-white'></i>");
  this.boton.append(icon);
}
    