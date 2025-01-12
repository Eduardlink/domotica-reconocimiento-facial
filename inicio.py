import streamlit as st
import login as login
from services.dispositivos_service import consultar_dispositivos, actualizar_estado_dispositivo
from services.permisos_service import verificar_permiso
from tensorflow.keras.models import load_model
import cv2
import numpy as np
import os
import json
from dataProcessing.preprocesamiento import preprocesar_imagen

st.markdown('''
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet" />
''', unsafe_allow_html=True)

st.header('Página :orange[principal]')
login.generarLogin()

if 'usuario' in st.session_state:

    st.markdown('''
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet" />
    ''', unsafe_allow_html=True)
    st.subheader('Gestión de Dispositivos')

    # Cargar el modelo de reconocimiento facial y el mapeo de etiquetas
    model_path = "model/cnn_model.h5"
    class_indices_path = "model/class_indices.json"

    if not os.path.exists(model_path) or not os.path.exists(class_indices_path):
        st.error("El modelo de reconocimiento facial no está disponible. Por favor, entrena el modelo primero.")
    else:
        model = load_model(model_path)
        with open(class_indices_path, "r") as f:
            class_indices = json.load(f)
        label_map = {v: k for k, v in class_indices.items()}  # Invertir el mapeo

    # Consultar dispositivos y cargar estado inicial en session_state
    if "dispositivos_estado" not in st.session_state:
        dispositivos = consultar_dispositivos()
        st.session_state['dispositivos_estado'] = {
            dispositivo[0]: {
                'nombre': dispositivo[1],
                'tipo': dispositivo[2],
                'estado': 'activado' if dispositivo[4] == 1 else 'desactivado',
                'icono_activado': dispositivo[5],
                'icono_desactivado': dispositivo[6],
            }
            for dispositivo in dispositivos
        }

    def parse_material_icon(icono_bd: str) -> str:
        """
        Convierte ':material/tv:' en la palabra 'tv' 
        (o el texto correcto que Material Icons usa dentro de <i>).
        """
        # Aquí asumo que el icono siempre viene con la forma :material/tv:
        # y que lo único que necesitas es quedarte con 'tv'
        icono_limpio = icono_bd.replace(':material/', '').replace(':', '')
        return icono_limpio


    # Función para reconocimiento facial
    def reconocer_usuario():
        st.info("Abriendo cámara para reconocimiento facial...")

        # Cargar modelo de detección de rostros
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        # Inicializar la cámara
        cap = cv2.VideoCapture(0)

        usuario_reconocido = None
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    st.error("No se pudo abrir la cámara.")
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

                # Dibujar rectángulos en cada rostro detectado
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                # Mostrar video en OpenCV
                cv2.imshow('Camara - presiona C para capturar y Q para salir', frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('c') and len(faces) > 0:
                    (x, y, w, h) = faces[0]
                    rostro = frame[y:y+h, x:x+w]

                    # Preprocesar el rostro
                    processed_frame = preprocesar_imagen(rostro)
                    processed_frame = np.expand_dims(processed_frame, axis=0)

                    # Realizar la predicción
                    prediction = model.predict(processed_frame)
                    label_idx = np.argmax(prediction)
                    usuario_reconocido = label_map[label_idx]
                    break
                elif key == ord('q'):  # Salir al presionar 'q'
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()

        if usuario_reconocido:
            st.success(f"Usuario reconocido: {usuario_reconocido}")
            return usuario_reconocido
        else:
            st.error("No se pudo reconocer ningún rostro.")
            return None

    # Función para cambiar el estado de un dispositivo con verificación de permisos
    def cambiar_estado_dispositivo(id_dispositivo):
        usuario_reconocido = reconocer_usuario()
        if usuario_reconocido:
            tiene_permiso = verificar_permiso(usuario_reconocido, id_dispositivo)
            if tiene_permiso:
                dispositivo = st.session_state['dispositivos_estado'][id_dispositivo]
                nuevo_estado = 0 if dispositivo['estado'] == 'activado' else 1
                actualizar_estado_dispositivo(id_dispositivo, nuevo_estado)
                dispositivo['estado'] = 'activado' if nuevo_estado == 1 else 'desactivado'
                st.success(f"Dispositivo '{dispositivo['nombre']}' {'activado' if nuevo_estado == 1 else 'desactivado'} correctamente.")
            else:
                st.error(f"Acceso denegado. El usuario '{usuario_reconocido}' no tiene permisos para este dispositivo.")
        else:
            st.error("No se pudo reconocer al usuario.")

    # Organizar dispositivos en filas y columnas estilo panel
    dispositivos = list(st.session_state['dispositivos_estado'].items())
    columnas_por_fila = 2  # Número de columnas por fila
    filas = [dispositivos[i:i + columnas_por_fila] for i in range(0, len(dispositivos), columnas_por_fila)]

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
        </style>
        """,
        unsafe_allow_html=True
    )

    # Mostrar las tarjetas con íconos dinámicos
    for fila in filas:
        cols = st.columns(columnas_por_fila)
        for idx, (id_dispositivo, info) in enumerate(fila):
            if idx >= len(fila):  # Evitar errores si la fila tiene menos columnas
                break

            with cols[idx]:
                # Seleccionar el ícono según el estado
                icono = parse_material_icon(info['icono_activado'] if info['estado'] == 'activado' else info['icono_desactivado'])

                # Determinar color según el estado
                color = "green" if info['estado'] == 'activado' else "red"

                # Generar HTML para el ícono
                icono_html = f'<i style="font-size:50px; color:{color};" class="material-symbols-outlined">{icono}</i>'

                # Mostrar tarjeta con ícono y estado
                st.markdown(
                    f"""
                    <div style="display: flex; flex-direction: column; align-items: center;">
                        <h3 style="max-width: 50px;">{icono_html}</h3>
                        <p><strong>{info['nombre']}</strong></p>
                        <p><strong>Estado:</strong> {info['estado'].capitalize()}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Botón de Activar/Desactivar con clave única
                if st.button(
                    f"Desactivar" if info['estado'] == 'activado' else "Activar",
                    key=f"btn_{id_dispositivo}",
                    on_click=cambiar_estado_dispositivo,
                    args=(id_dispositivo,)
                ):
                    pass
