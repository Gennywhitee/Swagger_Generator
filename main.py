from langchain_openai import ChatOpenAI 
from langchain_core.prompts import PromptTemplate 
from dotenv import load_dotenv 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Carica le variabili di ambiente da un file .env
load_dotenv()
model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.7)
# Modifica la funzione generate_pet_name per creare un oggetto StringPromptValue dal template prima di passarlo alla funzione invoke
def generate_pet_name(animal_type, pet_color):
    prompt = ChatPromptTemplate.from_template("Ho un {animal_type} e vorrei un nome per lui. Suggeriscimi cinque nomi da dargli se il suo colore è {pet_color}. Senza altri commenti.")
    output_parser = StrOutputParser()
    
    chain = prompt | model | output_parser

    response = chain.invoke({"animal_type" :animal_type, "pet_color":pet_color})

    return response

if __name__ == "__main__":
    print(generate_pet_name("cavallo", "bianco"))


