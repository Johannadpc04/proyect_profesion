import google.generativeai as genai
import streamlit as st
from PIL import Image
import io
import os
from dotenv import load_dotenv

# Cargar la clave API desde .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Modelo correcto para generar imágenes (asegúrate de que esté disponible)
model = genai.GenerativeModel('models/gemini-2.0-flash-preview-image-generation')

def generate_image(prompt, image):
    try:
        # Generar contenido con respuesta tipo imagen
        response = model.generate_content(
            [prompt, image],
            generation_config={"response_mime_type": "image/png"}
        )

        # Verificar que haya una imagen en la respuesta
        if response._result and hasattr(response._result, "candidates"):
            image_data = response._result.candidates[0].content.parts[0].data
            return Image.open(io.BytesIO(image_data))
        else:
            return None
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None

# Interfaz en Streamlit
st.title("🧑‍🎨 Transformador de Profesión")
profession = st.text_input("Escribe la profesión (ej. bombero, chef, doctor)")
uploaded_file = st.file_uploader("Sube una foto tuya (jpg, png)", type=["jpg", "jpeg", "png"])

if uploaded_file and profession:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen original", use_container_width=True)

    prompt = f"""
    Transforma esta persona en un {profession}. Asegúrate de:
    - Mantener el rostro
    - Agregar uniforme y herramientas profesionales
    - Ambientar la imagen en el entorno típico del {profession}
    """

    with st.spinner("Generando imagen..."):
        result_img = generate_image(prompt, image)

        if result_img:
            st.image(result_img, caption=f"Imagen como {profession}", use_container_width=True)
            # Botón para descargar
            img_byte_arr = io.BytesIO()
            result_img.save(img_byte_arr, format='PNG')
            st.download_button("Descargar imagen", img_byte_arr.getvalue(), f"{profession}.png", "image/png")
        else:
            st.warning("❗ No se pudo generar la imagen. Verifica el modelo o tu clave API.")
