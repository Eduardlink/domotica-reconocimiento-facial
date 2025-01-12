import streamlit as st
from services.dispositivos_service import consultar_dispositivos, insertar_dispositivo
import login

# Generar el login y validar el usuario
login.generarLogin()
if 'usuario' in st.session_state:
    st.header('Gestión de :blue[Dispositivos]')

    # Mostrar los dispositivos registrados
    st.subheader("Lista de dispositivos registrados")

    # Función para actualizar la lista de dispositivos en session_state
    def actualizar_tabla_dispositivos():
        st.session_state["dispositivos"] = consultar_dispositivos()

    # Consultar dispositivos si no están en session_state
    if "dispositivos" not in st.session_state:
        actualizar_tabla_dispositivos()

    dispositivos = st.session_state["dispositivos"]

    if dispositivos:
        # Mostrar los dispositivos en una tabla
        st.table(
            [
                {
                    "ID": dispositivo[0],
                    "Nombre": dispositivo[1],
                    "Tipo": dispositivo[2],
                    "Descripción": dispositivo[3],
                    "Fecha de creación": dispositivo[7],  # Ajustado al índice correcto
                }
                for dispositivo in dispositivos
            ]
        )
    else:
        st.warning("No hay dispositivos registrados.")

    # Botón para actualizar manualmente la tabla
    if st.button("Actualizar tabla"):
        actualizar_tabla_dispositivos()

    # Formulario para agregar un nuevo dispositivo
    st.subheader("Agregar un nuevo dispositivo")
    with st.form("form_agregar_dispositivo"):
        nombre = st.text_input("Nombre del dispositivo")
        tipo = st.text_input("Tipo del dispositivo")
        descripcion = st.text_input("Descripción del dispositivo")
        icono_activado = st.text_input("Ícono activado")
        icono_desactivado = st.text_input("Ícono desactivado")
        btn_submit = st.form_submit_button("Agregar")

        if btn_submit:
            if nombre and tipo and descripcion and icono_activado and icono_desactivado:
                insertar_dispositivo(nombre, tipo, descripcion, icono_activado, icono_desactivado)
                st.success(f"Dispositivo '{nombre}' agregado correctamente.")
                # Actualizar la tabla dinámicamente después de agregar
                actualizar_tabla_dispositivos()
            else:
                st.error("Todos los campos son obligatorios.")
