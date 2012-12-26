var alumnos_asignados = new Array();
var c  = 0;
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

/*      var texto = $(td).text();
      $("#grupo").text('').append("<strong> Integrantes "+texto+":</strong>");
      tableBody.children().each(function(){
        if ($(this).hasClass("selected")){
          var numgrupo = $(this).text(); //obtengo el grupo anterior seleccionado
          var num_grupo_arr = numgrupo.split(" ");
          var numgrupo = parseInt(num_grupo_arr[1]);
          var alumnos = new Array();
          $("#tabla_grupos_asignados tbody tr").each(function (){
              var campo1,campo2;              
              campo1 = $(this).children("td").text();
              campo2 = $(this).next("td").text();
              group[0] = campo1;
              group[1] = campo2;              
              alumnos_asignados[numgrupo-1][c++] = group;
              $(this).hide();
          
          });
          c = 0;
        }
      }); */
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

var tamano = 0;

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

          $("#tabla_sin_grupos tbody tr").each(function (index){
              var campo1,campo2;
              campo1 = $(this).children("td").text();
              campo2 = $(this).next("td").text();
              if ($(this).hasClass("selected")){                  
                  //$(this).fadeOut(40);

                  jQuery($(this)).appendTo('#tabla_grupos_asignados tbody');
                  $(this).removeClass("selected");
                  //$(this).fadeOut(400, function(){
                  //    $(this).remove();
                  // });
                 // $("tabla_grupos_asignados tbody").appendChild($(fila));
                  //$("#tabla_grupos_asignados tbody").append("<tr><td > <p>"+campo1+"</p> </td><td> <p> "+campo2+" </p> </td></tr>");
              }
          });

    });


    $("#desasignar").click(function (event){    

          $("#tabla_grupos_asignados tbody tr").each(function (index){
              var campo1,campo2;
              if ($(this).hasClass("selected")){
                  campo1 = $(this).children("td").text();
                  campo2 = $(this).next("td").text();

                  //$(this).fadeOut(400, function(){
                    //$(this).remove();
                //});
                  jQuery($(this)).appendTo('#tabla_sin_grupos tbody');
                  $(this).removeClass("selected");
                  //funciona
                  //$("#tabla_sin_grupos tbody").append($("<tr> <td>"+campo1+"</td><td  nowrap>"+campo2+"</td> </tr>"));
              }
          });

    });

    $("#borrar_grupo").click(function (event){
          $("#tabla_de_grupos tbody tr").each(function (index){
              var campo;
              campo = $(this).children("td").text();              
              if ($(this).hasClass("selected")){              
                  $(this).fadeOut(40, function(){
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
        for (var i = 0; i < alumnos_asignados.length; i++) {
          var c1,c2;
          alert("grupo: "+i);
          for (var j = 0; j < alumnos_asignados[i].length; j++) {
                      c1 = alumnos_asignados[i][j][0];
                      c2 = alumnos_asignados[i][j][1];
                      alert("alumno: "+j+" -  ID: "+c1 +" - Nombre: "+ c2);
          };                   
          

          
     
        };
      
    });    



});
