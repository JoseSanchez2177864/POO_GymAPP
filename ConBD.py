# conexion.py
import pyodbc

def crear_conexion():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DESKTOP-IJ2TNG7\\SQLEXPRESS;'  
            'DATABASE=Road_To_Fit;'
            'Trusted_Connection=yes;'
        )
        return conn
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None
def probar_conexion():
    conn = crear_conexion()
    if conn:
        print("✅ ¡Conexión exitosa!")
        conn.close()
    else:
        print("❌ No se pudo conectar.")

probar_conexion()
