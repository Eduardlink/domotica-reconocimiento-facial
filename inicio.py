import streamlit as st
import login as login
from services.dispositivos_service import consultar_dispositivos


st.header('Página :orange[principal]')
login.generarLogin()
if 'usuario' in st.session_state:
    st.subheader('Gestión de Dispositivos')

    # Inicializar estados de dispositivos en st.session_state
    if 'dispositivos_estado' not in st.session_state:
        dispositivos = consultar_dispositivos()
        st.session_state['dispositivos_estado'] = {
            dispositivo[0]: {'nombre': dispositivo[1], 'tipo': dispositivo[2], 'estado': 'desactivado'}
            for dispositivo in dispositivos
        }

    # Función para cambiar el estado de un dispositivo
    def cambiar_estado_dispositivo(id_dispositivo):
        dispositivo = st.session_state['dispositivos_estado'][id_dispositivo]
        dispositivo['estado'] = 'activado' if dispositivo['estado'] == 'desactivado' else 'desactivado'

    # Organizar dispositivos en filas y columnas estilo panel
    dispositivos = list(st.session_state['dispositivos_estado'].items())
    columnas_por_fila = 2  # Número de columnas por fila
    filas = [dispositivos[i:i + columnas_por_fila] for i in range(0, len(dispositivos), columnas_por_fila)]

    # Estilo CSS para las tarjetas
    st.markdown(
        """
        <style>
        .stHorizontalBlock .stVerticalBlock {
            border: 1px solid #ccc;
            border-radius: 10px;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
            padding: 20px;
        }
        .tarjeta h3 {
            margin: 10px 0;
        }
        .tarjeta button {
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    for fila in filas:
        cols = st.columns(columnas_por_fila)
        for idx, (id_dispositivo, info) in enumerate(fila):
            if idx >= len(fila):  # Evitar errores si la fila tiene menos columnas
                break

            with cols[idx]:
                nombre = info['nombre']
                estado = info['estado']

                # Seleccionar ícono según el estado
                icono = "✅" if estado == 'activado' else "❌"

                # Mostrar tarjeta del dispositivo con estilo CSS
                st.markdown(
                    f"""
                    <div class="tarjeta">
                        <h3>{icono} {nombre}</h3>
                        <p><strong>Estado:</strong> {'Activado' if estado == 'activado' else 'Desactivado'}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Botón de Activar/Desactivar
                if st.button(
                    f"Desactivar" if estado == 'activado' else "Activar",
                    key=f"btn_{id_dispositivo}",
                    on_click=cambiar_estado_dispositivo,
                    args=(id_dispositivo,)
                ):
                    st.success(f"{nombre} ha sido {'activado' if estado == 'desactivado' else 'desactivado'}.")
