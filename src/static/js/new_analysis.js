const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const previewImage = document.getElementById('previewImage');
const placeholder = document.getElementById('placeholder');
const openCameraBtn = document.getElementById('openCamera');
const captureBtn = document.getElementById('captureBtn');
const imageUpload = document.getElementById('imageUpload');

let stream;

async function openCamera() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert(
            'La camara no esta disponible en esta URL. Abre la app en localhost o usa HTTPS para permitir el acceso a la camara.'
        );
        return;
    }

    try {
        stream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false,
        });

        video.srcObject = stream;
        video.classList.remove('d-none');
        previewImage.classList.add('d-none');
        canvas.classList.add('d-none');
        placeholder.classList.add('d-none');
    } catch (error) {
        alert('No se pudo acceder a la camara. Revisa permisos del navegador y usa localhost o HTTPS.');
        console.error(error);
    }
}

function capturePhoto() {
    if (!stream) {
        alert('Primero debes abrir la camara');
        return;
    }

    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    previewImage.src = canvas.toDataURL('image/png');
    previewImage.classList.remove('d-none');
    video.classList.add('d-none');
    canvas.classList.add('d-none');
}

function loadLocalImage(event) {
    const file = event.target.files[0];
    if (!file) {
        return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
        previewImage.src = e.target.result;
        previewImage.classList.remove('d-none');
        video.classList.add('d-none');
        canvas.classList.add('d-none');
        placeholder.classList.add('d-none');
    };

    reader.readAsDataURL(file);
}

if (openCameraBtn) {
    openCameraBtn.addEventListener('click', openCamera);
}

if (captureBtn) {
    captureBtn.addEventListener('click', capturePhoto);
}

if (imageUpload) {
    imageUpload.addEventListener('change', loadLocalImage);
}
