import pandas as pd
import sqlite3
from flask import Flask, jsonify
import os

app = Flask(__name__)

# Obtener el directorio de trabajo actual
directorio_actual = os.getcwd()

def inicializar_bd():
    """
    Inicializa la base de datos leyendo un archivo Excel y creando una tabla SQL.
    """
    try:
        # Ruta relativa al archivo (ajusta según sea necesario)
        ruta_archivo = os.path.join(directorio_actual, 'Superstore.xlsx')
        df = pd.read_excel(ruta_archivo)
        print("Archivo Excel cargado correctamente.")

        # Conectar a la base de datos SQLite
        conn = sqlite3.connect('ventas.db')

        # Crear la tabla 'pedidos' a partir del DataFrame
        df.to_sql('pedidos', conn, if_exists='replace', index=False)
        conn.close()
        print("Base de datos inicializada exitosamente.")

    except FileNotFoundError as e:
        print(f"El archivo Excel no se encontró: {e}")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {str(e)}")

# Inicializa la base de datos al inicio
inicializar_bd()

def obtener_conexion_bd():
    """
    Establece y retorna una conexión a la base de datos.
    """
    return sqlite3.connect('ventas.db')

@app.route('/pedidos/<order_id>', methods=['GET'])
def obtener_pedido(order_id):
    """
    Maneja la solicitud GET para obtener un pedido específico.
    """
    conn = obtener_conexion_bd()
    try:
        # Ejecuta la consulta SQL para obtener el pedido
        cursor = conn.execute("SELECT * FROM pedidos WHERE [Order ID] = ?", (order_id,))
        resultado = cursor.fetchone()

        if resultado:
            # Obtiene los nombres de las columnas
            columnas = [description[0] for description in cursor.description]
            # Convierte el resultado a un diccionario
            pedido = dict(zip(columnas, resultado))
            return jsonify(pedido)
        else:
            return jsonify({"error": "Pedido no encontrado"}), 404

    except sqlite3.Error as e:
        # Maneja errores específicos de SQLite
        return jsonify({"error": f"Error de base de datos: {e}"}), 500
    except Exception as e:
        # Maneja otros tipos de excepciones
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)