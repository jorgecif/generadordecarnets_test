import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.platypus import Image as RLImage
import base64
from io import BytesIO

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Generador de Carnet",
    page_icon="🕵️‍♂️",
    layout="centered",
)

# Título de la aplicación
st.title("Generador de Carnet de Agente Secreto")

# Campos de entrada
nombre = st.text_input("Nombre:")
equipo = st.text_input("Equipo:")
identificacion = st.text_input("Identificación:")
rol = st.selectbox("Rol:", ["Rol 1", "Rol 2", "Rol 3"])
foto_perfil = st.file_uploader("Subir Foto de Perfil", type=["jpg", "png"])

# Botón para generar el carnet
if st.button("Generar Carnet"):
    # Crear un objeto PDF en memoria
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    
    # Definir colores personalizados
    color_fondo = HexColor("#222222")  # Fondo oscuro
    color_marco = HexColor("#FFFF00")   # Marco amarillo brillante
    
    # Configurar fondo y marco
    pdf.setFillColor(color_fondo)
    pdf.rect(20, 20, 580, 340, fill=True)
    pdf.setStrokeColor(color_marco)
    pdf.rect(10, 10, 600, 350, stroke=True)
    
    # Agregar el nombre de la organización
    pdf.setFont("Helvetica-Bold", 16)
    pdf.setFillColor(color_marco)
    pdf.drawString(30, 320, "Evoke - Agencia Secreta")
    
    # Agregar detalles del agente
    pdf.setFont("Helvetica", 12)
    pdf.setFillColor(color_marco)
    pdf.drawString(30, 280, "Nombre: " + nombre)
    pdf.drawString(30, 260, "Equipo: " + equipo)
    pdf.drawString(30, 240, "Identificación: " + identificacion)
    pdf.drawString(30, 220, "Rol: " + rol)
    
    # Agregar la foto de perfil si se ha subido
    if foto_perfil is not None:
        image = RLImage(foto_perfil)
        image.drawHeight = 80
        image.drawWidth = 80
        image.wrap(80, 80)
        image.drawOn(pdf, 420, 220)
    
    # Guardar el PDF en el búfer de memoria
    pdf.showPage()
    pdf.save()
    
    # Obtener los bytes del PDF
    pdf_bytes = buffer.getvalue()
    
    # Mostrar el enlace para descargar el PDF
    st.success("Carnet generado. ¡Haz clic abajo para descargar!")
    st.markdown(
        f'<a href="data:application/pdf;base64,{base64.b64encode(pdf_bytes).decode("utf-8")}" download="{nombre}_carnet.pdf">Descargar Carnet</a>',
        unsafe_allow_html=True,
    )

# Estilo CSS para el carnet
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #FFFF00;
        color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
