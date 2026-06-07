
function vc_asignarConfiguraciones(url = "/usuario/data"){
    // Declarar la variable en un ámbito superior (nivel de función)
    let iduser = null;

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
                        { data: 'username',title:'username' },
                        { data: 'email',title:'email' },
                        { data: 'fecha_creacion' ,title:'fecha_creacion'},
                        { data: 'rol_id' ,title:'rol_id'}
                    ],

                     dom: 'Bfrtip',
                     buttons: [ 'excel','pdf','print' ]
                });
                    // Evento para seleccionar fila
                    $('#table_id tbody').on('click', 'tr', function() {
                        if ($(this).hasClass('selected')) {
                            $(this).removeClass('selected');
                            iduser = null; // Resetear al deseleccionar
                        } else {
                            table.$('tr.selected').removeClass('selected');
                            $(this).addClass('selected');
                            const rowData = table.row(this).data();
                            iduser = rowData.id; // Asignar valor
                            console.log("ID seleccionado:", iduser);
                        }
                 });

            });

        //********************************************
        //Botón agregar (para cargar la pagina Mant Usuario)
            $('#agregar').on('click', function () {
                window.location.href = '/usuario/page_user';
            });
           //*******************************************************
        //Boton Editar (para cargar la pagina de Edicion)

            $('#editar').on('click', function (e) {
                    if (typeof iduser === 'undefined' || iduser === null) {
            Swal.fire({
                title: "Usuario",
                text: "Seleccione una fila",
                icon: "warning"
            });
            return;
        }

        // Redirige directamente con el ID como query param
        //IDOR (Insecure Direct Object Reference)
        window.location.href = `/usuario/page_user?id=${iduser}`;
        });
};
