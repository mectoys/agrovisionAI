function vo_methodCreate() {
    $('#guardar').off('click').on('click', async function (e) {
        e.preventDefault();
        clearErrors();

        const spinner = document.getElementById('loading-spinner');
        spinner.style.display = 'block';

        let isValid = true;
        const requiredFields = ['#name', '#location'];
        const areaInput = $('#area_hectares');

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

        const areaRawValue = areaInput.val().trim().replace(',', '.');
        const areaValue = Number(areaRawValue);

        if (areaRawValue === '') {
            showError('#area_hectares', 'Este campo es obligatorio');
            spinner.style.display = 'none';
            return;
        }

        if (Number.isNaN(areaValue) || areaValue <= 0) {
            showError('#area_hectares', 'Ingresa un numero decimal valido mayor a 0');
            spinner.style.display = 'none';
            return;
        }

        areaInput.val(areaRawValue);

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
    const idfarm = $('#idfarm').val().trim();

    const formData = {
        idfarm: idfarm,
        name: $('#name').val().trim(),
        location: $('#location').val().trim(),
        area_hectares: $('#area_hectares').val()
    };

    ejecutar_Solicitud(formData, '/farms/page')
        .then(response => {
            spinner.style.display = 'none';
            if (response.success) {
                Swal.fire({
                    title: "Exito",
                    text: response.message,
                    icon: "success",
                    willClose: () => window.location.href = '/farms'
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
