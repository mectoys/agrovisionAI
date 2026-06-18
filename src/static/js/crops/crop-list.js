
function asignarConfiguraciones(url = "/crops/data"){
    // Declarar la variable en un ámbito superior (nivel de función)
    let id_crop = null;

     $(document).ready(function(){
            const table =$('#table_id').DataTable({
            processing: true,
            responsive:true,
            order:[[0,'desc']],
            ajax:{
                // "Server-side processing"
                url:url,
                type:"GET",
                dataSrc: ""
            },
                    language: {
                        processing: '<div class="chakra-datatable-loader"><span class="spinner-border spinner-border-sm text-success me-2" role="status" aria-hidden="true"></span>Cargando fundos...</div>',
                        loadingRecords: 'Cargando Cultivos...',
                        emptyTable: 'No hay fundos registrados',
                        zeroRecords: 'No se encontraron Cultivos'
                    },
                    columns :[
                        { data: 'id',title:'id' },
                        { data: 'name',title:'Nombre' },
                        { data: 'scientific_name',title:'Nombre Científico' },
                        { data: 'description' ,title:'Descripción'},
                        { data: 'fecha_creacion' ,title:'fecha_creacion'}
                    ],

                     dom: 'Bfrtip',
                     buttons: [ 'excel','pdf','print' ]
                });
                    // Evento para seleccionar fila
                    $('#table_id tbody').on('click', 'tr', function() {
                        if ($(this).hasClass('selected')) {
                            $(this).removeClass('selected');
                            id_crop = null; // Resetear al deseleccionar
                        } else {
                            table.$('tr.selected').removeClass('selected');
                            $(this).addClass('selected');
                            const rowData = table.row(this).data();
                            id_crop = rowData.id; // Asignar valor

                        }
                 });

            });

        //********************************************
        //Botón agregar (para cargar la pagina Mant Usuario)
            $('#agregar').on('click', function () {
                window.location.href = '/crops/crop-createupdate';
            });
           //*******************************************************
        //Boton Editar (para cargar la pagina de Edicion)

            $('#editar').on('click', function (e) {
                    if (typeof id_crop === 'undefined' || id_crop === null) {
            Swal.fire({
                title: "Cultivo",
                text: "Seleccione una fila",
                icon: "warning"
            });
            return;
        }
        // Redirige directamente con el ID como query param
        //IDOR (Insecure Direct Object Reference)
        window.location.href = `/crops/crop-createupdate?id=${id_crop}`;
        });
};
