import re  
import os  
from IO_function import *  

# Funzione per trovare e restituire solo le dipendenze dalle relazioni JPA
def extract_dependencies(java_code):
    
    # Regex per trovare le relazioni con altre entità
    dependency_pattern = r'@(OneToOne|OneToMany|ManyToOne|ManyToMany)[^;]*\s+private\s+([\w<>]+)\s+([\w]+);'
    
    # Trova tutte le corrispondenze delle relazioni e dei campi privati nel codice Java
    matches = re.findall(dependency_pattern, java_code)

    dependencies = []
    # Per ogni corrispondenza trovata, creo una stringa che rappresenta la relazione
    for match in matches:
        relation_type, class_name, variable_name = match
        dependencies.append(f'{class_name} {variable_name};')
    
    return dependencies 

# Funzione per generare l'output con solo le dipendenze trovate
def clean_java_class(java_code):
    
    # Cerco il nome della classe con una regex
    class_name_match = re.search(r'class\s+(\w+)\s*', java_code)
    
    if class_name_match:
        # Estrae il nome della classe
        class_name = class_name_match.group(1)
        # Estrae le dipendenze
        dependencies = extract_dependencies(java_code)
        
        # Se ci sono dipendenze trovate, genero il codice della classe con solo quelle
        if dependencies:
            cleaned_code = f'class {class_name}{{' 
            for dep in dependencies: cleaned_code += f' {dep}' 
            cleaned_code += '}\n'
            return cleaned_code
        else:
            # Se non ci sono dipendenze, restituisco una classe vuota 
            return f'class {class_name}{{}}\n'
    else:
        # Caso in cui nei file non vi è la classe cercata
        return "// Nessuna classe trovata\n"

# Funzione per processare una directory di file Java
def process_java_directory(input_dir, output_file):

    all_cleaned_code = []  # Lista per memorizzare il codice ripulito di ogni file

    # Scorro ogni file nella directory specificata
    for filename in os.listdir(input_dir):
        if filename.endswith(".java"):
            file_path = os.path.join(input_dir, filename)
            java_code = text_from_file(file_path)

            if not java_code:
                print(f"Il file {filename} è vuoto o non può essere letto.")
                continue  # Se il file è vuoto o non può essere letto, passo al successivo

            # Pulisco il codice Java mantenendo solo le dipendenze
            cleaned_code = clean_java_class(java_code)
            all_cleaned_code.append(cleaned_code)  # Aggiungo il codice pulito alla lista

    # Unisco tutto il codice ripulito in un'unica stringa
    final_cleaned_code = "\n\n".join(all_cleaned_code)

    out_on_file(final_cleaned_code, output_file)

    
    if final_cleaned_code.strip() == "":
        print("Errore: il file di output finale è vuoto!")
    else:
        print("Il file di output contiene dati.")

    return final_cleaned_code 



 
process_java_directory('java_classes', 'output_dipendenze/final_output.java')
