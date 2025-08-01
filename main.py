import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# Configuración
load_dotenv()
st.set_page_config(
    page_title="Transformador de Profesiones IA",
    page_icon="👔",
    layout="centered"
)

# Título
st.title("👔 Transformador de Profesiones")
st.markdown("Sube tu foto y escribe cualquier profesión para ver cómo te verías")

# Sidebar
with st.sidebar:
    st.header("Configuración")
    profession = st.text_input(
        "¿Qué profesión quieres probar?",
        placeholder="Ej: Chef espacial, Ingeniero de robots..."
    )
    creativity = st.slider("Nivel de creatividad", 0.0, 1.0, 0.7)

# Conexión con Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro-vision')

# Subida de imagen
uploaded_file = st.file_uploader("Sube tu foto (JPEG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file and profession:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="Tu foto original", width=300)
        
        with st.spinner(f"Creando tu versión como {profession}..."):
            prompt = f"""
            Describe en detalle cómo se vería esta persona como {profession}.
            Incluye:
            1. Vestimenta profesional
            2. Entorno de trabajo
            3. Herramientas/equipos
            4. Rasgos faciales reconocibles
            Estilo: Fotografía realista
            Creatividad: {creativity}/1.0
            """
            
            response = model.generate_content([prompt, image])
            
            st.success("¡Transformación completada!")
            with st.expander("📝 Descripción detallada", expanded=True):
                st.write(response.text)
                
            st.info("ℹ️ Próximamente: Generación de imágenes con DALL-E 3")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
elif uploaded_file and not profession:
    st.warning("⚠️ Por favor ingresa una profesión")

# Ejemplos
st.markdown("---")
st.subheader("🎨 Ejemplos")
col1, col2 = st.columns(2)
with col1:
    st.image("static/examples/example1.jpg", caption="Chef molecular", width=200)
with col2:
    st.image("static/examples/example2.jpg", caption="Ingeniera de robots", width=200)