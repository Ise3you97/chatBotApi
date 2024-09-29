from datetime import datetime
import json
import requests
from pymongo import MongoClient

# Conectar a la base de datos MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Cambia la URI si es necesario
db = client['chatGptTEST_db']  # Nombre de la base de datos
users_collection = db['users']  # Colección de usuarios
messages_collection = db['messages']  # Colección de mensajes

# Función para agregar un usuario a la base de datos
def add_user_to_db(username: str):
    user = {
        "username": username,
        "timestamp": datetime.utcnow().isoformat() + 'Z'
    }
    users_collection.insert_one(user)  # Inserta el usuario en la colección

# Función para agregar un mensaje a la base de datos
def add_message_to_db(speaker: str, text: str):
    timestamp = datetime.utcnow().isoformat() + 'Z'  # Genera el timestamp en formato ISO 8601 UTC
    message = {
        "speaker": speaker,
        "text": text,
        "timestamp": timestamp
    }
    messages_collection.insert_one(message)  # Inserta el mensaje en la colección

# Función para obtener la respuesta de la API de ChatGPT
def get_chatgpt_response(prompt: str):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer YOUR_API_KEY",  # Reemplaza con tu clave de API
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",  # O el modelo que estés usando
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    
    # Extrae la respuesta de la API
    chatgpt_output = response_data['choices'][0]['message']['content'] if 'choices' in response_data else "Error en la respuesta."
    return chatgpt_output

# Ciclo para ingresar usuarios y mensajes
while True:
    # Pedir al usuario que ingrese un nombre de usuario
    username = input("Ingresa el nombre de usuario (o 'salir' para terminar): ")
    if username.lower() == 'salir':
        break
    add_user_to_db(username)

    # Pedir al usuario que ingrese un mensaje
    message_text = input(f"Ingrese un mensaje de {username}: ")
    add_message_to_db(username, message_text)

    # Obtener respuesta de ChatGPT
    chatgpt_response = get_chatgpt_response(message_text)
    add_message_to_db("system", chatgpt_response)

# Mostrar un resumen de los datos almacenados (opcional)
print("\nDatos almacenados:")
print("Usuarios:", users_collection.find())
print("Mensajes:", messages_collection.find())
