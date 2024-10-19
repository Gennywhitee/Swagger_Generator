import os
from dotenv import load_dotenv 
from IO_function import *
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def changeNames(input_file):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

    # Imposta il parser per l'output
    output_parser = StrOutputParser()

    java_code = text_from_file(input_file)


    prompt = ChatPromptTemplate.from_template("""
                                                Task: Refactor a Java Entity Bean file by renaming the variables according to the following rules:

                                                1. Variables must be written entirely in English.
                                                2. Variable names must follow the camelCase pattern, where the first word is lowercase, and each subsequent word 
                                                starts with an uppercase letter.
                                                3. Expand abbreviations or acronyms into their full forms (e.g., empId becomes employeeId).

                                                Additional Requirement:
                                                - At the end of the file, append the following string: newline /*=== Variable Changes ===*/ newline.
                                                - Below this string, list the changes made to the variable names in the format: originalName -> newName.

                                                Example:
                                                If a variable is changed from `empId` to `employeeId`, the end of the file should look like this:

                                                /*=== Variable Changes ===*/
                                                empId -> employeeId
                                                deptName -> departmentName

                                                java class is: \n {java_code}
                                              """)
    chain = prompt | llm | output_parser

    response = chain.invoke({"java_code":java_code})

    output_directory = 'java_classes_modified'
    
    # Crea la cartella se non esiste
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Estrai il nome del file dall'input e crea il percorso di output
    output_file = os.path.join(output_directory, os.path.basename(input_file))
    out_on_file(response, output_file)
    refactorJavaClass(output_file)

    return output_file

def refactorJavaClass(input_file):
    java_code = text_from_file(input_file)
    change_marker = "/*=== Variable Changes ===*/"

    if change_marker in java_code:
        java_code_parts = java_code.split(change_marker)
        java_code = java_code_parts[0]  # Codice senza la sezione delle modifiche
        mapping_text = java_code_parts[1].strip()  # Parte delle modifiche senza spazi
        
        # Salva il codice modificato nel file originale
        out_on_file(java_code, input_file)

        modified_dir = os.path.dirname(input_file)
        mapping_dir = os.path.join(modified_dir,"mapping")
        os.makedirs(mapping_dir, exist_ok=True)

        # crea il path per il mapping associato a quel file
        base_name = os.path.splitext(os.path.basename(input_file))[0]  # Rimuove l'estensione del file
        mapping_file = os.path.join(mapping_dir,f"{base_name}_mapping.txt")  # Crea il nuovo nome per il file di mapping
        
        # Salva il mapping delle variabili nel nuovo file
        out_on_file(mapping_text, mapping_file)
    

def change_names_by_folder(input_directory):
    # Scorre attraverso la cartella specificata
    for root, dirs, files in os.walk(input_directory):
        for f in files:
            if f.endswith(".java"):  # Verifica che sia un file .java
                # Costruisce il percorso completo del file
                file_path = os.path.join(root, f)
                
                # Richiama la funzione per refactorizzare la classe Java
                try:
                    changeNames(file_path)
                    print(f"File processed: {file_path}")
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
    
    print("Esecuzione Terminata\n")



