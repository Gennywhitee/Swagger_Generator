import os
import json
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from IO_function import *
from web_function import *
from yaml_control import *

# Funzione per leggere il file JSON con le dipendenze
def load_class_dependencies(json_file):
    with open(json_file, 'r') as file:
        class_data = json.load(file)
    return class_data

# Funzione per trovare il file Java corrispondente a una classe
def find_java_file(class_name, folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".java") and class_name in filename:
            return os.path.join(folder_path, filename)
    return None

# Funzione per creare la cartella di output
def create_output_folder(output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

# Funzione per salvare il testo unito in un file
def save_merged_class(class_name, merged_text, output_folder):
    file_path = os.path.join(output_folder, f"{class_name}_merged.java")
    with open(file_path, 'w') as file:
        file.write(merged_text)
    print(f"File unito salvato: {file_path}")

# Funzione ricorsiva per unire le dipendenze delle dipendenze, evitando duplicazioni
def merge_class_with_dependencies(class_name, class_text, dependencies, folder_path, class_dependencies, merged_classes=None):
    # Inizializza l'insieme delle classi già elaborate se non è fornito
    if merged_classes is None:
        merged_classes = set()

    # Inizialmente contiene solo il testo della classe principale
    merged_text = class_text
    
    # Evita di processare una classe che è già stata aggiunta
    if class_name in merged_classes:
        return merged_text
    
    # Aggiungi la classe corrente all'insieme delle classi già elaborate
    merged_classes.add(class_name)

    # Cerca le dipendenze e aggiungile al contenuto della classe principale
    for dependency in dependencies:
        # Trova il percorso del file Java della dipendenza
        dep_class_path = find_java_file(dependency, folder_path)
        if dep_class_path:
            # Leggi il contenuto della dipendenza
            dep_class_text = text_from_file(dep_class_path)
            if dep_class_text:
                # Controlla se la dipendenza ha ulteriori dipendenze
                if dependency in class_dependencies and "dependencies" in class_dependencies[dependency]:
                    nested_dependencies = class_dependencies[dependency]["dependencies"]
                    if nested_dependencies:
                        # Unisci il testo della dipendenza con le sue dipendenze ricorsive
                        dep_class_text = merge_class_with_dependencies(
                            dependency, dep_class_text, nested_dependencies, folder_path, class_dependencies, merged_classes
                        )
                
                # Aggiungi il contenuto della dipendenza (incluso il testo ricorsivo) alla classe principale
                merged_text += "\n\n" + dep_class_text
            else:
                print(f"Il file Java della dipendenza {dependency} è vuoto.")
        else:
            print(f"File Java per la dipendenza {dependency} non trovato.")
    
    return merged_text


# Funzione principale per generare la documentazione Swagger e salvarla
def swagger_generator_from_json(json_file, folder_path, context, output_folder="swagger_output"):
    # Carica le dipendenze delle classi dal file JSON
    class_dependencies = load_class_dependencies(json_file)
    
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.5)
    output_parser = StrOutputParser()
    
    # Crea la cartella di output
    create_output_folder(output_folder)
    
    for class_name, data in class_dependencies.items():
        # Trova il file Java per la classe principale
        java_class_path = find_java_file(class_name, folder_path)
        if not java_class_path:
            print(f"File Java per {class_name} non trovato.")
            continue
        
        # Legge il contenuto del file Java della classe principale
        main_class_text = text_from_file(java_class_path)
        if not main_class_text:
            print(f"La classe Java {class_name} è vuota.")
            continue
        
        # Unisce la classe principale con le sue dipendenze
        if "dependencies" in data and data["dependencies"]:
            merged_text = merge_class_with_dependencies(
                class_name, main_class_text, data["dependencies"], folder_path, class_dependencies, merged_classes=set()
            )
        else:
            merged_text = main_class_text  # Se non ha dipendenze, il testo rimane solo quello della classe principale
        
        # Inizializza la lista per raccogliere le parti YAML
        yaml_parts = []
        
        # Non dividere il testo in chunk, passare l'intero merged_text al prompt
        prompt = ChatPromptTemplate.from_template(
            "Genera **esclusivamente** la documentazione Swagger seguendo lo standard OpenAPI 3.0 per il seguente entity bean in Java: {text}. "
            "Crea i metodi CRUD necessari, formattati correttamente in YAML, e non includere **nessun** testo che non faccia parte della documentazione Swagger. "
            "Non includere commenti, spiegazioni o descrizioni aggiuntive. "
            "La documentazione deve essere conforme alle regole dello standard che trovi qui: {context}. "
            "IMPORTANTE: L'output deve essere puramente YAML, senza altri contenuti extra."
        )
        
        # Invoca il modello per generare lo YAML
        chain = prompt | llm | output_parser
        response = chain.invoke({"text": merged_text, "context": context})
        yaml_parts.append(response)
        
        # Unisci tutte le parti YAML generate (in questo caso dovrebbe essere solo una)
        final_yaml = "\n".join(yaml_parts)
        
        # Salva il file YAML nella cartella di output
        output_file_path = os.path.join(output_folder, f"{class_name}_swagger_output.yaml")
        out_on_file(final_yaml, output_file_path)
        
        print(f"Swagger YAML per {class_name} (con dipendenze) generato e salvato in {output_file_path}.")
    
    return "Generazione Swagger completata."
