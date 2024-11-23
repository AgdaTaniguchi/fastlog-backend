from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from time import sleep

app = Flask(__name__)
CORS(app)

print("HOST:", os.environ["MYSQL_HOST"])

# Função para conectar ao banco de dados
def connect_database():
    retries = 5
    while retries > 0:
        try:
            database = mysql.connector.connect(
                host=os.environ["MYSQL_HOST"],
                user=os.environ["MYSQL_USER"],
                password=os.environ["MYSQL_PASSWORD"],
                database=os.environ["MYSQL_DATABASE"],
            )
            print("Conexão ao banco de dados bem-sucedida.")
            return database
        except Error as e:
            print(f"Erro ao se conectar com o banco de dados: {e}")
            retries -= 1
            print(f"Tentando novamente... {retries} tentativas restantes.")
            sleep(2)

    print("Não foi possível estabelecer conexão com o banco de dados.")
    return None

# Inicializa a conexão
database = connect_database()

@app.route("/status")
def status_route():
    global database
    try:
        tracking_id = request.args.get("id")

        if not tracking_id:
            return jsonify({"error": "ID de rastreamento não fornecido"}), 400
        
        # Verifica e reconecta ao banco, se necessário
        if not database or not database.is_connected():
            database = connect_database()
            if not database:
                return jsonify({"error": "Falha ao conectar ao banco de dados"}), 500

        cursor = database.cursor()

        # Usa parâmetros para evitar injeção de SQL
        query = """
            SELECT d.tracking_number, d.estimated_date, u.delivery_status, u.updated_date
            FROM delivery d
            INNER JOIN delivery_update u ON d.tracking_number = u.tracking_number
            WHERE d.tracking_number = %s
        """
        cursor.execute(query, (tracking_id,))
        results = cursor.fetchall()

        if not results:
            return jsonify([]), 404

        # Formata os dados para o cliente
        response = {
            "tracking_number": results[0][0],
            "estimated_date": results[0][1],
            "status": [
                {"delivery_status": result[2], "updated_date": result[3]} for result in results
            ],
        }

        return jsonify(response), 200
    except Exception as e:
        print(f"Erro ao processar a requisição: {e}")
        return jsonify({"error": "Erro interno no servidor"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8501)
