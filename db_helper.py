import mysql.connector
import os

def get_db():
    host = os.environ.get("HOST")
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    database = os.environ.get("DATABASE")
    
    conexion = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    
    # IMPORTANTE: Configuramos para que guarde cambios automáticamente
    conexion.autocommit = True
    
    # IMPORTANTE: Al guardar la conexión dentro del cursor,
    # evitamos que Python la cierre por error.
    cursor = conexion.cursor(dictionary=True)  #Nos da la informacion de la base de datos en forma de diccionario con los nombres de las columnas
    cursor._conexion_padre = conexion 
    
    return conexion, cursor