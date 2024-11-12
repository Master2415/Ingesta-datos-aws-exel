import pandas as pd
import mysql.connector
import glob

# Configuración de la conexión a la base de datos
db_config = {
    'user': 'root',
    'password': 'root1234',
    'host': 'datalake-uniquindio.cfgqm6ii0exs.us-east-1.rds.amazonaws.com',
    'database': 'DATALAKE'
}

# Función para cargar datos de un archivo Excel a una tabla
def cargar_datos_excel(ruta_archivo, tabla):
    # Conectar a MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Leer archivo Excel
    df = pd.read_excel(ruta_archivo)

    # Insertar cada registro en la tabla
    for _, row in df.iterrows():
        sql = f"INSERT INTO {tabla} (nombre_estudiante, codigo_estudiante, materia, nota, periodo_academico, programa_academico) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (
            row['Nombre del estudiante'],
            row['Código del estudiante'],
            row['Materia'],
            row['Nota'],
            row['Periodo académico'],
            row['Programa académico']
        )
        cursor.execute(sql, valores)

    # Confirmar transacción
    conn.commit()
    cursor.close()
    conn.close()

# Rutas de los archivos Excel
rutas_ing_sistemas = glob.glob("C:/Users/DOUGLAS/OneDrive/Universidad/11 SEMESTRE/Data Like/XLXS/ing-sistemas/*.xlsx")
rutas_administracion = glob.glob("C:/Users/DOUGLAS/OneDrive/Universidad/11 SEMESTRE/Data Like/XLXS/administracion/*.xlsx")

# Procesar cada archivo y cargarlo en la tabla correspondiente
for ruta in rutas_ing_sistemas:
    cargar_datos_excel(ruta, "ing_sistemas")

for ruta in rutas_administracion:
    cargar_datos_excel(ruta, "administracion")

print("Carga de datos completada.")
