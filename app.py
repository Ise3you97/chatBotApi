from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import openai
from config import OPENAI_API_KEY
from db import MongoDB

app = Flask(__name__)
CORS(app)

mongo_db = MongoDB()
openai.api_key = OPENAI_API_KEY

# Enviar datos 
@app.route('/api/obtener-respuesta', methods=['POST'])
def obtener_respuesta():
    data = request.json
    prompt = data.get('prompt')
    speaker = data.get('speaker')
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
        # Almacenar en MongoDB
        mongo_db.almacenar_prompt_y_respuesta(text= prompt, speaker=speaker)
        mongo_db.almacenar_prompt_y_respuesta(text= text, speaker= "System")
        
        return jsonify({"speaker": speaker, "output": text}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Mostrar Datos
@app.route('/api/data', methods=['GET'])
def obtener_prompts():
    try:
        prompts = mongo_db.obtener_prompts()
        return jsonify(prompts), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
