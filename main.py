import os 
from langchain_openai import ChatOpenAI 
from langchain_core.prompts import PromptTemplate 
from dotenv import load_dotenv 

# Carica le variabili di ambiente da un file .env
load_dotenv()

# Definisci una funzione per generare un nome per un animale domestico
def generate_pet_name(animal_type, pet_color):
    # Crea un'istanza di ChatOpenAI con la tua chiave API e una temperatura impostata a 0.7 per generare risposte più creative
    llm = ChatOpenAI(api_key=os.getenv('OPENAI_API_KEY'), temperature=0.7)

    # Crea un prompt template con spazi vuoti da riempire con l'animale e il suo colore
    prompt_template = "Ho un {} e vorrei un nome per lui. Suggeriscimi cinque nomi da dargli se il suo colore è {}. Senza altri commenti."
    prompt = PromptTemplate.from_template(prompt_template.format(animal_type, pet_color))

    # Crea una catena di operazioni concatenando l'istanza di ChatOpenAI e il prompt template
    chain = llm | prompt

    # Invoca la catena con il prompt per ottenere una risposta
    response = chain.invoke(prompt) 

    # Restituisci la risposta generata
    return response

# Esegui il codice solo se questo modulo è eseguito come script principale
if __name__ == "__main__":
    # Chiama la funzione generate_pet_name con "cane" come tipo di animale e "nero" come colore e stampa il risultato
    print(generate_pet_name("cane", "nero"))
