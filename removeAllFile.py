import os
import shutil

def remove_files_and_folders():
    paths_to_remove = [
        './output_swagger_folder',  # Cartella
        './output_dipendenze/final_output.java',  # File
        './jsonDependecies/dependeciesTree.json',  # File
        './java_classes_modified'  # Cartella
    ]
    
    for path in paths_to_remove:
        if os.path.exists(path):
            if os.path.isdir(path):  # Controllo se è una cartella
                shutil.rmtree(path)  # Rimuove cartella e tutto il suo contenuto
                print(f"Cartella rimossa: {path}")
            elif os.path.isfile(path):  # Controllo se è un file
                os.remove(path)  # Rimuove il file
                print(f"File rimosso: {path}")
        else:
            print(f"Il path non esiste: {path}")

