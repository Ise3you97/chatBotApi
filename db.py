from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME
from datetime import datetime

class MongoDB:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]
        
    # Funcion para almacenar datos
    def almacenar_prompt_y_respuesta(self, text, speaker):
        documento = {
            'speaker': speaker,
            'text': text,
             'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        self.collection.insert_one(documento)

    # Funcion para mostrar todos los datos 
    def obtener_prompts(self):
        # Convertir ObjectId a string
        return [
            {
                "_id": str(doc["_id"]),
                "speaker": doc["speaker"],
                "text": doc["text"],
                "timestamp": doc["timestamp"]
            }
            for doc in self.collection.find()
        ]
