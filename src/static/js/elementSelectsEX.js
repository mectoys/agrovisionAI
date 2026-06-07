 //Funcion para cargar opciones de manera asícrona

 /*
 loadOptions() es una función asíncrona (usa AJAX). Entonces, cuando llega a selectValueforSelectedIndex(...),
 el <select> aún no tiene opciones cargadas, por eso no encuentra la opción a seleccionar y no funciona.
 */
function loadOptions(idSelect, url, valorPropiedad, callback = null) {
    // Mostrar spinner
    const spinner = document.getElementById('loading-spinner');
    spinner.style.display = 'block';

    $.ajax({
        type: 'GET',
        url: url,
        success: function (data) {
            // Limpiar opciones actuales
            $(idSelect).empty();

            // Agregar opción por defecto
            $(idSelect).append('<option value="">Seleccione una opción</option>');

            // Agregar nuevas opciones
            for (var i = 0; i < data.length; i++) {
                $(idSelect).append(
                    '<option value="' + data[i][valorPropiedad] + '">' + data[i].descripcion + '</option>'
                );
            }

            spinner.style.display = 'none';

             if (callback) {
                callback();  // Ejecutar la función una vez que las opciones ya se han cargado
            }

        },

        error: function (xhr, status, error) {
            console.error("Error al cargar opciones:", error);
            spinner.style.display = 'none';

            // Opcional: notificación visual
            alert("No se pudieron cargar los datos. Intente nuevamente.");
        }
    });
}



 /*
 * Selecciona un valor en un elemento select basado en su valor, usado para EDICION de formularios.
 * @param {string} idFieldName - El valor que se desea seleccionar en el elemento select.
 * @param {string} selectInputName - El nombre o ID del elemento select.
 */
function selectValueforSelectedIndex(idFieldName,selectInputName)
    {
       var selectElement = document.getElementById(selectInputName); // Obtener el elemento select

        // Iterar sobre las opciones y seleccionar la correcta
        for (var i = 0; i < selectElement.options.length; i++) {

            if (selectElement.options[i].value === idFieldName) {

                selectElement.selectedIndex = i;
                break;
            }
         }
    }