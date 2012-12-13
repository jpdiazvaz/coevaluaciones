var alumnos_asignados = new Array();
var tamano = 0;
var grupo_actual="";
var grupo_anterior="";
var borrado = 0;
var c  = 0;
function is_alumn(alumnos, ID){  
  for (var i = 0; i < alumnos.length; i++) {
    if (alumnos[i][0]  == ID){
      return 1;
    }  
  };
  return 0;
}
function get_alumn(alumnos){
 for (var i = 0; i < alumnos.length; i++) {
    if (alumnos[i][0]  == ID){
      return 1;
    }  
  };
  return 0; 
}


var tableSelect = {

multipleRows: function (event) {
    var td = event.target;
    var rowElement = $(td).parent();
    var tableBody = rowElement.parent();
    this.clearSelection();

    if (!event.shiftKey && !event.ctrlKey && !event.altKey) {
      //tableBody.children().removeClass("selected"); agregue el if-else y borre este
      if ($(rowElement).hasClass("selected")){ //deseleccionar si ya estaba seleccionado sin necesidad de presionar ctrl
        rowElement.removeClass("selected");
      }
      else{
        rowElement.addClass("selected");
        tableBody.children().removeClass("lastSelected");
        rowElement.addClass("lastSelected");
      }
    } else if (event.ctrlKey || event.altKey) {
        if (rowElement.hasClass("selected")) {
          rowElement.removeClass("selected");
        } else {
            rowElement.addClass("selected");
            tableBody.children().removeClass("lastSelected");
            rowElement.addClass("lastSelected");
          }
    } else if (event.shiftKey) {
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

singleRow: function (event) {
      var td = event.target;  
      var rowElement = $(td).parent();
      var tableBody = rowElement.parent();
      this.clearSelection();




//caso despues de borrar
      if (borrado == 1){ 
        grupo_anterior=""; 
        grupo_actual = $(td).text();        
         borrado=1-borrado;
      //caso sin borrar y solo cambiar de grupo
      }else{        
        grupo_anterior=grupo_actual;
        grupo_actual = $(td).text();
        //desvanesco el grupo anterior para mostrar el nuevo seleccionado
        $("#tabla_grupos_asignados tbody tr").each(function(){
          $(this).removeClass("selected");
          if ($(this).hasClass(grupo_anterior)){
              $(this).fadeOut(4);
          }
        });

      }

      $("#grupo").text('').append("<strong> Integrantes "+grupo_actual+":</strong>");

      $("#tabla_grupos_asignados tbody tr").each(function(){
            if ($(this).hasClass(grupo_actual)){
              $(this).fadeIn(4);
            }
        });


     
      
      //selecciono el nuevo grupo.
      tableBody.children().removeClass("selected");
      rowElement.addClass("selected");
    },

clearSelection: function () {
    var sel;
    if (document.selection && document.selection.empty) {
        try {
            document.selection.empty();
        } catch (error) {
          // ignore error. workaround for bug in IE8
        }
        } else if (window.getSelection) {
            sel = window.getSelection();
            if (sel && sel.removeAllRanges) {
              sel.removeAllRanges();
            }
        }
    }
};
//VARIABLE TABLESELECT

//FUNCIONES A EVENTOS CLICKS !
$(document).ready(function () {

// in order to not select ranges of text in IE8,
// set the attribute unselectable to "on" for the table cell
//TABLA 1
  $("#tabla_sin_grupos tbody td").attr('unselectable', 'on');

  $("#tabla_sin_grupos tbody").click(function (event) {
    tableSelect.multipleRows(event);
    });

// TABLA 2
  $("#tabla_grupos_asignados tbody td").attr('unselectable', 'on');
//cosa nueva que agregare  

  $("#tabla_grupos_asignados tbody").click(function (event) {
    tableSelect.multipleRows(event);
    });

// TABLA 3
  $("#tabla_de_grupos tbody td").attr('unselectable', 'on');

  $("#tabla_de_grupos tbody").click(function (event) { 
    tableSelect.singleRow(event);
    });

/* FUNCIONA
  $("#tabla_sin_grupos tbody tr").click(function(){
    $(this).fadeOut(400, function(){
            $(this).remove();
        });
  });

FALTA ORDENAR LOS DATOS DENTRO DE LA TABLA
*/

    $("#asignar").click(function (event){
         // $("#tabla_sin_grupos").find("tr:eq(2) .selected").remove();
         $("#tabla_de_grupos tbody tr").each(function(){
            if ($(this).hasClass("selected")){              
              $("#tabla_sin_grupos tbody tr").each(function (index){
                  //var campo1,campo2;
                  //campo1 = $(this).children("td").text();
                  //campo2 = $(this).next("td").text();
                  if ($(this).hasClass("selected")){                  
                      //$(this).fadeOut(40);
                      $(this).addClass(grupo_actual);
                      jQuery($(this)).appendTo('#tabla_grupos_asignados tbody');
                      $(this).removeClass("selected");
                      //$(this).fadeOut(400, function(){
                      //    $(this).remove();
                      // });
                     // $("tabla_grupos_asignados tbody").appendChild($(fila));
                      //$("#tabla_grupos_asignados tbody").append("<tr><td > <p>"+campo1+"</p> </td><td> <p> "+campo2+" </p> </td></tr>");
                  }
              });
            }

          });

    });


    $("#desasignar").click(function (event){    

        $("#tabla_de_grupos tbody tr").each(function(){
            if ($(this).hasClass("selected")){
                  //var grupo = $(this).text();
                  $("#tabla_grupos_asignados tbody tr").each(function (index){
                      //var campo1,campo2;
                      //campo1 = $(this).children("td").text();
                      //campo2 = $(this).next("td").text();
                      if ($(this).hasClass("selected")){
                          
                          var c1=$(this).text();                          
                          $(this).removeClass(grupo_actual);
                          //$(this).fadeOut(400, function(){
                            //$(this).remove();
                        //});
                          jQuery($(this)).appendTo('#tabla_sin_grupos tbody');
                          $(this).removeClass("selected");
                          //funciona
                          //$("#tabla_sin_grupos tbody").append($("<tr> <td>"+campo1+"</td><td  nowrap>"+campo2+"</td> </tr>"));
                      }
                  });
            }
        });

    });

    $("#borrar_grupo").click(function (event){  
          borrado = 1-borrado;        
          $("#grupo").text('');
          $("#tabla_de_grupos tbody tr").each(function (index){                                        
              if ($(this).hasClass("selected")){ //debe estar seleccionado un grupo
                  //desasignar alumnos del grupo que se elimina
                    $("#tabla_grupos_asignados tbody tr").each(function(){
                      var classname = $(this).attr("class");
                      alert(classname);
                      if ($(this).hasClass("selected")){
                        $(this).removeClass("selected");  
                      }                    
                      if ($(this).hasClass(grupo_actual)){
                        $(this).removeClass(grupo_actual);
                        jQuery($(this)).appendTo('#tabla_sin_grupos tbody');
                      }                     
                      
                    });
                  $(this).fadeOut(4, function(){
                    $(this).remove(); //desasignar el grupo de esos alumnos y dejarlos en la otra tabla!
                    //tamano--;
                  });                  
              }
          });
    });    
    //falta agregar el grupo
    $("#crear_grupo").click(function (event){
          //var tamano = $("#tabla_de_grupos tr").length;          
        var campo = "Grupo "+(++tamano);          
        $("#tabla_de_grupos tbody").append("<tr><td>"+campo+"</td></tr>");

    });    
});
