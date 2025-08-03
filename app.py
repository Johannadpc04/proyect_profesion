import streamlit as st
import os
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar la API Key desde el archivo .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Inicializar el modelo generativo de IA (Gemini 2.0 Flash)
# Nota: "gemini-pro-vision" ha sido reemplazado por "gemini-2.0-flash"
model = genai.GenerativeModel('gemini-2.0-flash-preview-image-generation')

# --- Interfaz de usuario con Streamlit ---
st.set_page_config(page_title="Gemini - Viste a una persona")

st.header("Viste a una persona con Gemini 📸")
st.markdown("Sube una imagen y describe la profesión o vestimenta deseada para generar una nueva imagen.")

# Subir la imagen
uploaded_file = st.file_uploader("Elige una imagen...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    st.image(uploaded_file, caption='Imagen subida.', use_column_width=True)
    # Convertir el archivo subido en un objeto de imagen de Pillow
    image = Image.open(uploaded_file)

    # Escribir el prompt
    prompt = st.text_input("Describe la profesión o vestimenta deseada (ej: 'un astronauta con un traje espacial')", "un astronauta con un traje espacial")

    # Botón para generar la imagen
    if st.button("Generar nueva imagen"):
        if prompt and image:
            with st.spinner("Generando tu nueva imagen..."):
                try:
                    # Enviar la imagen y el prompt al modelo
                    # El prompt se envía como una lista que contiene el texto y la imagen
                    response = model.generate_content([prompt, image])

                    # Mostrar la respuesta del modelo (texto que describe la nueva imagen)
                    st.success("¡Imagen generada exitosamente!")
                    st.write("Descripción de la nueva imagen:")
                    st.write(response.text)

                    # Nota: La API de Gemini 2.0 Flash también devuelve texto, no una imagen.
                    # El modelo te devolverá una descripción detallada de cómo se vería la nueva imagen.
                except Exception as e:
                    st.error(f"Ocurrió un error: {e}")
                    st.error("Asegúrate de que la API Key es correcta y que la descripción no es demasiado compleja para el modelo.")
        else:
            st.warning("Por favor, sube una imagen y escribe un prompt.")