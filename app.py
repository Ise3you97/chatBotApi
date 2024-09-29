# app.py
import json  # Asegúrate de importar el módulo json
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import openai
from config import OPENAI_API_KEY
from db import MongoDB

app = Flask(__name__)
CORS(app)

mongo_db = MongoDB()
openai.api_key = OPENAI_API_KEY

@app.route('/api/obtener-respuesta', methods=['POST'])
def obtener_respuesta():
    data = request.json
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({"error": "Prompt no proporcionado"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        text = response['choices'][0]['message']['content']
        speaker = "kelvin"
        # Almacenar en MongoDB
        mongo_db.almacenar_prompt_y_respuesta(text= prompt, speaker=speaker)
        mongo_db.almacenar_prompt_y_respuesta(text= text, speaker= speaker)
        
        return jsonify({"speaker": speaker, "respuesta": text}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/prompts', methods=['GET'])
def obtener_prompts():
    try:
        prompts = mongo_db.obtener_prompts()
        return jsonify(prompts), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/exportar-json', methods=['GET'])
def exportar_json():
    try:
        prompts = mongo_db.obtener_prompts()
        
        # Escribir los datos en un archivo .txt
        with open('prompts.json', 'w') as json_file:
            json.dump(prompts, json_file, default=str)  # Convertir ObjectId a string

        return send_file('prompts.json', as_attachment=True)  # Enviar el archivo como respuesta

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
