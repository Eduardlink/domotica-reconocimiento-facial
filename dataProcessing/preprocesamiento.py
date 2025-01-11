import cv2
import os
import numpy as np

def suavizar_imagen(image, kernel_size=5):

    if kernel_size % 2 == 0:
        raise ValueError("El tamaño del kernel debe ser impar.")

    
    if len(image.shape) == 3:
        is_rgb = True
    else:
        is_rgb = False
        image = image[..., np.newaxis]  

    # Dimensiones de la imagen
    h, w, c = image.shape
    offset = kernel_size // 2

    # Padding
    padded_image = np.pad(image, ((offset, offset), (offset, offset), (0, 0)), mode='reflect')

    
    suavizada = np.zeros((h, w, c), dtype=np.uint8)

    # Aplicar filtro de media
    for i in range(h):
        for j in range(w):
            for channel in range(c):
                ventana = padded_image[i:i+kernel_size, j:j+kernel_size, channel]
                suavizada[i, j, channel] = np.mean(ventana)

    
    return suavizada if is_rgb else suavizada[..., 0]

def acentuar_imagen(image):
    # Definir el kernel de pase alto
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    
    
    if len(image.shape) == 3:
        is_rgb = True
    else:
        is_rgb = False
        image = image[..., np.newaxis]  

    # Dimensiones de la imagen
    h, w, c = image.shape
    offset = kernel.shape[0] // 2 

    # Imagen con borde para manejar los bordes
    padded_image = np.pad(image, ((offset, offset), (offset, offset), (0, 0)), mode='reflect')

    # Crear una matriz para la imagen acentuada
    acentuada = np.zeros((h, w, c), dtype=np.uint8)

    # Aplicar convolución
    for i in range(h):
        for j in range(w):
            for channel in range(c):
                ventana = padded_image[i:i+kernel.shape[0], j:j+kernel.shape[1], channel]
                valor = np.sum(ventana * kernel)
                acentuada[i, j, channel] = np.clip(valor, 0, 255)

    
    return acentuada if is_rgb else acentuada[..., 0]

def aplicar_sobel(image):

    if len(image.shape) == 3:
        image = np.mean(image, axis=2).astype(np.uint8)  
    
    # Mascaras de Sobel
    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])
    
    sobel_y = np.array([[-1, -2, -1],
                        [ 0,  0,  0],
                        [ 1,  2,  1]])
    
    # Dimensiones de la imagen
    h, w = image.shape
    offset = sobel_x.shape[0] // 2

    # Padding
    padded_image = np.pad(image, ((offset, offset), (offset, offset)), mode='reflect')

    
    grad_x = np.zeros((h, w), dtype=np.float32)
    grad_y = np.zeros((h, w), dtype=np.float32)
    sobel_combined = np.zeros((h, w), dtype=np.float32)

    # Aplicar convolución
    for i in range(h):
        for j in range(w):
            # Extraer ventana de la imagen
            ventana = padded_image[i:i+sobel_x.shape[0], j:j+sobel_x.shape[1]]
            # Gradiente en X
            grad_x[i, j] = np.sum(ventana * sobel_x)
            # Gradiente en Y
            grad_y[i, j] = np.sum(ventana * sobel_y)

    # Calcular la magnitud combinada
    sobel_combined = np.sqrt(grad_x**2 + grad_y**2)

    # Normalizar la magnitud combinada a rango [0, 255]
    sobel_combined = (sobel_combined / sobel_combined.max()) * 255.0
    sobel_combined = sobel_combined.astype(np.uint8)

    # Convertir a BGR para mantener compatibilidad
    return np.stack([sobel_combined]*3, axis=-1)

def procesar_imagenes(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(input_dir, filename)
            image = cv2.imread(image_path)
            
            # Suavizar, acentuar y aplicar Sobel
            suavizada = suavizar_imagen(image)
            acentuada = acentuar_imagen(suavizada)
            sobel = aplicar_sobel(acentuada)
            
            # Guardar la imagen procesada
            output_path = os.path.join(output_dir, filename)
            cv2.imwrite(output_path, sobel)

def preprocesar_imagen(image, target_size=(128, 128)):
    # Suavizar, acentuar y aplicar Sobel
    image = suavizar_imagen(image)
    image = acentuar_imagen(image)
    image = aplicar_sobel(image)
    
    # Redimensionar y normalizar
    image = cv2.resize(image, target_size)
    image = image.astype("float32") / 255.0
    return image
