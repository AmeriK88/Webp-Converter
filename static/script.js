// script.js

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('input-images').addEventListener('change', function() {
        var previewSection = document.getElementById('preview-section');
        previewSection.innerHTML = '';

        var files = this.files;
        for (var i = 0; i < files.length; i++) {
            var file = files[i];
            if (!file.type.startsWith('image/')) { continue }

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
