FROM python:3.9-slim

WORKDIR /server

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./
COPY java_classes/ ./java_classes/
COPY java_classes_modified/ ./java_classes_modified/
COPY output_dipendenze/ ./output_dipendenze/
COPY jsonDependecies/ ./jsonDependecies/
COPY output_swagger_folder/ ./output_swagger_folder/

EXPOSE 5000

CMD ["python","server.py"]