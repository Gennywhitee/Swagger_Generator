from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def uploadfiles():
    # Recupera i file dal request
    uploadedfiles = request.files.getlist('files')

    for file in uploadedfiles:
        print(f"Ricevuto file: {file.filename}")
        # Qui puoi aggiungere la logica per elaborare i file, salvarli, o generare Swagger

    return {"message": "File ricevuti correttamente."}, 200

if __name__ == '__main':
    app.run(host='0.0.0.0', port=5000)