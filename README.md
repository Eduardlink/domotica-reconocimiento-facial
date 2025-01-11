
# Proyecto de Domótica con Reconocimiento Facial

Este proyecto implementa un sistema de domótica con un inicio de sesión basado en reconocimiento facial. Utiliza **Streamlit** como interfaz principal y una base de datos en MySQL para gestionar usuarios y sus carpetas asociadas.

## Requisitos previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:
- Python 3.7 o superior
- MySQL
- Git (opcional, para clonar el repositorio si está en un repositorio remoto)

## Instalación

### 1. Clonar el repositorio (si aplica)
Si el proyecto está en un repositorio remoto, clónalo con:
```bash
git clone https://github.com/tu_usuario/tu_proyecto.git
cd tu_proyecto
```

### 2. Crear y activar un entorno virtual
Crea un entorno virtual llamado `domoticaEnv` y actívalo:

#### En Windows:
```bash
python -m venv domoticaEnv
domoticaEnv\Scripts\activate
```

#### En Linux/Mac:
```bash
python3 -m venv domoticaEnv
source domoticaEnv/bin/activate
```

### 3. Instalar las dependencias
Con el entorno virtual activado, instala las dependencias necesarias:
```bash
pip install mysql-connector-python
pip install streamlit
pip install opencv-python
pip install h5py
pip install scikit-learn
pip install tensorflow
```

### 4. Configurar la base de datos
1. Asegúrate de tener MySQL instalado y en ejecución.
2. Crea una base de datos llamada `reconocimiento_facial` en MySQL.
3. Importa el archivo `usuarios.sql` ubicado en `services/usuarios.sql` para crear la estructura de la base de datos:
   ```bash
   mysql -u tu_usuario -p reconocimiento_facial < services/usuarios.sql
   ```

   Reemplaza `tu_usuario` con tu usuario de MySQL.

### 5. Ejecutar la aplicación
Con el entorno virtual activado, ejecuta la aplicación usando **Streamlit**:
```bash
streamlit run inicio.py
```

### 6. Navegar por la aplicación
Abre tu navegador y accede a la dirección que Streamlit indica, por ejemplo:
```
http://localhost:8501
```

## Estructura del proyecto
```
├── dataProcessing/
│   ├── activations.py
│   ├── aumento_datos.py
│   ├── entrenamiento_modelo.py
│   ├── preprocesamiento.py
├── domoticaEnv/          # Entorno virtual (creado localmente)
├── model/
├── pages/
│   ├── pagina1.py
│   ├── pagina2.py
│   ├── pagina3.py
├── scripts/
│   ├── entrenamiento_modelo.py
├── services/
│   ├── base_datos.py
│   ├── usuario_service.py
│   ├── usuarios.sql       # Backup de la base de datos
├── users/
│   ├── inicio.py
│   ├── login.py
```

## Librerías utilizadas
A continuación, se describen las librerías instaladas y su propósito:
- **mysql-connector-python**: Para conectarse y trabajar con la base de datos MySQL.
- **streamlit**: Framework para crear aplicaciones web interactivas.
- **opencv-python**: Librería para procesamiento de imágenes y video (reconocimiento facial).
- **h5py**: Manejo de archivos HDF5 (útil para guardar modelos de TensorFlow).
- **scikit-learn**: Algoritmos de machine learning.
- **tensorflow**: Framework de deep learning para el reconocimiento facial.

## Notas adicionales
- Asegúrate de configurar las credenciales de la base de datos en el archivo `services/base_datos.py`:
```python
connection = mysql.connector.connect(
    host="localhost",
    user="tu_usuario",
    password="tu_contraseña",
    database="reconocimiento_facial"
)
```
- Si tienes problemas al iniciar, revisa el log de errores y verifica que la base de datos y las dependencias estén correctamente configuradas.

