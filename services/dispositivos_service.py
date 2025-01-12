from services.base_datos import create_connection, execute_query, close_connection

def insertar_dispositivo(nombre, tipo, descripcion):
    """
    Inserta un nuevo dispositivo en la base de datos.

    Args:
        nombre (str): Nombre del dispositivo.
        tipo (str): Tipo del dispositivo.
        descripcion (str): Descripción del dispositivo.
    """
    connection = create_connection()
    if connection:
        try:
            query = """
            INSERT INTO dispositivos (nombre, tipo, descripcion, fecha_creacion)
            VALUES (%s, %s, %s, NOW());
            """
            params = (nombre, tipo, descripcion)
            execute_query(connection, query, params)
        finally:
            close_connection(connection)

def consultar_dispositivos():
    """
    Consulta todos los dispositivos registrados en la base de datos.

    Returns:
        list: Lista de dispositivos.
    """
    connection = create_connection()
    dispositivos = []
    if connection:
        try:
            query = "SELECT * FROM dispositivos;"
            cursor = connection.cursor()
            cursor.execute(query)
            dispositivos = cursor.fetchall()  # Consume todos los resultados
            cursor.close()
        finally:
            close_connection(connection)
    return dispositivos

def buscar_dispositivo_por_id(id_dispositivo):
    """
    Busca un dispositivo por su ID y devuelve los detalles.

    Args:
        id_dispositivo (int): ID del dispositivo a buscar.

    Returns:
        tuple: Información del dispositivo si se encuentra, de lo contrario None.
    """
    connection = create_connection()
    dispositivo = None
    if connection:
        try:
            query = "SELECT * FROM dispositivos WHERE id = %s;"
            params = (id_dispositivo,)
            cursor = connection.cursor()
            cursor.execute(query, params)
            dispositivo = cursor.fetchone()
            cursor.close()
        finally:
            close_connection(connection)
    return dispositivo

def actualizar_dispositivo(id_dispositivo, nombre, tipo, descripcion):
    """
    Actualiza los detalles de un dispositivo en la base de datos.

    Args:
        id_dispositivo (int): ID del dispositivo a actualizar.
        nombre (str): Nuevo nombre del dispositivo.
        tipo (str): Nuevo tipo del dispositivo.
        descripcion (str): Nueva descripción del dispositivo.
    """
    connection = create_connection()
    if connection:
        try:
            query = """
            UPDATE dispositivos
            SET nombre = %s, tipo = %s, descripcion = %s
            WHERE id = %s;
            """
            params = (nombre, tipo, descripcion, id_dispositivo)
            execute_query(connection, query, params)
        finally:
            close_connection(connection)

def eliminar_dispositivo(id_dispositivo):
    """
    Elimina un dispositivo de la base de datos.

    Args:
        id_dispositivo (int): ID del dispositivo a eliminar.
    """
    connection = create_connection()
    if connection:
        try:
            query = "DELETE FROM dispositivos WHERE id = %s;"
            params = (id_dispositivo,)
            execute_query(connection, query, params)
        finally:
            close_connection(connection)
