from services.base_datos import create_connection, execute_query, close_connection

def insertar_dispositivo(nombre, tipo, descripcion, icono_activado, icono_desactivado):
    """
    Inserta un nuevo dispositivo en la base de datos.

    Args:
        nombre (str): Nombre del dispositivo.
        tipo (str): Tipo del dispositivo.
        descripcion (str): Descripción del dispositivo.
        icono_activado (str): Ícono para estado activado.
        icono_desactivado (str): Ícono para estado desactivado.
    """
    connection = create_connection()
    if connection:
        try:
            query = """
            INSERT INTO dispositivos (nombre, tipo, descripcion, estado, icono_activado, icono_desactivado, fecha_creacion)
            VALUES (%s, %s, %s, 0, %s, %s, NOW());
            """
            params = (nombre, tipo, descripcion, icono_activado, icono_desactivado)
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

def actualizar_dispositivo(id_dispositivo, nombre, tipo, descripcion, icono_activado, icono_desactivado):
    """
    Actualiza los detalles de un dispositivo en la base de datos.

    Args:
        id_dispositivo (int): ID del dispositivo a actualizar.
        nombre (str): Nuevo nombre del dispositivo.
        tipo (str): Nuevo tipo del dispositivo.
        descripcion (str): Nueva descripción del dispositivo.
        icono_activado (str): Nuevo ícono para estado activado.
        icono_desactivado (str): Nuevo ícono para estado desactivado.
    """
    connection = create_connection()
    if connection:
        try:
            query = """
            UPDATE dispositivos
            SET nombre = %s, tipo = %s, descripcion = %s, icono_activado = %s, icono_desactivado = %s
            WHERE id = %s;
            """
            params = (nombre, tipo, descripcion, icono_activado, icono_desactivado, id_dispositivo)
            execute_query(connection, query, params)
        finally:
            close_connection(connection)

def actualizar_estado_dispositivo(id_dispositivo, estado):
    """
    Actualiza solo el estado de un dispositivo en la base de datos.

    Args:
        id_dispositivo (int): ID del dispositivo a actualizar.
        estado (int): Nuevo estado del dispositivo (0 o 1).
    """
    connection = create_connection()
    if connection:
        try:
            query = """
            UPDATE dispositivos
            SET estado = %s
            WHERE id = %s;
            """
            params = (estado, id_dispositivo)
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
