// Script para visualizar la imágene seleccionada en la interfaz

//Espera a que el DOM esté totalmente cargado
document.addEventListener('DOMContentLoaded', function() {
    //Espera a que el evento addListener se active cuando hay un cambio - antes se borra el contenido existente en caso de haber y añade archivo para previsualizarlo
    document.getElementById('input-images').addEventListener('change', function() {
        var previewSection = document.getElementById('preview-section');
        previewSection.innerHTML = '';

        //Obtiene los archivos seleccionados por el usuario e itera sobre ellos
        var files = this.files;
        for (var i = 0; i < files.length; i++) {
            var file = files[i];
            //Comprueba que los archivos son imágenes
            if (!file.type.startsWith('image/')) { continue }

            //Crea un campo de imágene para añadirla y previsualizarla en la interfaz
            var img = document.createElement('img');
            img.classList.add('preview-image');
            img.file = file;
    
            previewSection.appendChild(img);

            var reader = new FileReader();
            reader.onload = (function(aImg) {
                return function(e) {
                    aImg.src = e.target.result;
                };
            })(img);

            reader.readAsDataURL(file);
        }
    });
});
