# Empezar corriendo una imagen de python 
FROM python:3.8-alpine

# Copiar requerimientos para ejecutar el programa
COPY ./requirements.txt /appofertas/requirements.txt

# Cambiar de directorio de trabajo a donde esta el ejectuable del API
WORKDIR /appofertas

# Instalar requerimientos de la app
RUN pip install -r requirements.txt

# Copiar el contenido del directorio actual en la imagen de docker
COPY . /appofertas

COPY ./entrypoint.sh /appofertas/entrypoint.sh
RUN ["chmod", "+x", "/appofertas/entrypoint.sh"]
# Configurar el contenedor para correr en una manera ejectuble
ENTRYPOINT ["/appofertas/entrypoint.sh"]

# Archivo principal donde corre el API
CMD [ "python", "app.py" ]


