
//Función que gestiona el formulario de cambio de Password
function vc_adminChangePassword(url){
     $(document).ready(function() {
        // 1. Alternar visibilidad de contraseña
        $('.toggle-pass').on('click', function() {
            const input = $('#new_password');
            const icon = $(this).find('i');
            if (input.attr('type') === 'password') {
                input.attr('type', 'text');
                icon.removeClass('bi-eye').addClass('bi-eye-slash');
            } else {
                input.attr('type', 'password');
                icon.removeClass('bi-eye-slash').addClass('bi-eye');
            }
        });

        // 2. Medidor de fuerza (Visual)
        $('#new_password').on('input', function() {
            let val = $(this).val();
            let strength = 0;
            if (val.length >= 8) strength += 25;
            if (val.match(/[A-Z]/)) strength += 25;
            if (val.match(/[0-9]/)) strength += 25;
            if (val.match(/[^a-zA-Z0-9]/)) strength += 25;

            const bar = $('#password-strength .progress-bar');
            bar.css('width', strength + '%');
            bar.removeClass('bg-danger bg-warning bg-success');

            if (strength <= 50) bar.addClass('bg-danger');
            else if (strength <= 75) bar.addClass('bg-warning');
            else bar.addClass('bg-success');
        });

        // 3. Envío y Validación Final
        $('#formCambiarPass').on('submit', function(e) {
            e.preventDefault();

            const pass = $('#new_password').val();
            const confirm = $('#confirm_password').val();
            const current = $('#current_password').val();

            // Validaciones de cliente
            if (pass.length < 8) {
                Swal.fire("Seguridad", "La nueva contraseña debe tener al menos 8 caracteres.", "warning");
                return;
            }

            if (pass !== confirm) {
                Swal.fire("Error", "Las contraseñas nuevas no coinciden.", "error");
                return;
            }

            // Petición a Flask
            Swal.fire({
                title: '¿Actualizar contraseña?',
                text: "Se cerrará tu sesión por seguridad tras el cambio.",
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Sí, cambiar',
                confirmButtonColor: '#0d6efd'
            }).then((result) => {
                if (result.isConfirmed) {
                    $.ajax({
                        url: url,
                        type: "POST",
                        contentType: "application/json",
                        data: JSON.stringify({
                            current_pass: $('#current_password').val(),
                            new_pass: $('#new_password').val()
                        }),
                        success: function(res) {
                            // Esto se ejecuta si Flask devuelve un 200
                            if(res.success) {
                                Swal.fire("¡Éxito!", res.message, "success")
                                    .then(() => window.location.href = "/logout");
                            }
                        },
                        error: function(xhr) {
                            // Esto captura el 400, 401, 500, etc.
                            const res = xhr.responseJSON; // Flask envía el JSON del error aquí
                            const mensajeError = (res && res.error) ? res.error : "Error inesperado";

                            Swal.fire("Validación", mensajeError, "warning");
                            $('#current_password').val('').focus(); // Limpia y pone el cursor ahí
                            // Usamos 'warning' porque es un error de usuario (clave mal escrita)
                        }
                    });
                }
            });
        });
   });

};

// "/usuario/update_password",
