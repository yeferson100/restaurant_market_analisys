import streamlit as st


def app():
    st.title('Bienvenido')

if __name__ == "__main__":
    app()

st.image("Logo.jpeg", use_column_width=220, output_format="JPEG")
# Título centrado
st.markdown("<h1 class='centered-title'>Recomendador de Inversión en el Sector de Restaurantes del Sureste de USA</h1>", unsafe_allow_html=True)
#from streamlit_option_menu import option_menu












