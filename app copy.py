import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.platypus import Image as RLImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import base64
from io import BytesIO
from streamlit_extras.let_it_rain import rain









# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Generador IDs Agentes Evoke",
    page_icon="🕵️‍♂️",
    layout="centered",
)
# Oculto botones de Streamlit
hide_streamlit_style = """
				<style>
				#MainMenu {visibility: hidden;}

				footer {visibility: hidden;}
				</style>
				"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Funciones
def success():
	rain(
		emoji="🎈",
		font_size=54,
		falling_speed=5,
		animation_length=1, #'infinite'
	)


# Contraseña correcta
contrasena_correcta = "12345"


# Fuentes ReportLab
pdfmetrics.registerFont(TTFont('Orbitron-Bold', 'Orbitron-Bold.ttf'))


# Título de la aplicación
st.title("🎓 Generador IDs Agentes Evoke")

# Ruta de imágenes
ruta_fondo_anverso = "fondo_anverso.png"
ruta_fondo_reverso = "fondo_anverso.png"
ruta_inicio = "carnet.jpeg"



# Tamaño del carnet
ancho_carnet = 290
alto_carnet = 180

# Posición del carnet en la página
x_carnet = (letter[0] - ancho_carnet) / 2
y_carnet = (letter[1] - alto_carnet) / 2

# Definir colores personalizados
color_fondo = HexColor("#222222")  # Fondo oscuro
color_marco = HexColor("#FFFFFF")   # Marco amarillo brillante
color_letra_grande = HexColor("#FFFFFF")   # Blanco
color_letra_pequena = HexColor("#FFFFFF")   # Blanco
color_marco_foto = HexColor("#8ae0db")   # Gris claro






# Inicia la interfaz
st.sidebar.image(ruta_inicio, use_column_width=True)
contrasena_aceptada="No"


# Campo de contraseña
contrasena_ingresada = st.sidebar.text_input("Introduce la Contraseña", type="password")



# Botón para enviar
if st.sidebar.button("Enviar"):
    if contrasena_ingresada == contrasena_correcta:
        st.success("Contraseña Correcta. Acceso Permitido.")

        contrasena_aceptada="Si"
    
    
    
    else:
        st.error("Contraseña Incorrecta. Acceso Denegado.")

        contrasena_aceptada="No"






if contrasena_aceptada == "Si":

    # Campos de entrada
    nombre = st.text_input("Nombre:")
    equipo = st.text_input("Equipo:")
    organizacion = st.selectbox("Organizacion", ["Org 1", "Org 2", "Org 3"])

    identificacion = st.text_input("Identificación:")
    rol = st.selectbox("Seleccione", ["Colaborador profundo", "Visionario creativo", "Solucionador de problemas"])
    foto_perfil = st.file_uploader("Subir Foto de Perfil", type=["jpg", "png"])

    # Botón para generar el carnet
    if st.button("Generar Carnet"):
        # Crear un objeto PDF en memoria
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter) 

        
        # Configurar fondo y marco
        pdf.setFillColor(color_fondo)
        pdf.rect(x_carnet, y_carnet, ancho_carnet, alto_carnet, fill=True)

        # Agregar la imagen de fondo al carnet

        pdf.drawImage(ruta_fondo_anverso, x_carnet, y_carnet, width=ancho_carnet, height=alto_carnet, preserveAspectRatio=True)
        pdf.drawImage(ruta_fondo_reverso, x_carnet, y_carnet-alto_carnet+10, width=ancho_carnet, height=alto_carnet, preserveAspectRatio=True)


        pdf.setStrokeColor(color_marco_foto)
        pdf.rect(x_carnet, y_carnet, ancho_carnet, alto_carnet, stroke=True)
        
        # Agregar el nombre de la organización
        pdf.setFont("Orbitron-Bold", 30)
        pdf.setFillColor(color_letra_grande)
        pdf.drawString(x_carnet+ancho_carnet/2-56, y_carnet+alto_carnet/2+30, "AGENTE")
        
        # Agregar detalles del agente
        pdf.setFont("Orbitron-Bold", 14)
        pdf.setFillColor(color_letra_grande)
        pdf.drawString(x_carnet+ancho_carnet/2-56, y_carnet+alto_carnet/2+10, nombre)
        pdf.setFont("Orbitron-Bold", 9)
        pdf.drawString(x_carnet+ancho_carnet/2-56, y_carnet+alto_carnet/2-8, rol)

        # Datos en reverso
        pdf.setFont("Orbitron-Bold", 11)
        pdf.setFillColor(color_letra_grande)
        pdf.drawString(x_carnet+ancho_carnet/2-86, y_carnet-alto_carnet+10+alto_carnet/2+10, "Equipo: " + equipo)
        pdf.drawString(x_carnet+ancho_carnet/2-86, y_carnet-alto_carnet+10+alto_carnet/2+25, "Organización: " + organizacion)
        pdf.drawString(x_carnet+ancho_carnet/2-86, y_carnet-alto_carnet+10+alto_carnet/2+40, "Identificación: " + identificacion)



        # Agregar la foto de perfil si se ha subido
        if foto_perfil is not None:
            image = RLImage(foto_perfil)
            image.drawHeight = 50
            image.drawWidth = 50
            image.wrap(50, 50)

            #image.drawOn(pdf, 190, 680)
            #image.drawOn(pdf, 10, 10)
            image.drawOn(pdf, x_carnet+ancho_carnet/2-110, y_carnet+alto_carnet/2+5)
            pdf.setFillColor(color_marco)
            pdf.rect(x_carnet+ancho_carnet/2-110, y_carnet+alto_carnet/2+5, 50, 50, stroke=True)



        # Guardar el PDF en el búfer de memoria
        pdf.showPage()
        pdf.save()
        
        # Obtener los bytes del PDF
        pdf_bytes = buffer.getvalue()
        
        # Mostrar el enlace para descargar el PDF
        st.success("Carnet generado. ¡Haz clic abajo para descargar!")
        success()
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
