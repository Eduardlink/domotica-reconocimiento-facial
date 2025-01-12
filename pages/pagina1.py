import streamlit as st
import os
from services.usuario_service import consultar_usuarios, insertar_usuario
from dataProcessing.aumento_datos import data_augmentation
from dataProcessing.preprocesamiento import procesar_imagenes
from scripts.entrenamiento_modelo import entrenar_modelo
import login

def capturar_imagenes(usuario, num_fotos=3):
    """
    Abre la cámara, captura varias imágenes, detecta los rostros y los guarda.

    Args:
        usuario (str): Nombre del usuario.
        num_fotos (int): Número de fotos a capturar.

    Returns:
        list: Lista de rutas a las imágenes capturadas.
    """
    carpeta_usuario = f"users/{usuario}"
    os.makedirs(carpeta_usuario, exist_ok=True)  # Crear la carpeta si no existe
    rutas_imagenes = []  # Lista para guardar las rutas de las imágenes

    import cv2
    # Cargar el modelo de detección de rostros
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    cap = cv2.VideoCapture(0)
    st.write(f"Presiona 'c' para capturar el rostro ({num_fotos} veces) o 'q' para salir.")

    fotos_capturadas = 0
    while cap.isOpened() and fotos_capturadas < num_fotos:
        ret, frame = cap.read()
        if not ret:
            st.error("No se pudo abrir la cámara.")
            break

        # Convertir a escala de grises para la detección
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

        # Dibujar rectángulos alrededor de los rostros detectados
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow("Captura de Rostro", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):  # Capturar imagen
            if len(faces) > 0:
                # Extraer el rostro (solo el primero detectado)
                x, y, w, h = faces[0]
                rostro = frame[y:y+h, x:x+w]
                ruta_imagen = os.path.join(carpeta_usuario, f"rostro_{fotos_capturadas + 1}.jpg")
                cv2.imwrite(ruta_imagen, rostro)  # Guardar el rostro recortado
                rutas_imagenes.append(ruta_imagen)
                st.success(f"Rostro capturado y guardado en {ruta_imagen}")
                fotos_capturadas += 1
            else:
                st.error("No se detectó ningún rostro. Intenta de nuevo.")
        elif key == ord('q'):  # Salir sin capturar
            st.info("Cerrando cámara sin capturar todas las imágenes.")
            break

    cap.release()
    cv2.destroyAllWindows()

    return rutas_imagenes if len(rutas_imagenes) == num_fotos else None


# Generar el login y validar el usuario
login.generarLogin()
if 'usuario' in st.session_state:
    st.header('Gestión de :blue[Usuarios]')

    # Función para actualizar la lista de usuarios
    def actualizar_tabla_usuarios():
        st.session_state["usuarios"] = consultar_usuarios()

    # Mostrar los usuarios registrados
    st.subheader("Lista de usuarios registrados")

    if "usuarios" not in st.session_state:
        actualizar_tabla_usuarios()

    usuarios = st.session_state["usuarios"]

    if usuarios:
        # Mostrar los usuarios en una tabla
        st.table(
            [
                {
                    "ID": usuario[0],
                    "Usuario": usuario[1],
                    "Admin": "Sí" if usuario[4] else "No",  # Columna admin
                    "Fecha de creación": usuario[5],
                }
                for usuario in usuarios
            ]
        )
    else:
        st.warning("No hay usuarios registrados.")

    # Botón para actualizar manualmente la tabla
    if st.button("Actualizar tabla"):
        actualizar_tabla_usuarios()
        #st.success("Tabla de usuarios actualizada correctamente.")

    # Formulario para agregar un nuevo usuario
    st.subheader("Agregar un nuevo usuario")
    if "rutas_imagenes" not in st.session_state:
        st.session_state["rutas_imagenes"] = None

    with st.form("form_agregar_usuario"):
        usuario = st.text_input("Nombre de usuario")
        contraseña = st.text_input("Contraseña", type="password")
        confirmar_contraseña = st.text_input("Confirmar contraseña", type="password")
        admin = st.checkbox("¿Es administrador?")
        capturar_btn = st.form_submit_button("Capturar imágenes para reconocimiento facial")
        btn_submit = st.form_submit_button("Agregar usuario")

        # Capturar imágenes para el reconocimiento facial
        if capturar_btn:
            if usuario:
                st.session_state["rutas_imagenes"] = capturar_imagenes(usuario, num_fotos=3)
            else:
                st.error("Por favor, ingresa un nombre de usuario antes de capturar las imágenes.")

        # Agregar usuario
        if btn_submit:
            if contraseña != confirmar_contraseña:
                st.error("Las contraseñas no coinciden.")
            elif not usuario or not contraseña:
                st.error("Todos los campos son obligatorios.")
            elif not st.session_state["rutas_imagenes"]:
                st.error("Debes capturar las imágenes antes de registrarte.")
            else:
                try:
                    # Ruta de la carpeta del usuario
                    user_dir = f"users/{usuario}"

                    # Aplicar Data Augmentation para cada imagen capturada
                    for ruta_imagen in st.session_state["rutas_imagenes"]:
                        data_augmentation(ruta_imagen, user_dir)

                    # Procesar imágenes aumentadas
                    procesar_imagenes(user_dir, user_dir)

                    # Entrenar modelo CNN con todas las imágenes y obtener precisión
                    precision = entrenar_modelo("users", "model/cnn_model.h5")

                    # Guardar información del usuario en la base de datos
                    insertar_usuario(usuario, contraseña, user_dir, admin)

                    st.success(f"Usuario '{usuario}' registrado con éxito. Modelo entrenado con una precisión de {precision:.2f}% en validación.")
                    st.session_state["rutas_imagenes"] = None  # Reiniciar las imágenes
                    # Actualizar la tabla dinámicamente
                    actualizar_tabla_usuarios()
                except Exception as e:
                    st.error(f"Error: {e}")
