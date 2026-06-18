function vo_methodCreate() {
    $('#guardar').off('click').on('click', async function (e) {
        e.preventDefault();
        clearErrors();

        const spinner = document.getElementById('loading-spinner');
        spinner.style.display = 'block';

        let isValid = true;
        const requiredFields = ['#name'];

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

        try {
            await enviarDatosAlServidor(spinner);
        } catch (error) {
            spinner.style.display = 'none';
            Swal.fire("Error", error.message, "error");
        }
    });
}

function showError(fieldId, message) {
    const errorElement = $(`${fieldId}`).siblings('.text-danger');
    errorElement.text(message).show();
}

function clearErrors() {
    $('.text-danger').hide();
}

function enviarDatosAlServidor(spinner) {
    const idcrop = $('#idcrop').val().trim();

    const formData = {
        idcrop: idcrop,
        name: $('#name').val().trim(),
        scientific_name : $('#scientific_name').val().trim(),
        description: $('#description').val().trim()
    };

    ejecutar_Solicitud(formData, '/crops/page')
        .then(response => {
            spinner.style.display = 'none';
            if (response.success) {
                Swal.fire({
                    title: "Exito",
                    text: response.message,
                    icon: "success",
                    willClose: () => window.location.href = '/crops'
                });
            } else {
                throw new Error(response.error);
            }
        })
        .catch(error => {
            spinner.style.display = 'none';
            Swal.fire({
                icon: "error",
                title: "Error..",
                text: error.message || "Error al procesar la solicitud"
            });
        });
}
