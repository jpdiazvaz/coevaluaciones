//MODIFICAR ESTO, NO BORRA BIEN LOS ELEMENTOS...

/*
$(document).ready(function() {
    $("tbody td").click(function(e) {
        var currentCellText = $(this).text();
        //alert(currentCellText);
    });
});


function reasignar_grupos(){    
    table = document.getElementById("tabla_de_grupos");
    var largo2 = table.rows.length; 


    for (var i = largo2; i>=1;i--){
        var hijo  = table.rows.item(0); 
        var currenttext = table.rows[i].cells[0].nodeValue;
        //alert(currenttext.data);

         
        //hijo.childNodes[0].innerText = "Grupo "+i;
        //alert(hijo.nodeValue);
    }
}

function agregar_grupo(ind) {   
   //valor++;   
   //grupos[tamano]  = valor;
    tamano++;
    var myRow = document.all.tabla_de_grupos.insertRow();
    var myCell = myRow.insertCell();  
    myCell.innerText = "Grupo "+(tamano);
        
    
   //grupos.sort(function(a,b){ return b-a;});
  
}

function borrar_todo(){	

    
	var Parent = document.getElementById("tabla_de_grupos");
    while(Parent.hasChildNodes())
    {
    	Parent.removeChild(Parent.firstChild);
    }
	
}
function borrar_grupo(ind) {
    document.all.tabla_de_grupos.deleteRow(ind);
    //indice = grupos.indexOf(ind);
    //Array.removeAt(grupos, ind);
    //grupos.splice(ind,1);
    //document.all.tabla_de_grupos.moveRow(0, 3);
    tamano--;
    //borrar_todo();
}
//HASTA AQUI LLEGA ESO DE LA TABLA GRUPO
*/