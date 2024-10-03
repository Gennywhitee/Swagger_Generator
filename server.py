from flask import Flask, request, jsonify
import os
import subprocess
from app import startapp  # Assicurati di importare correttamente la funzione

app = Flask(__name__)

@app.route('/swagger', methods=['POST'])
def swagger():
    classes_dir = "java_classes"
    output_dir = "output_swagger_folder"  # Directory where output is generated

    # Assicurati che le directory esistano
    os.makedirs(classes_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)  # Assicurati che la directory di output esista

    # Recupera i file dalla richiesta
    uploadedfiles = request.files.getlist('files')

    saved_files = []  # Lista per tenere traccia dei file salvati
    rejected_files = []  # Lista per tenere traccia dei file rifiutati

    # Controlla se sono stati caricati file .java
    for file in uploadedfiles:
        if file.filename.endswith('.java'):
            print(f"Ricevuto file: {file.filename}")
            # Salva il file usando il metodo save dell'oggetto file
            file_path = os.path.join(classes_dir, file.filename)
            file.save(file_path)
            saved_files.append(file.filename)  # Tieni traccia del file salvato
        else:
            rejected_files.append(file.filename)  # Tieni traccia del file rifiutato
            print(f"File rifiutato (non .java): {file.filename}")

    # Se non sono stati salvati file .java, restituisci un messaggio di errore
    if not saved_files:
        return {
            "error": "Nessun file .java ricevuto.",
            "rejected_files": rejected_files
        }, 400  # 400 Bad Request status code

    # Esegui la funzione startapp() dopo aver salvato i file
    try:
        startapp()  # Chiama la funzione per eseguire l'app
        print("startapp eseguita con successo.")
    except Exception as e:  # Cambiato per catturare tutte le eccezioni
        return {
            "error": f"Errore nell'esecuzione di startapp: {str(e)}"
        }, 500  # 500 Internal Server Error status code

    # Elenca il contenuto della directory di output
    output_files = os.listdir(output_dir)
    output_files_full_paths = [os.path.join(output_dir, file) for file in output_files]

    response = {
        "message": "File ricevuti correttamente.",
        "saved_files": saved_files,
        "rejected_files": rejected_files,
        "output_files": output_files_full_paths  # Include i percorsi completi dei file di output nella risposta
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
