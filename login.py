import streamlit as st
from services.usuario_service import buscar_usuario_por_nombre

# Validación simple de usuario y clave con la base de datos
def validarUsuario(usuario, clave):    
    """Permite la validación de usuario y clave usando la base de datos.

    Args:
        usuario (str): usuario a validar.
        clave (str): clave del usuario.

    Returns:
        bool: True si el usuario es válido, False si no lo es.
    """    
    usuario_data = buscar_usuario_por_nombre(usuario)
    if usuario_data and usuario_data[2] == clave:  # La contraseña se encuentra en la tercera columna
        return True
    else:
        return False

def generarMenu(usuario):
    """Genera el menú dependiendo del usuario.

    Args:
        usuario (str): usuario utilizado para generar el menú.
    """        
    with st.sidebar:
        st.write(f"Hola **:blue-background[{usuario}]** ")
        # Mostramos los enlaces de páginas
        st.page_link("inicio.py", label="Inicio", icon=":material/home:")
        st.subheader("Tableros")
        st.page_link("pages/pagina1.py", label="Ventas", icon=":material/sell:")
        st.page_link("pages/pagina2.py", label="Compras", icon=":material/shopping_cart:")
        st.page_link("pages/pagina3.py", label="Personal", icon=":material/group:")    
        # Botón para cerrar la sesión
        btnSalir = st.button("Salir")
        if btnSalir:
            st.session_state.clear()
            # Luego de borrar el Session State reiniciamos la app para mostrar la opción de usuario y clave
            st.rerun()

def generarLogin():
    """Genera la ventana de login o muestra el menú si el login es válido.
    """    
    # Validamos si el usuario ya fue ingresado    
    if 'usuario' in st.session_state:
        generarMenu(st.session_state['usuario'])  # Si ya hay usuario cargamos el menú        
    else: 
        # Cargamos el formulario de login       
        with st.form('frmLogin'):
            parUsuario = st.text_input('Usuario')
            parPassword = st.text_input('Password', type='password')
            btnLogin = st.form_submit_button('Ingresar', type='primary')
            if btnLogin:
                if validarUsuario(parUsuario, parPassword):
                    st.session_state['usuario'] = parUsuario
                    # Si el usuario es correcto reiniciamos la app para que se cargue el menú
                    st.rerun()
                else:
                    # Si el usuario es inválido, mostramos el mensaje de error
                    st.error("Usuario o clave inválidos", icon=":material/gpp_maybe:")
