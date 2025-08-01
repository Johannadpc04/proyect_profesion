import os
import requests
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# *** AQUÍ PEGARÁS LA URL DE NGROK QUE TE DIO GOOGLE COLAB ***
# Asegúrate de actualizar esta URL cada vez que reinicies el cuaderno de Colab.
COLAB_API_URL = " https://69d7fdddde03.ngrok-free.app/generate_image"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    generated_image_url = None
    original_image_url = None
    error_message = None

    if request.method == 'POST':
        if 'file' not in request.files:
            error_message = "No se ha seleccionado ningún archivo."
            return render_template('index.html', error_message=error_message)

        file = request.files['file']
        profession = request.form.get('profession', 'astronauta').strip()

        if not profession:
            error_message = "Por favor, ingresa una profesión."
            return render_template('index.html', error_message=error_message)
            
        if file.filename == '':
            error_message = "No se ha seleccionado ningún archivo."
            return render_template('index.html', error_message=error_message)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            original_image_url = url_for('uploaded_file', filename=filename)

            try:
                # Envía la imagen y el prompt al servidor de Colab
                with open(filepath, 'rb') as f:
                    files = {'file': (file.filename, f.read(), file.content_type)}
                    data = {'profession': profession}
                    
                    response = requests.post(COLAB_API_URL, files=files, data=data)
                    response.raise_for_status() # Lanza un error si la respuesta no es 200

                    # Guarda la imagen binaria que recibimos del servidor de Colab
                    img_filename = f"generated_{profession}_{os.urandom(8).hex()}.png"
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
                    with open(image_path, 'wb') as img_file:
                        img_file.write(response.content)
                    
                    generated_image_url = url_for('uploaded_file', filename=img_filename)

            except requests.exceptions.RequestException as e:
                print(f"Error al conectar con el servidor de Colab: {e}")
                error_message = f"Error al conectar con el servidor de Colab: {e}"
            except Exception as e:
                print(f"Error al procesar la imagen: {e}")
                error_message = f"Ocurrió un error al procesar la imagen: {e}"

    return render_template('index.html', generated_image_url=generated_image_url, original_image_url=original_image_url, error_message=error_message)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)