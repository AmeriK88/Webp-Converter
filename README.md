# Proyecto de Conversión de Imágenes a formato WEBP con Flask

Este proyecto es una aplicación web desarrollada con Flask que permite a los usuarios cargar imágenes en varios formatos comunes (PNG, JPG, JPEG, GIF, BMP) y convertirlas al formato WEBP.

## Funcionalidades

- Permite la carga de una o varias imágenes simultáneamente.
- Verifica la extensión de archivo para asegurar que solo se carguen tipos de archivos válidos.
- Convierte las imágenes cargadas al formato WEBP.
- Proporciona enlaces para descargar las imágenes convertidas.
- Muestra mensajes de error y éxito al usuario utilizando flash.

## Configuración y Uso

1. Clona o descarga este repositorio.
2. Instala las dependencias necesarias especificadas en `requirements.txt` utilizando pip: `pip install -r requirements.txt`.
3. Ejecuta la aplicación con el comando: `python app.py`.
4. Abre tu navegador y ve a `http://localhost:5000` para acceder a la aplicación.

## Estructura de Archivos

- `app.py`: Contiene el código de la aplicación Flask.
- `templates/`: Carpeta que contiene los archivos HTML para las vistas.
- `uploads/`: Carpeta donde se almacenarán las imágenes cargadas y convertidas.
- `static/`: Carpeta opcional que contiene archivos estáticos como CSS o JavaScript.

## Tecnologías Utilizadas

- Python
- Flask
- Werkzeug
- PIL (Python Imaging Library)

## Autor

José Félix Gordo

## Licencia

Este proyecto está bajo la [Licencia MIT]([LICENSE](https://opensource.org/license/mit)).

