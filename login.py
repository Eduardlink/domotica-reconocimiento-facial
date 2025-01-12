import streamlit as st
import cv2
from services.usuario_service import buscar_usuario_por_nombre
from tensorflow.keras.models import load_model
import numpy as np
import os
import json
from dataProcessing.preprocesamiento import preprocesar_imagen

# Validación simple de usuario y clave con la base de datos
def validarUsuario(usuario, clave):
    """
    Permite la validación de usuario y clave usando la base de datos.
    """
    usuario_data = buscar_usuario_por_nombre(usuario)
    if usuario_data and usuario_data[2] == clave:  # La contraseña se encuentra en la tercera columna
        return True
    return False

def generarMenu(usuario):
    """
    Genera el menú dependiendo del usuario.
    """
    with st.sidebar:
        st.write(f"Hola **:blue-background[{usuario}]**")
        st.page_link("inicio.py", label="Inicio", icon=":material/home:")
        st.subheader("Administrar permisos")
        st.page_link("pages/pagina1.py", label="Usuarios", icon="👥")
        st.page_link("pages/pagina2.py", label="Dispositivos", icon="🖥️")
        st.page_link("pages/pagina3.py", label="Permisos", icon="🔗")
        btnSalir = st.button("Salir")
        if btnSalir:
            st.session_state.clear()
            st.rerun()

def reconocer_usuario():
    """
    Captura una imagen con la cámara, detecta el rostro, lo procesa y lo reconoce.
    """
    st.info("Abriendo cámara para reconocimiento facial...")
    
    # Cargar modelo entrenado
    model_path = "model/cnn_model.h5"
    class_indices_path = "model/class_indices.json"
    
    if not os.path.exists(model_path) or not os.path.exists(class_indices_path):
        st.error("El modelo o el mapeo de etiquetas no están disponibles. Por favor, entrena el modelo primero.")
        return
    
    model = load_model(model_path)
    
    # Cargar mapeo de etiquetas
    with open(class_indices_path, "r") as f:
        class_indices = json.load(f)
    label_map = {v: k for k, v in class_indices.items()}  # Invertir el mapeo
    
    # Cargar el modelo de detección de rostros
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    # Inicializar la cámara
    cap = cv2.VideoCapture(0)
    st.write("Presiona 'c' para capturar el rostro o 'q' para salir.")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("No se pudo abrir la cámara.")
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        cv2.imshow("Reconocimiento Facial", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            if len(faces) > 0:
                x, y, w, h = faces[0]
                rostro = frame[y:y+h, x:x+w]
                processed_frame = preprocesar_imagen(rostro)
                processed_frame = np.expand_dims(processed_frame, axis=0)
                
                prediction = model.predict(processed_frame)
                predicted_label = label_map[np.argmax(prediction)]
                
                st.success(f"Usuario reconocido: {predicted_label}")
                st.session_state["usuario"] = predicted_label
                st.rerun()
            else:
                st.error("No se detectó ningún rostro. Intenta de nuevo.")
            break
        elif key == ord('q'):
            st.info("Cerrando cámara sin capturar rostro.")
            break
    cap.release()
    cv2.destroyAllWindows()

def generarLogin():
    """
    Genera la ventana de login o muestra el menú si el login es válido.
    """
    if 'usuario' in st.session_state:
        generarMenu(st.session_state['usuario'])
    else:
        with st.form('frmLogin'):
            parUsuario = st.text_input('Usuario')
            parPassword = st.text_input('Password', type='password')
            btnLogin = st.form_submit_button('Ingresar', type='primary')
            if btnLogin:
                if validarUsuario(parUsuario, parPassword):
                    st.session_state['usuario'] = parUsuario
                    st.rerun()
                else:
                    st.error("Usuario o clave inválidos", icon=":material/gpp_maybe:")

        st.markdown("---")
        st.write("**O bien, puedes ingresar con reconocimiento facial:**")
        if st.button("Ingresar con Reconocimiento Facial"):
            reconocer_usuario()
