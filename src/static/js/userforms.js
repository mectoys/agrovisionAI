    function vo_methodCreate() {
    // Asegurar un solo listener
    $('#guardar').off('click').on('click', async function (e) {
        e.preventDefault();
        clearErrors();
        const spinner = document.getElementById('loading-spinner');
        spinner.style.display = 'block';

        let isValid = true;
        const requiredFields = ['#username', '#email'];

        // Solo validar clave y reclave si los campos están visibles (modo creación)
        if ($('#clave').length && $('#clave').is(':visible')) {
            requiredFields.push('#clave', '#reclave');
        }

        requiredFields.forEach(field => {
            const input = $(field);
            if (input.length && input.val().trim() === '') {
                showError(field, 'Este campo es obligatorio');
                isValid = false;
            }
        });

        if (!isValid) {
            spinner.style.display = 'none';
            return;
        }

        // Validar email
        const email = $('#email').val().trim();
        if (email && !isValidEmail(email)) {
            showError('#email', 'Ingresa un correo válido');
            isValid = false;
        }

        // Validar contraseñas
        if ($('#clave').length && $('#clave').is(':visible')) {
            const clave = $('#clave').val();
            const reclave = $('#reclave').val();
            if (clave !== reclave) {
                showError('#reclave', 'Las contraseñas no coinciden');
                isValid = false;
            }
        }

        if (!isValid) {
            spinner.style.display = 'none';
            return;
        }

        // Enviar datos (asíncrono)
        try {
            await enviarDatosAlServidor(spinner);
        } catch (error) {
            spinner.style.display = 'none';
            Swal.fire("Error", error.message, "error");
        }
    });
}
    // Funciones auxiliares
    function showError(fieldId, message) {
        const errorElement = $(`${fieldId}`).siblings('.text-danger');
        errorElement.text(message).show();
    }

    function clearErrors() {
        $('.text-danger').hide();
    }

    function isValidEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }

 function enviarDatosAlServidor(spinner){

        const iduser = $('#iduser').val().trim();
        const isEdit = iduser && iduser !== "0"; // modo edición si existe iduser válido

        const formData = {
            iduser: iduser,
            username: $('#username').val().trim(),
            email: $('#email').val().trim(),
            rol: $('#rol').val()
        };
        console.log(formData);
        // Solo añadir clave y reclave si es modo creación (no edición)
        if (!isEdit) {
            formData.clave = $('#clave').val();
            formData.reclave = $('#reclave').val();
        }

        ejecutar_Solicitud(formData, '/usuario/page') //anterior  '/usuario/create'
            .then(response => {
            spinner.style.display = 'none'; // Ocultar en éxito
                if (response.success) {
                    Swal.fire({
                        title: "Éxito",
                        text: response.message,
                        icon: "success",
                        willClose: () => window.location.href = '/usuario'
                    });
                } else {
                    throw new Error(response.error); // Forzar entrada al catch
                }
            })
            .catch(error => {
            spinner.style.display = 'none'; // Ocultar en error
                Swal.fire({
                    icon: "error",
                    title: "Error..",
                    text: error.message || "Error al procesar la solicitud"
                });
            });

  }
