import streamlit as st
from Pages import Bienvenido, Portal_de_Consultas, Datos_por_Estados

st.set_page_config(
        page_title="Home",
)
class MultiApp:
    def __init__(self):
        self.apps = []
    def add_app(self, title,function):
        self.apps.append({
            "title": title,
            "function": function
        }) 
    def run(self):
        app_titles = [app["title"] for app in self.apps]
        pagina_actual = st.sidebar.selectbox("Seleccione una página", app_titles)
        app = next(app for app in self.apps if app["title"] == pagina_actual)
        app["function"]()

# Crear una instancia de Multiapp
app = MultiApp()

# Agregar las aplicaciones que deseas
app.add_app("Bienvenido", Bienvenido)
app.add_app("Portal de Consultas", Portal_de_Consultas)
app.add_app("Datos por Estados", Datos_por_Estados)

app.run()