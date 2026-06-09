
function asignarConfiguraciones(url = "/farms/data"){
    // Declarar la variable en un ámbito superior (nivel de función)
    let id_farm = null;

     $(document).ready(function(){
            const table =$('#table_id').DataTable({
            responsive:true,
            order:[[0,'desc']],
            ajax:{
                // "Server-side processing"
                url:url,
                type:"GET",
                dataSrc: ""
            },
                    columns :[
                        { data: 'id',title:'id' },
                        { data: 'name',title:'Nombre' },
                        { data: 'location',title:'Ubicación' },
                        { data: 'area_hectares' ,title:'Hectáreas'},
                        { data: 'fecha_creacion' ,title:'fecha_creacion'}
                    ],

                     dom: 'Bfrtip',
                     buttons: [ 'excel','pdf','print' ]
                });
                    // Evento para seleccionar fila
                    $('#table_id tbody').on('click', 'tr', function() {
                        if ($(this).hasClass('selected')) {
                            $(this).removeClass('selected');
                            id_farm = null; // Resetear al deseleccionar
                        } else {
                            table.$('tr.selected').removeClass('selected');
                            $(this).addClass('selected');
                            const rowData = table.row(this).data();
                            id_farm = rowData.id; // Asignar valor
                            console.log("ID seleccionado:", id_farm);
                        }
                 });

            });

        //********************************************
        //Botón agregar (para cargar la pagina Mant Usuario)
            $('#agregar').on('click', function () {
                window.location.href = '/farms/farm-createupdate';
            });
           //*******************************************************
        //Boton Editar (para cargar la pagina de Edicion)

            $('#editar').on('click', function (e) {
                    if (typeof id_farm === 'undefined' || id_farm === null) {
            Swal.fire({
                title: "Fundo",
                text: "Seleccione una fila",
                icon: "warning"
            });
            return;
        }

        // Redirige directamente con el ID como query param
        //IDOR (Insecure Direct Object Reference)
        window.location.href = `/farms/farm_page?id=${id_farm}`;
        });
};
