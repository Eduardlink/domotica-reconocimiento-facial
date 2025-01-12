import streamlit as st
from services.usuario_service import consultar_usuarios
from services.dispositivos_service import consultar_dispositivos
from services.permisos_service import obtener_dispositivos_usuario, agregar_permiso
import login

# Generar el login y validar el usuario
login.generarLogin()
if 'usuario' in st.session_state:
    st.header('Gestión de :green[Permisos]')

    # Obtener lista de usuarios
    st.subheader("Lista de usuarios")
    usuarios = consultar_usuarios()

    if usuarios:
        # Mostrar lista de usuarios para seleccionar
        opciones_usuarios = {f"{usuario[1]}": usuario[0] for usuario in usuarios}
        usuario_seleccionado = st.selectbox("Selecciona un usuario", list(opciones_usuarios.keys()))

        # Obtener ID del usuario seleccionado
        id_usuario_seleccionado = opciones_usuarios[usuario_seleccionado]

        st.markdown(f"### Dispositivos asociados al usuario: **{usuario_seleccionado}**")

        # Callback interno para actualizar los dispositivos asociados
        if f"dispositivos_asociados_{id_usuario_seleccionado}" not in st.session_state:
            st.session_state[f"dispositivos_asociados_{id_usuario_seleccionado}"] = obtener_dispositivos_usuario(id_usuario_seleccionado)

        # Función para actualizar la tabla dinámicamente
        def actualizar_dispositivos_asociados():
            st.session_state[f"dispositivos_asociados_{id_usuario_seleccionado}"] = obtener_dispositivos_usuario(id_usuario_seleccionado)

        dispositivos_asociados = st.session_state[f"dispositivos_asociados_{id_usuario_seleccionado}"]

        # Renderizar la tabla de dispositivos asociados
        if dispositivos_asociados:
            st.table(
                [
                    {
                        "ID": dispositivo[0],
                        "Nombre": dispositivo[1],
                        "Tipo": dispositivo[2],
                        "Descripción": dispositivo[3],
                    }
                    for dispositivo in dispositivos_asociados
                ]
            )
        else:
            st.warning("Este usuario no tiene dispositivos asociados.")

        # Botón para actualizar la tabla
        if st.button("Actualizar tabla"):
            actualizar_dispositivos_asociados()
            #st.success("Tabla actualizada correctamente.")

        # Formulario para agregar dispositivos al usuario
        st.markdown("### Agregar dispositivo al usuario")

        # Obtener todos los dispositivos disponibles
        dispositivos = consultar_dispositivos()

        if dispositivos:
            # Crear un selectbox para seleccionar un dispositivo
            opciones_dispositivos = {f"{dispositivo[1]} ": dispositivo[0] for dispositivo in dispositivos}
            dispositivo_seleccionado = st.selectbox("Selecciona un dispositivo", list(opciones_dispositivos.keys()))

            # Botón para agregar el permiso
            if st.button("Agregar dispositivo al usuario"):
                id_dispositivo_seleccionado = opciones_dispositivos[dispositivo_seleccionado]
                agregar_permiso(id_usuario_seleccionado, id_dispositivo_seleccionado)
                st.success(f"El dispositivo '{dispositivo_seleccionado}' ha sido asociado al usuario '{usuario_seleccionado}'.")
                # Llamar al callback para actualizar la tabla automáticamente
                actualizar_dispositivos_asociados()
        else:
            st.warning("No hay dispositivos disponibles para asociar.")
    else:
        st.warning("No hay usuarios registrados.")
