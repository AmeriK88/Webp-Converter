from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import os

app = Flask(__name__)

# Carpeta de carga de archivos - devuelve el directorio de trabajo actual - crea uno en caso de no existir
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Extensiones de archivo permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Clave secreta para sesiones - cookies
app.secret_key = "your_secret_key"

# Función para verificar si la extensión de archivo es válida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para descargar imágenes
@app.route('/download/<filename>')
def download_image(filename):
    return send_from_directory('uploads', filename)

# Ruta para mostrar archivos cargados
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

# Ruta para la conversión de imágenes
@app.route('/convert', methods=['POST'])
def convert():
    input_images = request.files.getlist('input_images')
    output_prefix = request.form['output_prefix']

    if 'input_images' not in request.files:
        flash('No files selected', 'error')
        return redirect(request.url)
    
    converted_images = []

    for idx, input_image in enumerate(input_images):
        if input_image.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if not allowed_file(input_image.filename):  # Aquí se verifica la extensión del archivo
            flash('Invalid file type', 'error')
            return redirect(request.url)

        filename = secure_filename(input_image.filename)
        output_image_path = os.path.join(UPLOAD_FOLDER, f'{output_prefix}_{idx}.webp')

        try:
            image = Image.open(input_image)
            image.save(output_image_path, 'WEBP')
            converted_images.append(output_image_path)
        except Exception as e:
            flash(f'Error converting image: {e}', 'error')
            return redirect(request.url)

    flash(f'{len(input_images)} imágenes convertidas con éxito', 'success')

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
