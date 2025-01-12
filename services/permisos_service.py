from services.base_datos import create_connection, execute_query, close_connection

def obtener_dispositivos_usuario(id_usuario):
    """
    Obtiene los dispositivos asociados a un usuario desde la tabla de permisos.
    
    Args:
        id_usuario (int): ID del usuario.

    Returns:
        list: Lista de dispositivos asociados al usuario.
    """
    connection = create_connection()
    dispositivos = []
    if connection:
        try:
            query = """
            SELECT d.id, d.nombre, d.tipo, d.descripcion
            FROM permisos p
            JOIN dispositivos d ON p.id_dispositivo = d.id
            WHERE p.id_usuario = %s;
            """
            params = (id_usuario,)
            cursor = connection.cursor()
            cursor.execute(query, params)
            dispositivos = cursor.fetchall()
            cursor.close()
        finally:
            close_connection(connection)
    return dispositivos

def agregar_permiso(id_usuario, id_dispositivo):
    """
    Agrega un permiso asociando un dispositivo a un usuario en la tabla de permisos.

    Args:
        id_usuario (int): ID del usuario.
        id_dispositivo (int): ID del dispositivo.
    """
    connection = create_connection()
    if connection:
        try:
            query = """
            INSERT INTO permisos (id_usuario, id_dispositivo)
            VALUES (%s, %s);
            """
            params = (id_usuario, id_dispositivo)
            execute_query(connection, query, params)
        finally:
            close_connection(connection)
