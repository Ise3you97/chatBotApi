# main.py
import openai
from config import OPENAI_API_KEY
from db import MongoDB

openai.api_key = OPENAI_API_KEY
mongo_db = MongoDB()

def obtener_respuesta(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except openai.error.RateLimitError:
        return "Error: Has superado tu cuota de uso. Intenta de nuevo más tarde."
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    while True:
        prompt = input("Ingresa tu pregunta (o 'quit' para salir): ")
        
        if prompt.lower() in ['quit', 'exit']:
            print("Saliendo del programa...")
            break
        
        respuesta = obtener_respuesta(prompt)
        print("Respuesta:", respuesta)

        
        mongo_db.almacenar_prompt_y_respuesta(prompt, respuesta)
