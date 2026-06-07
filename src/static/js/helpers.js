/**
 * Realiza una solicitud AJAX para operaciones CRUD en un voucher.
 * @param {Object} formData - Los datos a enviar en la solicitud.
 * @param {string} url - La URL a la que se enviará la solicitud.
 * @returns {Promise} - Una promesa que se resuelve con la respuesta del servidor o se rechaza con un error.
 */
function ejecutar_Solicitud(formData, url) {

    return new Promise(function (resolve, reject) {
        $.ajax({
            type: 'POST',
            url: url,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify(formData),
            success: function (response) {
                // Si el backend retorna éxito
                if (response.success) {
                    resolve(response);
                } else {
                    // Si el backend retorna un error controlado (ej: 409)
                    reject(new Error(response.error || "Error desconocido"));
                }
            },
            error: function (error) {
                // Captura el mensaje de error del backend
                const errorMessage = error.responseJSON?.error || "Error al procesar la solicitud";
                reject(new Error(errorMessage));
            }
        });
    });
}